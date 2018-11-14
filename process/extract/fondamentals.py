#!/usr/bin/python3

import math

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

def AddTR( iSoup, iSBody, iText, iData, iCSSFunction=None, iCSSFunction2=None, iHeader=False, iUrl='' ):
	if iData is None:
		return
	
	tr = iSoup.new_tag( 'tr' )
	
	td = iSoup.new_tag( 'th' )
	if not iUrl:
		td.string = iText
	else:
		a = iSoup.new_tag( 'a', href=iUrl )
		a.append( iText )
		td.append( a )
	tr.append( td )
	
	data = iData.mData
	if not data and iData.mParent:
		data = [''] * len( iData.mParent.mData )
	
	for i, v in enumerate( data ):
		td = iSoup.new_tag( 'th' if iHeader else 'td' )
		td['class'] = GetCSS( v, iCSSFunction )
		td.string = v
		tr.append( td )
		
	td = iSoup.new_tag( 'th' if iHeader else 'td' )
	td['class'] = GetCSS( iData.mGrowthAverage, iCSSFunction )
	td.string = str( iData.mGrowthAverage )
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
	
	if iData.mCurrent or iData.m5Years or iData.mIndex:
		td = iSoup.new_tag( 'th' if iHeader else 'td' )
		td['class'] = [ GetCSS( iData.mCurrent, iCSSFunction ), 'left-space' ]
		if iCSSFunction2 is not None:	#PATCH: to colorize yield without PS/Impots with another lambda
			td['class'] = [ GetCSS( iData.mCurrent, iCSSFunction2 ), 'left-space' ]
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
	
	if not iCompany.mMorningstar.Region():
		return div_data
	
	#---
	
	tbody = iSoup.new_tag( 'tbody' )
	
	AddTR( iSoup, tbody, '', iCompany.mMorningstarISYears, iHeader=True )
	AddTR( iSoup, tbody, 'EBITDA', iCompany.mMorningstarEBITDA, iUrl=iCompany.mMorningstar.UrlIncomeStatement() )
	
	# AddTR( iSoup, tbody, '', iCompany.mMorningstarBSYears, iHeader=True )
	AddTR( iSoup, tbody, 'LongTerm Debt', iCompany.mMorningstarLongTermDebt, iUrl=iCompany.mMorningstar.UrlBalanceSheet() )
	AddTR( iSoup, tbody, 'LT-Debt/EBITDA (<5)', iCompany.mMorningstarLTDOnEBITDA, lambda v : 1 if v < 5.0 else -1 )
	
	table = iSoup.new_tag( 'table' )
	table.append( tbody )
	
	div_data.append( table )
	
	#---
	
	tbody = iSoup.new_tag( 'tbody' )
	
	AddTR( iSoup, tbody, '', iCompany.mMorningstarFinancialsYears, iHeader=True )
	# AddTR( iSoup, tbody, '', iCompany.mMorningstarGrowthYears, iHeader=True )
	AddTR( iSoup, tbody, 'Revenue', iCompany.mMorningstarFinancialsRevenue, iUrl=iCompany.mMorningstar.UrlRatios() )
	AddTR( iSoup, tbody, 'Growth Revenue (%)', iCompany.mMorningstarGrowthRevenue, lambda v : 0 if math.isclose( v, 0.0 ) else 1 if v > 0 else -1 )
	AddTR( iSoup, tbody, 'Net Income', iCompany.mMorningstarFinancialsNetIncome )
	AddTR( iSoup, tbody, 'Growth Net Income (%)', iCompany.mMorningstarGrowthNetIncome, lambda v : 0 if math.isclose( v, 0.0 ) else 1 if v > 0 else -1 )
	AddTR( iSoup, tbody, 'Book', iCompany.mMorningstarFinancialsBook )
	AddTR( iSoup, tbody, 'Growth Book (%)', iCompany.mMorningstarFinancialsGrowthBook, lambda v : 0 if math.isclose( v, 0.0 ) else 1 if v > 0 else -1 )
	AddTR( iSoup, tbody, 'EPS', iCompany.mMorningstarFinancialsEarnings )
	AddTR( iSoup, tbody, 'Growth EPS (%)', iCompany.mMorningstarGrowthEarnings, lambda v : 0 if math.isclose( v, 0.0 ) else 1 if v > 0 else -1 )
	AddTR( iSoup, tbody, 'Dividends', iCompany.mMorningstarFinancialsDividends )
	AddTR( iSoup, tbody, 'GrowthDividends (%)', iCompany.mMorningstarFinancialsGrowthDividends, lambda v : 0 if math.isclose( v, 0.0 ) else 1 if v > 0 else -1 )
	
	#---
	
	AddTR( iSoup, tbody, '', iCompany.mMorningstarProfitabilityYears, iHeader=True )
	#TODO: see what is it ? not corresponding to zonebourse
	AddTR( iSoup, tbody, 'Payout Ratio (<60)', iCompany.mMorningstarFinancialsPayoutRatio, lambda v : 1 if v <= 60.0 else 0 if v <= 70.0 else -1 )
	AddTR( iSoup, tbody, 'ROE (>15)', iCompany.mMorningstarProfitabilityROE, lambda v : 1 if v >= 15.0 else 0 if v >= 8.0 else -1 )
	AddTR( iSoup, tbody, 'ROI (>15)', iCompany.mMorningstarProfitabilityROI, lambda v : 1 if v >= 15.0 else 0 if v >= 8.0 else -1 )
	AddTR( iSoup, tbody, 'Interest Cover (>3)', iCompany.mMorningstarProfitabilityIC, lambda v : 1 if v >= 3.0 else -1 )
	AddTR( iSoup, tbody, 'FCF/Sales (>5)', iCompany.mMorningstarCashFlowFCFOnSales, lambda v : 1 if v >= 5.0 else -1 )
	
	#---
	
	AddTR( iSoup, tbody, '', iCompany.mMorningstarHealthYears, iHeader=True )
	AddTR( iSoup, tbody, 'Current Ratio (>1.5)', iCompany.mMorningstarHealthCurrentRatio, lambda v : 1 if v >= 1.5 else 0 if v >= 1.0 else -1 )
	AddTR( iSoup, tbody, 'Debt/Equity (<1)', iCompany.mMorningstarHealthDebtOnEquity, lambda v : 1 if v < 1.0 else -1 )
	
	table = iSoup.new_tag( 'table' )
	table.append( tbody )
	
	div_data.append( table )
	
	#---
	
	tbody = iSoup.new_tag( 'tbody' )
	
	AddTR( iSoup, tbody, '', iCompany.mMorningstarValuationYears, iHeader=True )
	AddTR( iSoup, tbody, 'PER (3<.<15)', iCompany.mMorningstarValuationPER, lambda v : 1 if v >=3.0 and v <= 12.0 else 0 if v >= 12.0 and v <= 18.0 else -1, iUrl=iCompany.mMorningstar.UrlValuation() )
	AddTR( iSoup, tbody, 'Price/Book (<4)', iCompany.mMorningstarValuationP2B, lambda v : 1 if v <= 4.0 else 0 if v <= 5.0 else -1 )
	AddTR( iSoup, tbody, 'Price/Sales (<2)', iCompany.mMorningstarValuationP2S, lambda v : 1 if v <= 2.0 else 0 if v <= 4.0 else -1 )
	AddTR( iSoup, tbody, 'Price/CashFlow (<8)', iCompany.mMorningstarValuationP2CF, lambda v : 1 if v <= 8.0 else 0 if v <= 12.0 else -1 )
	AddTR( iSoup, tbody, 'EV/EBITDA (<8)', iCompany.mMorningstarValuationEVOnEBITDA, lambda v : 1 if v <= 5.0 else 0 if v <= 8.0 else -1 )
	
	AddTR( iSoup, tbody, 'Dividend Yield', iCompany.mMorningstarFinancialsDividendsYield, lambda v : 1 if v >= 4.2 else 0 if v >= 3.5 else -1, iCSSFunction2=lambda v : 1 if v >= 3.0 else 0 if v >= 2.5 else -1 )
	AddTR( iSoup, tbody, 'Dividends after 10Y', iCompany.mMorningstarFinancialsDividendsYield10Years, iUrl=iCompany.mUrlMorningstarDividendCalculator10Years )
	AddTR( iSoup, tbody, 'Dividends after 20Y ', iCompany.mMorningstarFinancialsDividendsYield20Years, iUrl=iCompany.mUrlMorningstarDividendCalculator20Years )
	
	table = iSoup.new_tag( 'table' )
	table.append( tbody )
	
	div_data.append( table )
	
	return div_data;

