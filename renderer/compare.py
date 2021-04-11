#!/usr/bin/env python3
#
# Copyright (c) 2018-20 m-ll. All Rights Reserved.
#
# Licensed under the MIT License.
# See LICENSE file in the project root for full license information.
#
# 2b13c8312f53d4b9202b6c8c0f0e790d10044f9a00d8bab3edf3cd287457c979
# 29c355784a3921aa290371da87bce9c1617b8584ca6ac6fb17fb37ba4a07d191
#

import copy
from datetime import date, datetime
from io import BytesIO
import math
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style
init( autoreset=True )

#---

def Title( iStockIndex, iCompanies, iSoup ):
    
    root = iSoup.new_tag( 'span' )
    root.append( iStockIndex.Name() )
    return root

#---

def CheckSameRowCount( iStockIndex, iCompanies ):
    index_dates = [ r['date'] for r in iStockIndex.mYahooFinance.mHistoric ]

    for company in iCompanies:
        company_dates = [ r['date'] for r in company.mYahooFinance.mHistoric ]
        if index_dates != company_dates:
            return company
    
    return None

def CompareWithStockIndex( iStockIndex, iCompanies, iSoup ):

    #TODO: maybe process the first part (check/compute/...) outside the renderer ?

    companies_of_same_zone = [ company for company in iCompanies if company.Zone() == iStockIndex.Zone() ]
    
    company = CheckSameRowCount( iStockIndex, companies_of_same_zone )
    if company is not None:
        print( Back.RED + f'Problem with historic rows between stock-index ({iStockIndex.Name()}) and one company ({company.Name()})' )

        root = iSoup.new_tag( 'span' )
        root.append( f'Problem with historic rows between stock-index ({iStockIndex.Name()}) and one company ({company.Name()})' )
        return root
    
    companies_with_invest = [ company for company in companies_of_same_zone if company.HasInvested() ]
    companies_without_invest = [ company for company in companies_of_same_zone if not company.HasInvested() ]
    if len( companies_with_invest ) and len( companies_without_invest ):
        print( Back.RED + f'Problem with companies with AND without invest ...' )

        root = iSoup.new_tag( 'span' )
        root.append( f'Problem with companies with AND without invest ...' )
        return root
    
    #---

    total_invest = 0
    for company in companies_of_same_zone:
        if not company.HasInvested():
            continue
        total_invest += company.GetInvested().ComputeTotalPrice()
    
    weight_of_each_company = []
    for company in companies_of_same_zone:
        if not company.HasInvested():
            weight_of_each_company.append( 1000 )
            continue

        company_invest = company.GetInvested().ComputeTotalPrice()

        weight_of_each_company.append( company_invest / total_invest * 1000 * len(companies_of_same_zone) ) #TOCHECK if correct

    for company, company_weight in zip( companies_of_same_zone, weight_of_each_company ):
        company.mYahooFinance.ComputeWeightPrice( company_weight )
    
    #---

    iStockIndex.mYahooFinance.ComputeWeightPrice( sum( weight_of_each_company ) )

    #---

    portfolio_weighted = []
    for row in iStockIndex.mYahooFinance.mHistoric:
        sum_row = { 'date': row['date'], 'price-weighted': 0.0 }
        for company in companies_of_same_zone:
            company_historic_row = next( ( r for r in company.mYahooFinance.mHistoric if r['date'] == sum_row['date'] ), None )
            sum_row['price-weighted'] += company_historic_row['price-weighted']
        portfolio_weighted.append( sum_row )

    #---

    plt.gcf().set_size_inches( 20, 5 )

    # first line
    x1 = [ row['date'] for row in iStockIndex.mYahooFinance.mHistoric ]
    y1 = [ row['price-weighted'] for row in iStockIndex.mYahooFinance.mHistoric ]
    # plotting the line 1 points
    plt.plot( x1, y1, '--', label=iStockIndex.Name())

    # second line
    x2 = [ row['date'] for row in portfolio_weighted ]
    y2 = [ row['price-weighted'] for row in portfolio_weighted ]
    # plotting the line 2 points
    plt.plot( x2, y2, label=f'{iStockIndex.Zone().upper()} ({len(companies_of_same_zone)})' )

    # show a legend on the plot
    plt.legend()

    # function to show the plot
    f = BytesIO()
    plt.savefig( f, format="svg" )
    plt.close()

    #---

    soup_xml = BeautifulSoup( f.getvalue().decode( 'utf-8' ), 'xml' )

    root = iSoup.new_tag( 'span' )
    root.append( soup_xml.find( 'svg' ) )

    return root
