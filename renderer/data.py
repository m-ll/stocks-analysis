#!/usr/bin/env python3

import copy
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

def HarmonizeData( iData, iReferences ):
	max_data = 0
	max_data_estimated = 0
	for ref in iReferences:
		max_data = max( max_data, len( ref.mData ) )
		max_data_estimated = max( max_data_estimated, len( ref.mDataEstimated ) )
		
	data = copy.copy( iData )
	
	diff = max_data - len( data.mData )
	if diff > 0:
		data.mData = [''] * diff + data.mData
		
	diff = max_data_estimated - len( data.mDataEstimated )
	if diff > 0:
		data.mDataEstimated = data.mDataEstimated + [''] * diff
		
	return data

def AddTR( iSoup, iText, iData, iReferences, iCSSFunction=None, iCSSFunction2=None, iHeader=False, iUrl='' ):
	data = HarmonizeData( iData, iReferences )
	
	tr = iSoup.new_tag( 'tr' )
	
	#---
	
	td = iSoup.new_tag( 'th' )
	if not iUrl:
		td.string = iText
	else:
		a = iSoup.new_tag( 'a', href=iUrl )
		a.append( iText )
		td.append( a )
	tr.append( td )
	
	#---
	
	for v in data.mData:
		td = iSoup.new_tag( 'th' if iHeader else 'td' )
		td['class'] = GetCSS( v, iCSSFunction )
		td.string = v
		tr.append( td )
	
	#---
	
	td = iSoup.new_tag( 'th' if iHeader else 'td' )
	if data.mTTM:
		td['class'] = GetCSS( data.mTTM, iCSSFunction )
		if iCSSFunction2 is not None:	#PATCH: to colorize yield without PS/Impots with another lambda
			td['class'] = GetCSS( data.mTTM, iCSSFunction2 )
		td.string = f'{data.mTTM}'
	tr.append( td )
	
	#---
		
	for v in data.mDataEstimated:
		td = iSoup.new_tag( 'th' if iHeader else 'td' )
		td['class'] = GetCSS( v, iCSSFunction )
		td.string = v
		tr.append( td )
	
	#---
	
	td = iSoup.new_tag( 'th' if iHeader else 'td' )
	td['class'] = GetCSS( data.mGrowthAverage, iCSSFunction )
	td.string = f'{data.mGrowthAverage}'
	tr.append( td )
	
	#---
	
	td = iSoup.new_tag( 'th' )
	if not iUrl:
		td.string = iText
	else:
		a = iSoup.new_tag( 'a', href=iUrl )
		a.append( iText )
		td.append( a )
	tr.append( td )
	
	#---
	
	return tr
	
