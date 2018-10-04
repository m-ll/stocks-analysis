#!/usr/bin/python3

import time
import copy
import requests
from bs4 import BeautifulSoup

from ..company import *

#---

def GetCSS( iString, iCSSFunction ):
	if not iString:
		return ''
	if iCSSFunction is None:
		return ''
		
	v = float( iString )
	if iCSSFunction( v ) == 1:
		return 'plus'
	elif iCSSFunction( v ) == 0:
		return 'bof'
	elif iCSSFunction( v ) == -1:
		return 'minus'
	
	return ''

def AddTR( iSoup, iSBody, iText, iData, iCSSFunction=None, iHeader=False ):
	if iData is None:
		return
	
	td = iSoup.new_tag( 'th' )
	td.string = iText
	tr = iSoup.new_tag( 'tr' )
	tr.append( td )
	
	for i, v in enumerate( iData.mData ):
		td = iSoup.new_tag( 'th' if iHeader else 'td' )
		td['class'] = GetCSS( v, iCSSFunction )
		td.string = v
		tr.append( td )
		
	if iData.mTTM or iData.mLatestQuarter:
		td = iSoup.new_tag( 'th' if iHeader else 'td' )
		td['class'] = [ GetCSS( iData.mTTM, iCSSFunction ), 'left-space' ]
		td.string = str( iData.mTTM )
		tr.append( td )
		
		td = iSoup.new_tag( 'th' if iHeader else 'td' )
		td['class'] = GetCSS( iData.mLatestQuarter, iCSSFunction )
		td.string = str( iData.mLatestQuarter )
		tr.append( td )
	else:
		td = iSoup.new_tag( 'th' if iHeader else 'td' )
		td['class'] = [ GetCSS( iData.mCurrent, iCSSFunction ), 'left-space' ]
		td.string = str( iData.mCurrent )
		tr.append( td )
		
		td = iSoup.new_tag( 'th' if iHeader else 'td' )
		td['class'] = GetCSS( iData.m5Years, iCSSFunction )
		td.string = str( iData.m5Years )
		tr.append( td )
		
		td = iSoup.new_tag( 'th' if iHeader else 'td' )
		td['class'] = GetCSS( iData.mIndex, iCSSFunction )
		td.string = str( iData.mIndex )
		tr.append( td )
	
	iSBody.append( tr )

