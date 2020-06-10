#!/usr/bin/env python3
#
# Copyright (c) 2018-19 m-ll. All Rights Reserved.
#
# Licensed under the MIT License.
# See LICENSE file in the project root for full license information.
#
# 2b13c8312f53d4b9202b6c8c0f0e790d10044f9a00d8bab3edf3cd287457c979
# 29c355784a3921aa290371da87bce9c1617b8584ca6ac6fb17fb37ba4a07d191
#

import csv
import re
from datetime import date, datetime

from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style

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
		self._ParseQuote( iCompany )
		self._ParseValuation( iCompany )
		self._ParseDividends( iCompany )
			
	#---
		
	def _ParseIncomStatement( self, iCompany ):
		print( '		- Income Statement ...' )

		input = iCompany.DataPathFile( iCompany.mMorningstar.FileNameIncomeStatement() )

		with input.open( newline='' ) as csvfile:
			reader = csv.reader( csvfile )
			
			for row in reader:
				if len( row ) <= 1:
					continue
				
				if row[0].startswith( 'Fiscal year ends' ):
					iCompany.mMorningstar.mISYears.SetRow( row )
				elif row[0].startswith( 'EBITDA' ):
					iCompany.mMorningstar.mEBITDA.SetRow( row )
		
	def _ParseBalanceSheet( self, iCompany ):
		print( '		- Balance Sheet ...' )

		input = iCompany.DataPathFile( iCompany.mMorningstar.FileNameBalanceSheet() )

		with input.open( newline='' ) as csvfile:
			reader = csv.reader( csvfile )
			
			for row in reader:
				if len( row ) <= 1:
					continue
				
				if row[0].startswith( 'Fiscal year ends' ):
					iCompany.mMorningstar.mBSYears.SetRow( row )
				elif row[0].startswith( 'Total non-current liabilities' ):
					iCompany.mMorningstar.mLongTermDebt.SetRow( row )
				elif row[0].startswith( 'Total liabilities' ) and not iCompany.mMorningstar.mLongTermDebt.mData:	# CNP
					iCompany.mMorningstar.mLongTermDebt.SetRow( row )
		
		for i, ltd in enumerate( iCompany.mMorningstar.mLongTermDebt.mData ):
			if not iCompany.mMorningstar.mEBITDA.mData:
				break
			
			ebitda = iCompany.mMorningstar.mEBITDA.mData[i]
			if not ltd or not ebitda:
				iCompany.mMorningstar.mLTDOnEBITDA.mData.append( '' )
				continue
			
			ratio = float( ltd ) / float( ebitda )
			iCompany.mMorningstar.mLTDOnEBITDA.mData.append( '{:.02f}'.format( ratio ) )
			iCompany.mMorningstar.mLTDOnEBITDA.Update()
			
	def _ParseRatios( self, iCompany ):
		print( '		- Ratios ...' )

		input = iCompany.DataPathFile( iCompany.mMorningstar.FileNameRatios() )

		with input.open( newline='' ) as csvfile:
			reader = csv.reader( csvfile )
			
			for row in reader:
				if not row:
					continue
				
				if not row[0] and not iCompany.mMorningstar.mFinancialsYears.mData:		# 2 lines have the same format, and the first one is the wanted one
					iCompany.mMorningstar.mFinancialsYears.SetRow( row )
				elif row[0].startswith( 'Revenue' ) and row[0].endswith( 'Mil' ):
					iCompany.mMorningstar.mFinancialsRevenue.SetRow( row )
				elif row[0].startswith( 'Net Income' ) and row[0].endswith( 'Mil' ):
					iCompany.mMorningstar.mFinancialsNetIncome.SetRow( row )
				elif row[0].startswith( 'Dividends' ):
					iCompany.mMorningstar.mFinancialsDividends.SetRow( row )
				elif row[0].startswith( 'Payout Ratio' ):
					iCompany.mMorningstar.mFinancialsPayoutRatio.SetRow( row )
				elif row[0].startswith( 'Earnings' ):
					iCompany.mMorningstar.mFinancialsEarnings.SetRow( row )
				elif row[0].startswith( 'Book Value Per Share' ):
					iCompany.mMorningstar.mFinancialsBook.SetRow( row )
					
				elif row[0].startswith( 'Profitability' ):
					iCompany.mMorningstar.mProfitabilityYears.SetRow( row )
				elif row[0].startswith( 'Return on Equity' ):
					iCompany.mMorningstar.mProfitabilityROE.SetRow( row )
				elif row[0].startswith( 'Return on Invested Capital' ):
					iCompany.mMorningstar.mProfitabilityROI.SetRow( row )
				elif row[0].startswith( 'Interest Coverage' ):
					iCompany.mMorningstar.mProfitabilityIC.SetRow( row )
					
				elif row[0].startswith( 'Key Ratios -> Growth' ):
					row = next( reader )
					iCompany.mMorningstar.mGrowthYears.SetRow( row )
				elif row[0].startswith( 'Revenue %' ):
					row = next( reader )
					iCompany.mMorningstar.mGrowthRevenue.SetRow( row )	# YoY
				elif row[0].startswith( 'Net Income %' ):
					row = next( reader )
					iCompany.mMorningstar.mGrowthNetIncome.SetRow( row )	# YoY
				elif row[0].startswith( 'EPS %' ):
					row = next( reader )
					iCompany.mMorningstar.mGrowthEarnings.SetRow( row )	# YoY
					
				elif row[0].startswith( 'Free Cash Flow/Sales' ):
					iCompany.mMorningstar.mCashFlowFCFOnSales.SetRow( row )
			
				elif row[0].startswith( 'Liquidity/Financial Health' ):
					iCompany.mMorningstar.mHealthYears.SetRow( row )
				elif row[0].startswith( 'Current Ratio' ):
					iCompany.mMorningstar.mHealthCurrentRatio.SetRow( row )
				elif row[0].startswith( 'Debt/Equity' ):
					iCompany.mMorningstar.mHealthDebtOnEquity.SetRow( row )
				
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
		
	def _ParseQuote( self, iCompany ):
		print( '		- Quote ...' )

		input = iCompany.DataPathFile( iCompany.mMorningstar.FileNameQuote() )

		html_content = ''
		with input.open( 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		soup = BeautifulSoup( html_content, 'html5lib' )

		sections = soup.find_all( class_='sal-component-band-grid' )
		for section in sections:
			beta = section.find( string='Beta' )
			if beta:
				iCompany.mMorningstar.mQuoteBeta = float( beta.parent.find_next_sibling().string.strip() )

		sections = soup.find_all( class_='stock__profile-items-item' )
		# sections = soup.find_all( class_='sal-component-company-profile-body' )
		for section in sections:
			sector = section.find( string='Sector' )
			if sector:
				iCompany.mMorningstar.mQuoteSector = sector.parent.find_next_sibling().string.strip()
			industry = section.find( string='Industry' )
			if industry:
				iCompany.mMorningstar.mQuoteIndustry = industry.parent.find_next_sibling().string.strip()
		
	def _ParseValuation( self, iCompany ):
		print( '		- Valuation ...' )

		input = iCompany.DataPathFile( iCompany.mMorningstar.FileNameValuation() )

		html_content = ''
		with input.open( 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		soup = BeautifulSoup( html_content, 'html5lib' )
		section = soup.find( attrs={'mwc-id': 'salComponentsValuation'} ).find( 'table', class_='report-table' )		# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#the-keyword-arguments
		
		iCompany.mMorningstar.mValuationYears.SetTR( section, 'td', 'Calendar' )
			
		iCompany.mMorningstar.mValuationP2S.SetTR( section, 'span', 'Price/Sales' )
		iCompany.mMorningstar.mValuationPER.SetTR( section, 'span', 'Price/Earnings' )
		iCompany.mMorningstar.mValuationP2CF.SetTR( section, 'span', 'Price/Cash Flow' )
		iCompany.mMorningstar.mValuationP2B.SetTR( section, 'span', 'Price/Book' )
		iCompany.mMorningstar.mValuationEVOnEBITDA.SetTR( section, 'span', 'Enterprise Value/EBITDA' )
		
	def _ParseDividends( self, iCompany ):
		print( '		- Dividends ...' )

		input = iCompany.DataPathFile( iCompany.mMorningstar.FileNameDividends() )

		html_content = ''
		with input.open( 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		soup = BeautifulSoup( html_content, 'html5lib' )
		
		div = soup.find( attrs={'mwc-id': 'salComponentsDividends'} ).find( class_='dividend-yield' ).find_all( 'div' )[-1]
		s = div.string.replace( ',', '.' ).replace( '%', '' ).replace( '-', '' ).replace( '—', '' )
		iCompany.mMorningstar.mFinancialsDividendsYield.mTTM = s if s else '0'
		iCompany.mMorningstar.mYieldCurrent = float( iCompany.mMorningstar.mFinancialsDividendsYield.mTTM )
		
		iCompany.mMorningstar.mUrlDividendCalculator10Years = iCompany.UrlDividendCalculator( float( iCompany.mMorningstar.mFinancialsDividendsYield.mTTM ), float( iCompany.mMorningstar.mFinancialsGrowthDividends.mGrowthAverage ), 10 )
		annual_average = iCompany.AskDividendCalculatorProjection( iCompany.mMorningstar.mUrlDividendCalculator10Years )
		iCompany.mMorningstar.mFinancialsDividendsYield10Years.mTTM = annual_average
		
		iCompany.mMorningstar.mUrlDividendCalculator20Years = iCompany.UrlDividendCalculator( float( iCompany.mMorningstar.mFinancialsDividendsYield.mTTM ), float( iCompany.mMorningstar.mFinancialsGrowthDividends.mGrowthAverage ), 20 )
		annual_average = iCompany.AskDividendCalculatorProjection( iCompany.mMorningstar.mUrlDividendCalculator20Years )
		iCompany.mMorningstar.mFinancialsDividendsYield20Years.mTTM = annual_average
		
		#---

		tbody0 = soup.find( attrs={'mwc-id': 'salComponentsDividends'} ).find( 'table', class_='dividends-recent-table' ).find( 'tbody' )
		tbodys = tbody0.find_next_siblings( 'tbody' )
		for tbody in tbodys:
			tr0 = tbody.find( 'tr' )
			if tr0.find( 'td', class_='upcoming' ):
				dates = []
				trs = tr0.find_next_siblings( 'tr' )
				for tr in trs:
					next_date = tr.find( 'td' ).get_text( strip=True ).replace( '*', '' )	# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#get-text
					next_date = datetime.strptime( next_date, '%b %d, %Y' ).date()
					dates.append( next_date )
				dates.reverse()
				iCompany.mMorningstar.mFinancialsDividendsYears.mTTM = dates
			else:
				dates = []
				trs = tr0.find_next_siblings( 'tr' )
				for tr in trs:
					next_date = tr.find( 'td' ).get_text( strip=True ).replace( '*', '' )	# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#get-text
					next_date = datetime.strptime( next_date, '%b %d, %Y' ).date()
					dates.append( next_date )
				dates.reverse()
				iCompany.mMorningstar.mFinancialsDividendsYears.mData.append( dates )

		iCompany.mMorningstar.mFinancialsDividendsYears.mData.reverse()