def Data( iCompany, iSoup ):
	root = iSoup.new_tag( 'div' )
	root['class'] = 'fondamentals'
	
	if not iCompany.mMorningstar.Region():				#TODO: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		return root
		
	references = [ iCompany.mMorningstar.mISYears, 
					iCompany.mMorningstar.mFinancialsYears, 
					iCompany.mMorningstar.mGrowthYears,
					iCompany.mMorningstar.mProfitabilityYears, 
					iCompany.mMorningstar.mHealthYears, 
					iCompany.mMorningstar.mValuationYears,
					iCompany.mZoneBourse.mYears ]
	
	#---
	
	tbody = iSoup.new_tag( 'tbody' )
	
	tr = AddTR( iSoup, '', iCompany.mMorningstar.mISYears, references, iHeader=True )
	tbody.append( tr )
	tr = AddTR( iSoup, 'EBITDA', iCompany.mMorningstar.mEBITDA, references, iUrl=iCompany.mMorningstar.UrlIncomeStatement() )
	tbody.append( tr )
	
	# tr = AddTR( iSoup, '', iCompany.mMorningstar.mBSYears, references, iHeader=True )
	# tbody.append( tr )
	tr = AddTR( iSoup, 'LongTerm Debt', iCompany.mMorningstar.mLongTermDebt, references, iUrl=iCompany.mMorningstar.UrlBalanceSheet() )
	tbody.append( tr )
	tr = AddTR( iSoup, 'LT-Debt/EBITDA (<5)', iCompany.mMorningstar.mLTDOnEBITDA, references, lambda v : 1 if v < 5.0 else -1 )
	tbody.append( tr )
	
	table = iSoup.new_tag( 'table' )
	table.append( tbody )
	
	root.append( table )
	
	#---
	
	tbody = iSoup.new_tag( 'tbody' )
	
	tr = AddTR( iSoup, '', iCompany.mMorningstar.mFinancialsYears, references, iHeader=True )
	tbody.append( tr )
	tr = AddTR( iSoup, '', iCompany.mZoneBourse.mYears, references, iHeader=True )
	tbody.append( tr )
	# tr = AddTR( iSoup, '', iCompany.mMorningstar.mGrowthYears, references, iHeader=True )
	# tbody.append( tr )
	tr = AddTR( iSoup, 'Revenue', iCompany.mZoneBourse.mRevenue, references )
	tbody.append( tr )
	tr = AddTR( iSoup, 'Growth Revenue (%)', iCompany.mZoneBourse.mGrowthRevenue, references, lambda v : 0 if math.isclose( v, 0.0 ) else 1 if v > 0 else -1 )
	tbody.append( tr )
	tr = AddTR( iSoup, 'Revenue', iCompany.mMorningstar.mFinancialsRevenue, references, iUrl=iCompany.mMorningstar.UrlRatios() )
	tbody.append( tr )
	tr = AddTR( iSoup, 'Growth Revenue (%)', iCompany.mMorningstar.mGrowthRevenue, references, lambda v : 0 if math.isclose( v, 0.0 ) else 1 if v > 0 else -1 )
	tbody.append( tr )
	
	tr = AddTR( iSoup, 'Net Income', iCompany.mZoneBourse.mNetIncome, references )
	tr['class'] = 'separator'
	tbody.append( tr )
	tr = AddTR( iSoup, 'Growth Net Income (%)', iCompany.mZoneBourse.mGrowthNetIncome, references, lambda v : 0 if math.isclose( v, 0.0 ) else 1 if v > 0 else -1 )
	tbody.append( tr )
	tr = AddTR( iSoup, 'Net Income', iCompany.mMorningstar.mFinancialsNetIncome, references )
	tbody.append( tr )
	tr = AddTR( iSoup, 'Growth Net Income (%)', iCompany.mMorningstar.mGrowthNetIncome, references, lambda v : 0 if math.isclose( v, 0.0 ) else 1 if v > 0 else -1 )
	tbody.append( tr )
	
	tr = AddTR( iSoup, 'Book', iCompany.mMorningstar.mFinancialsBook, references )
	tr['class'] = tr.get( 'class', [] ) + ['less-important', 'separator']
	tbody.append( tr )
	tr = AddTR( iSoup, 'Growth Book (%)', iCompany.mMorningstar.mFinancialsGrowthBook, references, lambda v : 0 if math.isclose( v, 0.0 ) else 1 if v > 0 else -1 )
	tr['class'] = tr.get( 'class', [] ) + ['less-important']
	tbody.append( tr )
	
	tr = AddTR( iSoup, 'EPS', iCompany.mZoneBourse.mEarnings, references )
	tr['class'] = 'separator'
	tbody.append( tr )
	tr = AddTR( iSoup, 'Growth EPS (%)', iCompany.mZoneBourse.mGrowthEarnings, references, lambda v : 0 if math.isclose( v, 0.0 ) else 1 if v > 0 else -1 )
	tbody.append( tr )
	tr = AddTR( iSoup, 'EPS', iCompany.mMorningstar.mFinancialsEarnings, references )
	tbody.append( tr )
	tr = AddTR( iSoup, 'Growth EPS (%)', iCompany.mMorningstar.mGrowthEarnings, references, lambda v : 0 if math.isclose( v, 0.0 ) else 1 if v > 0 else -1 )
	tbody.append( tr )
	
	tr = AddTR( iSoup, 'Dividends', iCompany.mZoneBourse.mDividends, references )
	tr['class'] = 'separator'
	tbody.append( tr )
	tr = AddTR( iSoup, 'Growth Dividends (%)', iCompany.mZoneBourse.mGrowthDividends, references, lambda v : 0 if math.isclose( v, 0.0 ) else 1 if v > 0 else -1 )
	tbody.append( tr )
	tr = AddTR( iSoup, 'Dividends', iCompany.mMorningstar.mFinancialsDividends, references )
	tbody.append( tr )
	tr = AddTR( iSoup, 'Growth Dividends (%)', iCompany.mMorningstar.mFinancialsGrowthDividends, references, lambda v : 0 if math.isclose( v, 0.0 ) else 1 if v > 0 else -1 )
	tbody.append( tr )
	
	#---
	
	tr = AddTR( iSoup, '', iCompany.mMorningstar.mProfitabilityYears, references, iHeader=True )
	tbody.append( tr )
	#TODO: see what is it ? not corresponding to zonebourse
	tr = AddTR( iSoup, 'Payout Ratio (<60)', iCompany.mMorningstar.mFinancialsPayoutRatio, references, lambda v : 1 if v <= 60.0 else 0 if v <= 70.0 else -1 )
	tbody.append( tr )
	tr = AddTR( iSoup, 'ROE (>15)', iCompany.mMorningstar.mProfitabilityROE, references, lambda v : 1 if v >= 15.0 else 0 if v >= 8.0 else -1 )
	tbody.append( tr )
	tr = AddTR( iSoup, 'ROI (>15)', iCompany.mMorningstar.mProfitabilityROI, references, lambda v : 1 if v >= 15.0 else 0 if v >= 8.0 else -1 )
	tr['class'] = tr.get( 'class', [] ) + ['less-important']
	tbody.append( tr )
	tr = AddTR( iSoup, 'Interest Cover (>3)', iCompany.mMorningstar.mProfitabilityIC, references, lambda v : 1 if v >= 3.0 else -1 )
	tr['class'] = tr.get( 'class', [] ) + ['less-important']
	tbody.append( tr )
	tr = AddTR( iSoup, 'FCF/Sales (>5)', iCompany.mMorningstar.mCashFlowFCFOnSales, references, lambda v : 1 if v >= 5.0 else -1 )
	tbody.append( tr )
	
	#---
	
	tr = AddTR( iSoup, '', iCompany.mMorningstar.mHealthYears, references, iHeader=True )
	tbody.append( tr )
	tr = AddTR( iSoup, 'Current Ratio (>1.5)', iCompany.mMorningstar.mHealthCurrentRatio, references, lambda v : 1 if v >= 1.5 else 0 if v >= 1.0 else -1 )
	tbody.append( tr )
	tr = AddTR( iSoup, 'Debt/Equity (<1)', iCompany.mMorningstar.mHealthDebtOnEquity, references, lambda v : 1 if v < 1.0 else -1 )
	tbody.append( tr )
	
	table = iSoup.new_tag( 'table' )
	table.append( tbody )
	
	root.append( table )
	
	#---
	
	tbody = iSoup.new_tag( 'tbody' )
	
	tr = AddTR( iSoup, '', iCompany.mMorningstar.mValuationYears, references, iHeader=True )
	tbody.append( tr )
	tr = AddTR( iSoup, 'PER (3<.<15)', iCompany.mMorningstar.mValuationPER, references, lambda v : 1 if v >=3.0 and v <= 12.0 else 0 if v >= 12.0 and v <= 18.0 else -1, iUrl=iCompany.mMorningstar.UrlValuation() )
	tbody.append( tr )
	tr = AddTR( iSoup, 'Price/Book (<4)', iCompany.mMorningstar.mValuationP2B, references, lambda v : 1 if v <= 4.0 else 0 if v <= 5.0 else -1 )
	tbody.append( tr )
	tr = AddTR( iSoup, 'Price/Sales (<2)', iCompany.mMorningstar.mValuationP2S, references, lambda v : 1 if v <= 2.0 else 0 if v <= 4.0 else -1 )
	tr['class'] = tr.get( 'class', [] ) + ['less-important']
	tbody.append( tr )
	tr = AddTR( iSoup, 'Price/CashFlow (<8)', iCompany.mMorningstar.mValuationP2CF, references, lambda v : 1 if v <= 8.0 else 0 if v <= 12.0 else -1 )
	tr['class'] = tr.get( 'class', [] ) + ['less-important']
	tbody.append( tr )
	tr = AddTR( iSoup, 'EV/EBITDA (<8)', iCompany.mMorningstar.mValuationEVOnEBITDA, references, lambda v : 1 if v <= 5.0 else 0 if v <= 8.0 else -1 )
	tr['class'] = tr.get( 'class', [] ) + ['less-important']
	tbody.append( tr )
	
	table = iSoup.new_tag( 'table' )
	table.append( tbody )
	
	root.append( table )
	
	#---
	
	tbody = iSoup.new_tag( 'tbody' )
	
	tr = AddTR( iSoup, '', iCompany.mZoneBourse.mYears, references, iHeader=True )
	tbody.append( tr )
	tr = AddTR( iSoup, 'Dividend Yield (ZB)', iCompany.mZoneBourse.mYields, references )
	tbody.append( tr )
	tr = AddTR( iSoup, 'Dividend Yield (MS)', iCompany.mMorningstar.mFinancialsDividendsYield, references, lambda v : 1 if v >= 4.3 else 0 if v >= 3.6 else -1 )
	tbody.append( tr )
	
	data = copy.copy( iCompany.mMorningstar.mFinancialsDividendsYield10Years )
	data.mTTM = iCompany.mMorningstar.mFinancialsGrowthDividends.mGrowthAverage
	data.mDataEstimated = [ iCompany.mZoneBourse.mGrowthDividends.mGrowthAverage ]
	tr = AddTR( iSoup, 'Growth Dividends (%)', data, references )
	tr['class'] = tr.get( 'class', [] ) + ['less-important']
	tbody.append( tr )
	
	data = copy.copy( iCompany.mMorningstar.mFinancialsDividendsYield10Years )
	data.mDataEstimated = [ iCompany.mZoneBourse.mDividendsYield10Years.mGrowthAverage ]
	tr = AddTR( iSoup, 'Dividends after 10Y', data, references, iUrl=iCompany.mMorningstar.mUrlDividendCalculator10Years )
	tbody.append( tr )
	
	data = copy.copy( iCompany.mMorningstar.mFinancialsDividendsYield20Years )
	data.mDataEstimated = [ iCompany.mZoneBourse.mDividendsYield20Years.mGrowthAverage ]
	tr = AddTR( iSoup, 'Dividends after 20Y ', data, references, iUrl=iCompany.mMorningstar.mUrlDividendCalculator20Years )
	tbody.append( tr )
	
	table = iSoup.new_tag( 'table' )
	table.append( tbody )
	
	root.append( table )
	
	return root
	
