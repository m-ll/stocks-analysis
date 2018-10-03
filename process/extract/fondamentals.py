#!/usr/bin/python3

import time
import copy
import requests
from bs4 import BeautifulSoup

from ..company import *

#---

def AddTR( iSoup, iSBody, iText, iData, iDataType, iCSSFunction, iHeader=False ):
	if iData is None:
		return
	
	td = iSoup.new_tag( 'th' )
	td.string = iText
	tr = iSoup.new_tag( 'tr' )
	tr.append( td )
	
	for i, v in enumerate( iData.mData ):
		td = iSoup.new_tag( 'th' if iHeader else 'td' )
		if v:
			if iDataType == 'kGrowth':
				td['class'] = 'plus' if iCSSFunction( float( v ) ) else 'minus'
			elif iDataType == 'kThreshold':
				if iCSSFunction( float( v ) ) == 1:
					td['class'] = 'plus'
				elif iCSSFunction( float( v ) ) == 0:
					td['class'] = 'bof'
				elif iCSSFunction( float( v ) ) == -1:
					td['class'] = 'minus'
		td.string = v
		tr.append( td )
		
	td = iSoup.new_tag( 'th' if iHeader else 'td' )
	td.string = str( iData.mTTM )
	tr.append( td )
	
	td = iSoup.new_tag( 'th' if iHeader else 'td' )
	td.string = str( iData.mLatestQuarter )
	tr.append( td )
	
	iSBody.append( tr )

def Extract( iCompany, iSoup ):
	div_data = iSoup.new_tag( 'div' )
	div_data['class'] = 'clear fondamentals'
	
	if not iCompany.mMorningstarRegion:
		return div_data
	
	tbody = iSoup.new_tag( 'tbody' )
	
	#---
	
	AddTR( iSoup, tbody, '', iCompany.mMorningstarISYears, 'kNone', None, iHeader=True )
	AddTR( iSoup, tbody, 'EBITDA', iCompany.mMorningstarEBITDA, 'kNone', None )
	
	# AddTR( iSoup, tbody, '', iCompany.mMorningstarBSYears, 'kNone', None, iHeader=True )
	AddTR( iSoup, tbody, 'LongTerm Debt', iCompany.mMorningstarLongTermDebt, 'kNone', None )
	AddTR( iSoup, tbody, 'LT-Debt/EBITDA (<5)', iCompany.mMorningstarLTDOnEBITDA, 'kThreshold', lambda v : 1 if v < 5 else -1 )
	
	#---
	
	AddTR( iSoup, tbody, '', iCompany.mMorningstarFinancialsYears, 'kNone', None, iHeader=True )
	# AddTR( iSoup, tbody, '', iCompany.mMorningstarGrowthYears, 'kNone', None, iHeader=True )
	AddTR( iSoup, tbody, 'Revenue', iCompany.mMorningstarFinancialsRevenue, 'kNone', None )
	AddTR( iSoup, tbody, 'Growth Revenue', iCompany.mMorningstarGrowthRevenue, 'kGrowth', lambda v : v >= 0 )
	AddTR( iSoup, tbody, 'Net Income', iCompany.mMorningstarFinancialsNetIncome, 'kNone', None )
	AddTR( iSoup, tbody, 'Growth Net Income', iCompany.mMorningstarGrowthNetIncome, 'kGrowth', lambda v : v >= 0 )
	AddTR( iSoup, tbody, 'Book', iCompany.mMorningstarFinancialsBook, 'kNone', None )
	AddTR( iSoup, tbody, 'Growth Book', iCompany.mMorningstarFinancialsGrowthBook, 'kGrowth', lambda v : v >= 0 )
	AddTR( iSoup, tbody, 'EPS', iCompany.mMorningstarFinancialsEarnings, 'kNone', None )
	AddTR( iSoup, tbody, 'Growth EPS', iCompany.mMorningstarGrowthEarnings, 'kGrowth', lambda v : v >= 0 )
	AddTR( iSoup, tbody, 'Dividends', iCompany.mMorningstarFinancialsDividends, 'kNone', None )
	AddTR( iSoup, tbody, 'GrowthDividends', iCompany.mMorningstarFinancialsGrowthDividends, 'kGrowth', lambda v : v >= 0 )
	
	#---
	
	AddTR( iSoup, tbody, '', iCompany.mMorningstarProfitabilityYears, 'kNone', None, iHeader=True )
	#TODO: see what is it ? not corresponding to zonebourse
	AddTR( iSoup, tbody, 'Payout Ratio (<60)', iCompany.mMorningstarFinancialsPayoutRatio, 'kThreshold', lambda v : 1 if v <= 60 else 0 if v <= 70 else -1 )
	AddTR( iSoup, tbody, 'ROE (>15)', iCompany.mMorningstarProfitabilityROE, 'kThreshold', lambda v : 1 if v >= 15 else 0 if v >= 8 else -1 )
	AddTR( iSoup, tbody, 'ROI (>15)', iCompany.mMorningstarProfitabilityROI, 'kThreshold', lambda v : 1 if v >= 15 else 0 if v >= 8 else -1 )
	AddTR( iSoup, tbody, 'Interest Cover (>3)', iCompany.mMorningstarProfitabilityIC, 'kThreshold', lambda v : 1 if v >= 3 else -1 )
	AddTR( iSoup, tbody, 'FCF/Sales (>5)', iCompany.mMorningstarCashFlowFCFOnSales, 'kThreshold', lambda v : 1 if v >= 5 else -1 )
	
	#---
	
	AddTR( iSoup, tbody, '', iCompany.mMorningstarHealthYears, 'kNone', None, iHeader=True )
	AddTR( iSoup, tbody, 'Current Ratio (>1.5)', iCompany.mMorningstarHealthCurrentRatio, 'kThreshold', lambda v : 1 if v >= 1.5 else 0 if v >= 1 else -1 )
	AddTR( iSoup, tbody, 'Debt/Equity (<1)', iCompany.mMorningstarHealthDebtOnEquity, 'kThreshold', lambda v : 1 if v < 1 else -1 )
	
	#---
	
	AddTR( iSoup, tbody, '', iCompany.mMorningstarValuationYears, 'kNone', None, iHeader=True )
	AddTR( iSoup, tbody, 'PER (3<<15)', iCompany.mMorningstarValuationPER, 'kThreshold', lambda v : 1 if v >=3 and v <= 12 else 0 if v >=12 and v <= 18 else -1 )
	AddTR( iSoup, tbody, 'Price/Book (<4)', iCompany.mMorningstarValuationP2B, 'kThreshold', lambda v : 1 if v <= 4 else 0 if v <= 5 else -1 )
	AddTR( iSoup, tbody, 'Price/Sales (<2)', iCompany.mMorningstarValuationP2S, 'kThreshold', lambda v : 1 if v <= 2 else 0 if v <= 4 else -1 )
	AddTR( iSoup, tbody, 'Price/CashFlow (<8)', iCompany.mMorningstarValuationP2CF, 'kThreshold', lambda v : 1 if v <= 8 else 0 if v <= 12 else -1 )
	AddTR( iSoup, tbody, 'EV/EBITDA (<8)', iCompany.mMorningstarValuationEVOnEBITDA, 'kThreshold', lambda v : 1 if v <= 5 else 0 if v <= 8 else -1 )
	
	#---
	
	table = iSoup.new_tag( 'table' )
	table.append( tbody )
	
	div_data.append( table )
	
	return div_data;

