#!/usr/bin/python3

import time
import copy
import requests
from bs4 import BeautifulSoup

from ..company import *

#---

def CreateTR( iSoup, iText, iValues, iHeader=False ):
	td = iSoup.new_tag( 'th' if iHeader else 'td' )
	td.string = iText
	tr = iSoup.new_tag( 'tr' )
	tr.append( td )
	
	for v in iValues:
		td = iSoup.new_tag( 'th' if iHeader else 'td' )
		td.string = str( v )
		tr.append( td )
		
	# td = iSoup.new_tag( 'th' if iHeader else 'td' )
	# td.string = 'Last 5 Years'
	# tr.append( td )
	
	return tr

def Extract( iCompany, iSoup ):
	div_data = iSoup.new_tag( 'div' )
	# div_data['class'] = 'clear last10'
	
	if not iCompany.mMorningstarRegion:
		return div_data
	
	tbody = iSoup.new_tag( 'tbody' )
	
	#---
	
	tr = CreateTR( iSoup, '', iCompany.is_years, True )
	tbody.append( tr )
	
	tr = CreateTR( iSoup, 'EBITDA', iCompany.ebitdas )
	tbody.append( tr )
	
	#---
	
	tr = CreateTR( iSoup, '', iCompany.bs_years, True )
	tbody.append( tr )
	
	tr = CreateTR( iSoup, 'LT-Debt', iCompany.ltd )
	tbody.append( tr )
	
	#---
	
	tr = CreateTR( iSoup, '', iCompany.financials_years, True )
	tbody.append( tr )
	
	tr = CreateTR( iSoup, 'Revenue', iCompany.revenues )
	tbody.append( tr )
	
	tr = CreateTR( iSoup, 'EPS', iCompany.earnings )
	tbody.append( tr )
	
	#---
	
	tr = CreateTR( iSoup, '', iCompany.profitability_years, True )
	tbody.append( tr )
	
	tr = CreateTR( iSoup, 'ROE', iCompany.roes )
	tbody.append( tr )
	
	tr = CreateTR( iSoup, 'ROI', iCompany.rois )
	tbody.append( tr )
	
	tr = CreateTR( iSoup, 'Interest Cover', iCompany.ics )
	tbody.append( tr )
	
	tr = CreateTR( iSoup, 'FCF/Sales', iCompany.fcf_ss )
	tbody.append( tr )
	
	#---
	
	tr = CreateTR( iSoup, '', iCompany.health_years, True )
	tbody.append( tr )
	
	tr = CreateTR( iSoup, 'Current Ratio', iCompany.currentratios )
	tbody.append( tr )
	
	tr = CreateTR( iSoup, 'Debt/Equity', iCompany.d_es )
	tbody.append( tr )
	
	#---
	
	table = iSoup.new_tag( 'table' )
	table.append( tbody )
	
	div_data.append( table )
	
	return div_data;