def CreateRow( iSoup, iLabel, iUrl, iData, iHeader=False ):
	tr = iSoup.new_tag( 'tr' )
	
	th = iSoup.new_tag( 'th' )
	a = iSoup.new_tag( 'a', href=iUrl )
	a.append( iLabel )
	th.append( a )
	tr.append( th )
	td = iSoup.new_tag( 'th' if iHeader else 'td' )
	td.string = iData['-5'] if '-5' in iData else ''
	td.string = td.string.replace( '%', '' ) + '%' if td.string else ''
	tr.append( td )
	td = iSoup.new_tag( 'th' if iHeader else 'td' )
	td.string = iData['-3'] if '-3' in iData else ''
	td.string = td.string.replace( '%', '' ) + '%' if td.string else ''
	tr.append( td )
	td = iSoup.new_tag( 'th' if iHeader else 'td' )
	td.string = iData['-1'] if '-1' in iData else ''
	td.string = td.string.replace( '%', '' ) + '%' if td.string else ''
	tr.append( td )
	td = iSoup.new_tag( 'th' if iHeader else 'td' )
	td.string = iData['0'] if '0' in iData else ''
	td.string = td.string.replace( '%', '' ) + '%' if td.string else ''
	tr.append( td )
	td = iSoup.new_tag( 'th' if iHeader else 'td' )
	td.string = iData['+1'] if '+1' in iData else ''
	td.string = td.string.replace( '%', '' ) + '%' if td.string else ''
	tr.append( td )
	td = iSoup.new_tag( 'th' if iHeader else 'td' )
	td.string = iData['+5'] if '+5' in iData else ''
	td.string = td.string.replace( '%', '' ) + '%' if td.string else ''
	tr.append( td )
	
	return tr

def DataGrowth( iCompany, iSoup ):
	root = iSoup.new_tag( 'div' )
	root['class'] = 'growth'
	
	tbody = iSoup.new_tag( 'tbody' )
	
	tr = CreateRow( iSoup, '', '', { '-5': '-5', '-3': '-3', '-1': '-1', '0': '0', '+1': '+1', '+5': '+5' }, iHeader=True )
	tbody.append( tr )
	
	tr = CreateRow( iSoup, 'Growth (YahooFinance)', iCompany.mYahooFinance.Url(), iCompany.mYahooFinance.mGrowth )
	tbody.append( tr )
	
	tr = CreateRow( iSoup, 'Growth (Finviz)', iCompany.mFinviz.Url(), iCompany.mFinviz.mBNAGrowth )
	tbody.append( tr )
	
	tr = CreateRow( iSoup, 'Growth (Reuters)', iCompany.mReuters.Url(), iCompany.mReuters.mBNAGrowth )
	tbody.append( tr )
	
	table = iSoup.new_tag( 'table' )
	table.append( tbody )
	root.append( table )
	
	return root