#!/usr/bin/env python3

import csv
import re
from datetime import date, datetime

from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style

import company.company

class cMorningstar:
	def __init__( self ):
		pass
	
	def Parse( self, iCompany ):
		print( '	Morningstar ...' )

		if not iCompany.mMorningstar.Region():
			print( Fore.CYAN + '	skipping ... (no id)' )
			return
		
		self._ParseIncomStatement( iCompany )
		self._ParseBalanceSheet( iCompany )
		self._ParseRatios( iCompany )
		self._ParseValuation( iCompany )
		self._ParseDividends( iCompany )
			
	#---
		
	def _ParseIncomStatement( self, iCompany ):
		print( '		- Income Statement ...' )

		with open( iCompany.DataPathFile( iCompany.mMorningstar.FileNameIncomeStatement() ), newline='' ) as csvfile:
			reader = csv.reader( csvfile )
			
			for row in reader:
				if len( row ) <= 1:
					continue
				
				if row[0].startswith( 'Fiscal year ends' ):
					iCompany.mMorningstar.mISYears = company.company.cDataMorningstar( row )
				elif row[0].startswith( 'EBITDA' ):
					iCompany.mMorningstar.mEBITDA = company.company.cDataMorningstar( row, iCompany.mMorningstar.mISYears )
		
		if iCompany.mMorningstar.mEBITDA is None:
			iCompany.mMorningstar.mEBITDA = company.company.cDataMorningstar()
			iCompany.mMorningstar.mEBITDA.mData = [''] * len( iCompany.mMorningstar.mISYears.mData )
		
	def _ParseBalanceSheet( self, iCompany ):
		print( '		- Balance Sheet ...' )

		with open( iCompany.DataPathFile( iCompany.mMorningstar.FileNameBalanceSheet() ), newline='' ) as csvfile:
			reader = csv.reader( csvfile )
			
			for row in reader:
				if len( row ) <= 1:
					continue
				
				if row[0].startswith( 'Fiscal year ends' ):
					iCompany.mMorningstar.mBSYears = company.company.cDataMorningstar( row )
				elif row[0].startswith( 'Total non-current liabilities' ):
					iCompany.mMorningstar.mLongTermDebt = company.company.cDataMorningstar( row, iCompany.mMorningstar.mBSYears )
				elif row[0].startswith( 'Total liabilities' ) and iCompany.mMorningstar.mLongTermDebt is None:	# CNP
					iCompany.mMorningstar.mLongTermDebt = company.company.cDataMorningstar( row, iCompany.mMorningstar.mBSYears )
		
		for i, ltd in enumerate( iCompany.mMorningstar.mLongTermDebt.mData ):
			ebitda = iCompany.mMorningstar.mEBITDA.mData[i]
			if not ltd or not ebitda:
				iCompany.mMorningstar.mLTDOnEBITDA.mData.append( '' )
				continue
			
			ratio = float( ltd ) / float( ebitda )
			iCompany.mMorningstar.mLTDOnEBITDA.mData.append( '{:.02f}'.format( ratio ) )
			iCompany.mMorningstar.mLTDOnEBITDA.Update()
			
	def _ParseRatios( self, iCompany ):
		print( '		- Ratios ...' )

		with open( iCompany.DataPathFile( iCompany.mMorningstar.FileNameRatios() ), newline='' ) as csvfile:
			reader = csv.reader( csvfile )
			
			for row in reader:
				if not row:
					continue
				
				if not row[0] and iCompany.mMorningstar.mFinancialsYears is None:		# 2 lines have the same format, and the first one is the wanted one
					iCompany.mMorningstar.mFinancialsYears = company.company.cDataMorningstar( row )
				elif row[0].startswith( 'Revenue' ) and row[0].endswith( 'Mil' ):
					iCompany.mMorningstar.mFinancialsRevenue = company.company.cDataMorningstar( row, iCompany.mMorningstar.mFinancialsYears )
				elif row[0].startswith( 'Net Income' ) and row[0].endswith( 'Mil' ):
					iCompany.mMorningstar.mFinancialsNetIncome = company.company.cDataMorningstar( row, iCompany.mMorningstar.mFinancialsYears )
				elif row[0].startswith( 'Dividends' ):
					iCompany.mMorningstar.mFinancialsDividends = company.company.cDataMorningstar( row, iCompany.mMorningstar.mFinancialsYears )
				elif row[0].startswith( 'Payout Ratio' ):
					iCompany.mMorningstar.mFinancialsPayoutRatio = company.company.cDataMorningstar( row, iCompany.mMorningstar.mFinancialsYears )
				elif row[0].startswith( 'Earnings' ):
					iCompany.mMorningstar.mFinancialsEarnings = company.company.cDataMorningstar( row, iCompany.mMorningstar.mFinancialsYears )
				elif row[0].startswith( 'Book Value Per Share' ):
					iCompany.mMorningstar.mFinancialsBook = company.company.cDataMorningstar( row, iCompany.mMorningstar.mFinancialsYears )
					
				elif row[0].startswith( 'Profitability' ):
					iCompany.mMorningstar.mProfitabilityYears = company.company.cDataMorningstar( row )
				elif row[0].startswith( 'Return on Equity' ):
					iCompany.mMorningstar.mProfitabilityROE = company.company.cDataMorningstar( row, iCompany.mMorningstar.mProfitabilityYears )
				elif row[0].startswith( 'Return on Invested Capital' ):
					iCompany.mMorningstar.mProfitabilityROI = company.company.cDataMorningstar( row, iCompany.mMorningstar.mProfitabilityYears )
				elif row[0].startswith( 'Interest Coverage' ):
					iCompany.mMorningstar.mProfitabilityIC = company.company.cDataMorningstar( row, iCompany.mMorningstar.mProfitabilityYears )
					
				elif row[0].startswith( 'Key Ratios -> Growth' ):
					row = next( reader )
					iCompany.mMorningstar.mGrowthYears = company.company.cDataMorningstar( row )
				elif row[0].startswith( 'Revenue %' ):
					row = next( reader )
					iCompany.mMorningstar.mGrowthRevenue = company.company.cDataMorningstar( row, iCompany.mMorningstar.mGrowthYears )	# YoY
				elif row[0].startswith( 'Net Income %' ):
					row = next( reader )
					iCompany.mMorningstar.mGrowthNetIncome = company.company.cDataMorningstar( row, iCompany.mMorningstar.mGrowthYears )	# YoY
				elif row[0].startswith( 'EPS %' ):
					row = next( reader )
					iCompany.mMorningstar.mGrowthEarnings = company.company.cDataMorningstar( row, iCompany.mMorningstar.mGrowthYears, iComputeGrowthAverage=True )	# YoY
					
				elif row[0].startswith( 'Free Cash Flow/Sales' ):
					iCompany.mMorningstar.mCashFlowFCFOnSales = company.company.cDataMorningstar( row, iCompany.mMorningstar.mProfitabilityYears )
			
				elif row[0].startswith( 'Liquidity/Financial Health' ):
					iCompany.mMorningstar.mHealthYears = company.company.cDataMorningstar( row )
				elif row[0].startswith( 'Current Ratio' ):
					iCompany.mMorningstar.mHealthCurrentRatio = company.company.cDataMorningstar( row, iCompany.mMorningstar.mHealthYears )
				elif row[0].startswith( 'Debt/Equity' ):
					iCompany.mMorningstar.mHealthDebtOnEquity = company.company.cDataMorningstar( row, iCompany.mMorningstar.mHealthYears )
				
		for i, dividend in enumerate( iCompany.mMorningstar.mFinancialsDividends.mData ):
			if not i:
				iCompany.mMorningstar.mFinancialsGrowthDividends.mData.append( '' )
				continue
			if not dividend or not iCompany.mMorningstar.mFinancialsDividends.mData[i-1]:
				iCompany.mMorningstar.mFinancialsGrowthDividends.mData.append( '' )
				continue
			
			previous_dividend = iCompany.mMorningstar.mFinancialsDividends.mData[i-1]
			ratio = ( float( dividend ) - float( previous_dividend ) ) / abs( float( previous_dividend ) )
			iCompany.mMorningstar.mFinancialsGrowthDividends.mData.append( '{:.02f}'.format( ratio * 100 ) )
			iCompany.mMorningstar.mFinancialsGrowthDividends.Update()
					
		for i, book in enumerate( iCompany.mMorningstar.mFinancialsBook.mData ):
			if not i:
				iCompany.mMorningstar.mFinancialsGrowthBook.mData.append( '' )
				continue
			if not book or not iCompany.mMorningstar.mFinancialsBook.mData[i-1]:
				iCompany.mMorningstar.mFinancialsGrowthBook.mData.append( '' )
				continue
			
			previous_book = iCompany.mMorningstar.mFinancialsBook.mData[i-1]
			ratio = ( float( book ) - float( previous_book ) ) / abs( float( previous_book ) )
			iCompany.mMorningstar.mFinancialsGrowthBook.mData.append( '{:.02f}'.format( ratio * 100 ) )
			iCompany.mMorningstar.mFinancialsGrowthBook.Update()
		
	def _ParseValuation( self, iCompany ):
		print( '		- Valuation ...' )

		html_content = ''
		with open( iCompany.DataPathFile( iCompany.mMorningstar.FileNameValuation() ), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		soup = BeautifulSoup( html_content, 'html5lib' )
		section = soup.find( 'a', attrs={'data-anchor': 'valuation'} ).parent		# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#the-keyword-arguments
		
		iCompany.mMorningstar.mValuationYears.SetTR( section, 'td', 'Calendar' )
			
		iCompany.mMorningstar.mValuationP2S.SetTR( section, 'span', 'Price/Sales' )
		iCompany.mMorningstar.mValuationPER.SetTR( section, 'span', 'Price/Earnings' )
		iCompany.mMorningstar.mValuationP2CF.SetTR( section, 'span', 'Price/Cash Flow' )
		iCompany.mMorningstar.mValuationP2B.SetTR( section, 'span', 'Price/Book' )
		iCompany.mMorningstar.mValuationEVOnEBITDA.SetTR( section, 'span', 'Enterprise Value/EBITDA' )
		
	def _ParseDividends( self, iCompany ):
		print( '		- Dividends ...' )

		html_content = ''
		with open( iCompany.DataPathFile( iCompany.mMorningstar.FileNameDividends() ), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		soup = BeautifulSoup( html_content, 'html5lib' )
		
		div = soup.find( id='sal-components-dividends' ).find( class_='dividend-yield' ).find_all( 'div' )[-1]
		s = div.string.replace( ',', '.' ).replace( '%', '' ).replace( '-', '' ).replace( '—', '' )
		iCompany.mMorningstar.mFinancialsDividendsYield.mGrowthAverage = s if s else '0'
		iCompany.mMorningstar.mFinancialsDividendsYield.mCurrent = '{:.02f}'.format( float( s ) * 0.7 ) if s else '0'	# Remove 30% for PS/Impots
		
		iCompany.mMorningstar.mUrlDividendCalculator10Years = iCompany.SourceUrlDividendCalculator( float( iCompany.mMorningstar.mFinancialsDividendsYield.mGrowthAverage ), float( iCompany.mMorningstar.mFinancialsGrowthDividends.mGrowthAverage ), 10 )
		annual_average = iCompany.AskDividendCalculatorProjection( iCompany.mMorningstar.mUrlDividendCalculator10Years )
		iCompany.mMorningstar.mFinancialsDividendsYield10Years.mGrowthAverage = annual_average
		iCompany.mMorningstar.mFinancialsDividendsYield10Years.mCurrent = '{:.02f}'.format( float( annual_average ) * 0.7 )	# Remove 30% for PS/Impots
		
		iCompany.mMorningstar.mUrlDividendCalculator20Years = iCompany.SourceUrlDividendCalculator( float( iCompany.mMorningstar.mFinancialsDividendsYield.mGrowthAverage ), float( iCompany.mMorningstar.mFinancialsGrowthDividends.mGrowthAverage ), 20 )
		annual_average = iCompany.AskDividendCalculatorProjection( iCompany.mMorningstar.mUrlDividendCalculator20Years )
		iCompany.mMorningstar.mFinancialsDividendsYield20Years.mGrowthAverage = annual_average
		iCompany.mMorningstar.mFinancialsDividendsYield20Years.mCurrent = '{:.02f}'.format( float( annual_average ) * 0.7 )	# Remove 30% for PS/Impots
		
		#---
		
		tr = soup.find( id='sal-components-dividends' ).find( 'table', class_='dividends-recent-table' ).find( 'tr', attrs={'ng-show': re.compile( 'upcomingDate.length' ) } )
		trs = tr.find_next_siblings( 'tr' )
		next_dates = []
		for tr in trs:
			next_date = tr.find( 'td' ).get_text( strip=True ).replace( '*', '' )	# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#get-text
			next_date = datetime.strptime( next_date, '%b %d, %Y' ).date()
			if next_date > date.today():
				iCompany.mMorningstar.mDividendNextDates.append( next_date )
		
		iCompany.mMorningstar.mDividendNextDates.reverse()
		