def Extract( iCompany, iSoup ):
	div_data = iSoup.new_tag( 'div' )
	div_data['class'] = 'clear fondamentals'
	
	if not iCompany.mMorningstarRegion:
		return div_data
	
	#---
	
	tbody = iSoup.new_tag( 'tbody' )
	
	AddTR( iSoup, tbody, '', iCompany.mMorningstarISYears, iHeader=True )
	AddTR( iSoup, tbody, 'EBITDA', iCompany.mMorningstarEBITDA )
	
	# AddTR( iSoup, tbody, '', iCompany.mMorningstarBSYears, iHeader=True )
	AddTR( iSoup, tbody, 'LongTerm Debt', iCompany.mMorningstarLongTermDebt )
	AddTR( iSoup, tbody, 'LT-Debt/EBITDA (<5)', iCompany.mMorningstarLTDOnEBITDA, lambda v : 1 if v < 5 else -1 )
	
	table = iSoup.new_tag( 'table' )
	table.append( tbody )
	
	div_data.append( table )
	
	#---
	
	tbody = iSoup.new_tag( 'tbody' )
	
	AddTR( iSoup, tbody, '', iCompany.mMorningstarFinancialsYears, iHeader=True )
	# AddTR( iSoup, tbody, '', iCompany.mMorningstarGrowthYears, iHeader=True )
	AddTR( iSoup, tbody, 'Revenue', iCompany.mMorningstarFinancialsRevenue )
	AddTR( iSoup, tbody, 'Growth Revenue (%)', iCompany.mMorningstarGrowthRevenue, lambda v : 1 if v >= 0 else -1 )
	AddTR( iSoup, tbody, 'Net Income', iCompany.mMorningstarFinancialsNetIncome )
	AddTR( iSoup, tbody, 'Growth Net Income (%)', iCompany.mMorningstarGrowthNetIncome, lambda v : 1 if v >= 0 else -1 )
	AddTR( iSoup, tbody, 'Book', iCompany.mMorningstarFinancialsBook )
	AddTR( iSoup, tbody, 'Growth Book (%)', iCompany.mMorningstarFinancialsGrowthBook, lambda v : 1 if v >= 0 else -1 )
	AddTR( iSoup, tbody, 'EPS', iCompany.mMorningstarFinancialsEarnings )
	AddTR( iSoup, tbody, 'Growth EPS (%)', iCompany.mMorningstarGrowthEarnings, lambda v : 1 if v >= 0 else -1 )
	AddTR( iSoup, tbody, 'Dividends', iCompany.mMorningstarFinancialsDividends )
	AddTR( iSoup, tbody, 'GrowthDividends (%)', iCompany.mMorningstarFinancialsGrowthDividends, lambda v : 1 if v >= 0 else -1 )
	
	#---
	
	AddTR( iSoup, tbody, '', iCompany.mMorningstarProfitabilityYears, iHeader=True )
	#TODO: see what is it ? not corresponding to zonebourse
	AddTR( iSoup, tbody, 'Payout Ratio (<60)', iCompany.mMorningstarFinancialsPayoutRatio, lambda v : 1 if v <= 60 else 0 if v <= 70 else -1 )
	AddTR( iSoup, tbody, 'ROE (>15)', iCompany.mMorningstarProfitabilityROE, lambda v : 1 if v >= 15 else 0 if v >= 8 else -1 )
	AddTR( iSoup, tbody, 'ROI (>15)', iCompany.mMorningstarProfitabilityROI, lambda v : 1 if v >= 15 else 0 if v >= 8 else -1 )
	AddTR( iSoup, tbody, 'Interest Cover (>3)', iCompany.mMorningstarProfitabilityIC, lambda v : 1 if v >= 3 else -1 )
	AddTR( iSoup, tbody, 'FCF/Sales (>5)', iCompany.mMorningstarCashFlowFCFOnSales, lambda v : 1 if v >= 5 else -1 )
	
	#---
	
	AddTR( iSoup, tbody, '', iCompany.mMorningstarHealthYears, iHeader=True )
	AddTR( iSoup, tbody, 'Current Ratio (>1.5)', iCompany.mMorningstarHealthCurrentRatio, lambda v : 1 if v >= 1.5 else 0 if v >= 1 else -1 )
	AddTR( iSoup, tbody, 'Debt/Equity (<1)', iCompany.mMorningstarHealthDebtOnEquity, lambda v : 1 if v < 1 else -1 )
	
	table = iSoup.new_tag( 'table' )
	table.append( tbody )
	
	div_data.append( table )
	
	#---
	
	tbody = iSoup.new_tag( 'tbody' )
	
	AddTR( iSoup, tbody, '', iCompany.mMorningstarValuationYears, iHeader=True )
	AddTR( iSoup, tbody, 'PER (3<.<15)', iCompany.mMorningstarValuationPER, lambda v : 1 if v >=3 and v <= 12 else 0 if v >=12 and v <= 18 else -1 )
	AddTR( iSoup, tbody, 'Price/Book (<4)', iCompany.mMorningstarValuationP2B, lambda v : 1 if v <= 4 else 0 if v <= 5 else -1 )
	AddTR( iSoup, tbody, 'Price/Sales (<2)', iCompany.mMorningstarValuationP2S, lambda v : 1 if v <= 2 else 0 if v <= 4 else -1 )
	AddTR( iSoup, tbody, 'Price/CashFlow (<8)', iCompany.mMorningstarValuationP2CF, lambda v : 1 if v <= 8 else 0 if v <= 12 else -1 )
	AddTR( iSoup, tbody, 'EV/EBITDA (<8)', iCompany.mMorningstarValuationEVOnEBITDA, lambda v : 1 if v <= 5 else 0 if v <= 8 else -1 )
	
	table = iSoup.new_tag( 'table' )
	table.append( tbody )
	
	div_data.append( table )
	
	return div_data;

