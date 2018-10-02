#!/usr/bin/python3

import os
import re
import sys
import csv
import locale

from bs4 import BeautifulSoup

class cCompany:
	def __init__( self, iISIN, iZBName, iZBCode, iZBSymbol, iMorningstarRegion, iMorningstarX, iYFSymbol, iRSymbol, iFVSymbol, iTSName, iFCName, iSourceDir, iDestinationDir ):
		self.mISIN = iISIN
		self.mName = iZBName
		
		self.mZBName = iZBName			# ZB = ZoneBourse
		self.mZBCode = iZBCode
		self.mZBSymbol = iZBSymbol

		self.mMorningstarSymbol = iZBSymbol
		self.mMorningstarRegion = iMorningstarRegion	# fra/gbr/usa/...
		self.mMorningstarX = iMorningstarX				# xpar/xlon/...
		
		self.mYFSymbol = iYFSymbol		# YF = Yahoo Finance
		self.mFVSymbol = iFVSymbol		# FV = FinViz
		self.mRSymbol = iRSymbol		# R = Reuters
		
		self.mTSName = iTSName			# TS = TradingSat
		self.mBName = iZBName			# B = boerse (use the same name as TradingSat, may use anything in fact)
		
		self.mFCName = iFCName			# FC = Finances.net
		
		self.mSourceDir = iSourceDir
		self.mDestinationDir = iDestinationDir
		
		self.Clean()
		
	#---
	
	def Clean( self ):
		self.mSFinancialsZB = None
		self.mSFinancialsZBTable = None
		self.mSFinancialsFV = None
		self.mSFinancialsR = None
		self.mSFinancialsYF = None
		self.mSFinancialsB = None
		self.mSSocietyZB = None
		self.mSDividendsFC = None
		self.mSDividendsTS = None
		
		self.mBNAGrowthFV5 = {}				# string 'xx%'
		self.mBNAGrowthR5 = {}				# string 'xx'
		self.mGrowthYF5 = {}				# string 'xx%'
		
		# B
		self.mYearsB = []
		self.mPERB = []
		self.mBNAB = []
		self.mBNAGrowthB = []
		self.mBNAGrowthAverageB = 0
		self.mBNAGrowthAverageLast5YB = 0
		self.mDividendB = []
		self.mDividendGrowthB = []
		self.mDividendGrowthAverageB = 0
		self.mDividendGrowthAverageLast5YB = 0
		self.mDividendYieldB = []
		
		# ZB
		self.mBNAGrowth = []
		self.mBNAGrowthAverage = 0
		self.mDividendsGrowth = []
		self.mDividendsGrowthAverage = 0	# 0.0 < ... < 1.0
		self.mYieldCurrent = 0				# 0.0 < ... < 100.0
	
	#---
	
	def SourceUrlFinancialsZB( self ):
		return 'https://www.zonebourse.com/{}-{}/{}/'.format( self.mZBName, self.mZBCode, 'fondamentaux' )
	def SourceFileHTMLFinancialsZB( self ):
		return os.path.join( self.mSourceDir, '{}.{}.finZB.html'.format( self.mName, self.mISIN ) )
		
	def SourceUrlFinancialsMorningstarIncomeStatement( self ):
		if self.mMorningstarX == 'xetr':
			return 'http://financials.morningstar.com/income-statement/is.html?t={}:{}&region={}&culture=en-US'.format( self.mMorningstarX, self.mMorningstarSymbol, self.mMorningstarRegion )
		return 'http://financials.morningstar.com/income-statement/is.html?t={}&region={}&culture=en-US'.format( self.mMorningstarSymbol, self.mMorningstarRegion )
	def SourceFileHTMLFinancialsMorningstarIncomeStatement( self ):
		return os.path.join( self.mSourceDir, '{}.{}.finMorningstarIncomeStatement.csv'.format( self.mName, self.mISIN ) )

	def SourceUrlFinancialsMorningstarBalanceSheet( self ):
		if self.mMorningstarX == 'xetr':
			return 'http://financials.morningstar.com/balance-sheet/bs.html?t={}:{}&region={}&culture=en-US'.format( self.mMorningstarX, self.mMorningstarSymbol, self.mMorningstarRegion )
		return 'http://financials.morningstar.com/balance-sheet/bs.html?t={}&region={}&culture=en-US'.format( self.mMorningstarSymbol, self.mMorningstarRegion )
	def SourceFileHTMLFinancialsMorningstarBalanceSheet( self ):
		return os.path.join( self.mSourceDir, '{}.{}.finMorningstarBalanceSheet.csv'.format( self.mName, self.mISIN ) )

	def SourceUrlFinancialsMorningstarRatios( self ):
		if self.mMorningstarX == 'xetr':
			return 'http://financials.morningstar.com/ratios/r.html?t={}:{}&region={}&culture=en-US'.format( self.mMorningstarX, self.mMorningstarSymbol, self.mMorningstarRegion )
		return 'http://financials.morningstar.com/ratios/r.html?t={}&region={}&culture=en-US'.format( self.mMorningstarSymbol, self.mMorningstarRegion )
	def SourceFileHTMLFinancialsMorningstarRatios( self ):
		return os.path.join( self.mSourceDir, '{}.{}.finMorningstarRatios.csv'.format( self.mName, self.mISIN ) )
		
	def SourceUrlFinancialsFV( self ):
		return 'https://finviz.com/quote.ashx?t={}'.format( self.mFVSymbol )
	def SourceFileHTMLFinancialsFV( self ):
		return os.path.join( self.mSourceDir, '{}.{}.finFV.html'.format( self.mName, self.mISIN ) )
		
	def SourceUrlFinancialsR( self ):
		return 'https://www.reuters.com/finance/stocks/financial-highlights/{}'.format( self.mRSymbol )
	def SourceFileHTMLFinancialsR( self ):
		return os.path.join( self.mSourceDir, '{}.{}.finR.html'.format( self.mName, self.mISIN ) )
		
	def SourceUrlFinancialsYF( self ):
		if self.mISIN == 'GB0008847096':
			return 'https://uk.finance.yahoo.com/quote/{}/analysis?p={}'.format( self.mYFSymbol, self.mYFSymbol )
		else:
			return 'https://finance.yahoo.com/quote/{}/analysis?p={}'.format( self.mYFSymbol, self.mYFSymbol )
	def SourceFileHTMLFinancialsYF( self ):
		return os.path.join( self.mSourceDir, '{}.{}.finYF.html'.format( self.mName, self.mISIN ) )
		
	def SourceUrlFinancialsB( self ):
		return 'https://www.boerse.de/fundamental-analyse/{}-Aktie/{}'.format( self.mBName, self.mISIN )
	def SourceFileHTMLFinancialsB( self ):
		return os.path.join( self.mSourceDir, '{}.{}.finB.html'.format( self.mName, self.mISIN ) )
		
	def SourceUrlSocietyZB( self ):
		return 'https://www.zonebourse.com/{}-{}/{}/'.format( self.mZBName, self.mZBCode, 'societe' )
	def SourceFileHTMLSocietyZB( self ):
		return os.path.join( self.mSourceDir, '{}.{}.socZB.html'.format( self.mName, self.mISIN ) )
		
	def SourceUrlDividendsTS( self ):
		return 'https://www.tradingsat.com/{}-{}/dividende.html'.format( self.mTSName, self.mISIN )
	def SourceFileHTMLDividendsTS( self ):
		return os.path.join( self.mSourceDir, '{}.{}.divTS.html'.format( self.mName, self.mISIN ) )
		
	def SourceUrlDividendsFC( self ):
		return 'http://www.finances.net/dividendes/{}'.format( self.mFCName )
	def SourceFileHTMLDividendsFC( self ):
		return os.path.join( self.mSourceDir, '{}.{}.divFC.html'.format( self.mName, self.mISIN ) )
		
	def SourceUrlChartZB( self ):
		return 'https://www.zonebourse.com/{}-{}/{}/'.format( self.mZBName, self.mZBCode, 'graphiques' )
	def SourceUrlStockPriceZB( self, iDuration, iWidth, iHeight ):
		return 'https://www.zonebourse.com/zbcache/charts/ObjectChart.aspx?Name={0}&Type=Custom&Intraday=1&Width={2}&Height={3}&Cycle=NONE&Duration={1}&TopMargin=10&Render=Candle&ShowName=0'.format( self.mZBCode, iDuration, iWidth, iHeight )
		
	def FileIMG( self, iYears ):
		return '{}.{}.{}.{}.gif'.format( self.mName, self.mISIN, self.mZBCode, iYears )

	def SourceFileIMG( self, iYears ):
		return os.path.join( self.mSourceDir, self.FileIMG( iYears ) )

	# from where the html file is !
	def DestinationFileIMG( self, iYears ):
		return os.path.join( self.mDestinationDir, self.FileIMG( iYears ) )
	
	#---
	
	def ComputeCroissanceTr( self, iTr ):
		bs = iTr.find_all( 'b' )
		prices = []
		for b in bs:
			price_str = b.string.strip().replace( ',', '.' ).replace( ' ', '' )
			if price_str == '-':
				continue
			prices.append( float( price_str ) )
		
		croissances = []
		for i in range( 5 ):
			if not i:
				continue
			av = ( prices[i] - prices[i-1] ) / abs( prices[i-1] )
			croissances.append( av )
		
		return ( croissances, sum( croissances ) / len( croissances ) )

	def ComputeCroissance( self, iList ):
		croissances = []
		for i in range( len( iList ) ):
			if not i:
				continue
			av = 0
			if iList[i-1]:
				av = ( iList[i] - iList[i-1] ) / abs( iList[i-1] )
			croissances.append( av )
		
		# return ( croissances, sum( croissances ) / len( croissances ), pow( croissances[-1] - croissances[0], 1.0 / len( croissances ) ) )
		return ( croissances, sum( croissances ) / len( croissances ), sum( croissances[-5:] ) / len( croissances ) )
		
	# bof bof
	def MyAtof( self, iX ):
		if not len( iX ):
			return 0.0
		return locale.atof( iX )

	def Fill( self ):
		html_financials = ''
		with open( self.SourceFileHTMLFinancialsZB(), 'r', encoding='utf-8' ) as fd:
			html_financials = fd.read()
		if not html_financials:
			print( 'ERROR: financials html is empty' )
			return
			
		self.mSFinancialsZB = BeautifulSoup( html_financials, 'html5lib' )
		
		if self.mFVSymbol:
			html_financials = ''
			with open( self.SourceFileHTMLFinancialsFV(), 'r', encoding='utf-8' ) as fd:
				html_financials = fd.read()
			if not html_financials:
				print( 'ERROR: financials html is empty' )
				return
				
			self.mSFinancialsFV = BeautifulSoup( html_financials, 'html5lib' )
		
		if self.mRSymbol:
			html_financials = ''
			with open( self.SourceFileHTMLFinancialsR(), 'r', encoding='utf-8' ) as fd:
				html_financials = fd.read()
			if not html_financials:
				print( 'ERROR: financials html is empty' )
				return
				
			self.mSFinancialsR = BeautifulSoup( html_financials, 'html5lib' )
		
		if self.mYFSymbol:
			html_financials = ''
			with open( self.SourceFileHTMLFinancialsYF(), 'r', encoding='utf-8' ) as fd:
				html_financials = fd.read()
			if not html_financials:
				print( 'ERROR: financials html is empty' )
				return
				
			self.mSFinancialsYF = BeautifulSoup( html_financials, 'html5lib' )
		
		if self.mBName:
			html_financials = ''
			with open( self.SourceFileHTMLFinancialsB(), 'r', encoding='utf-8' ) as fd:
				html_financials = fd.read()
			if not html_financials:
				print( 'ERROR: financials html is empty' )
				return
				
			self.mSFinancialsB = BeautifulSoup( html_financials, 'html5lib' )
		
		html_society_zb = ''
		with open( self.SourceFileHTMLSocietyZB(), 'r', encoding='utf-8' ) as fd:
			html_society_zb = fd.read()
		if not html_society_zb:
			print( 'ERROR: society html is empty' )
			return
			
		self.mSSocietyZB = BeautifulSoup( html_society_zb, 'html5lib' )
		
		if self.mFCName:
			html_dividends = ''
			with open( self.SourceFileHTMLDividendsFC(), 'r', encoding='utf-8' ) as fd:
				html_dividends = fd.read()
			if not html_dividends:
				print( 'ERROR: dividends fc html is empty' )
				return
				
			self.mSDividendsFC = BeautifulSoup( html_dividends, 'html5lib' )
			
		if self.mTSName:
			html_dividends = ''
			with open( self.SourceFileHTMLDividendsTS(), 'r', encoding='utf-8' ) as fd:
				html_dividends = fd.read()
			if not html_dividends:
				print( 'ERROR: dividends ts html is empty' )
				return
				
			self.mSDividendsTS = BeautifulSoup( html_dividends, 'html5lib' )
		
		#---
		
		self.mSFinancialsZBTable = self.mSFinancialsZB.find( 'table', class_='BordCollapseYear' )
		if self.mSFinancialsZBTable:
			for tr in self.mSFinancialsZBTable.find_all( 'tr' ):
				tr.append( self.mSFinancialsZB.new_tag( 'td' ) )
			
			tr_years = self.mSFinancialsZBTable.find( 'tr' ).find_next_sibling()
			tr_ca = tr_years.find_next_sibling()
			tr_ebitda = tr_ca.find_next_sibling()
			tr_ebitda.find_next_sibling().decompose()
			tr_ebitda.find_next_sibling().decompose()
			tr_net = tr_ebitda.find_next_sibling()
			
			tr_bna = tr_net.find_next_sibling().find_next_sibling()
			tr_dividends = tr_bna.find_next_sibling()
			tr_rendements = tr_dividends.find_next_sibling()
			
			#---
			
			self.mDividendsGrowth, self.mDividendsGrowthAverage = self.ComputeCroissanceTr( tr_dividends )
			
			self.mBNAGrowth, self.mBNAGrowthAverage = self.ComputeCroissanceTr( tr_bna )
			
			td_rendement = tr_rendements.find( 'td' ).find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find( 'b' ).string
			self.mYieldCurrent = float( td_rendement.strip().replace( '%', '' ).replace( ',', '.' ) )
		
		#---
		
		self.mBNAGrowthFV5['-5'] = '-'
		self.mBNAGrowthFV5['0'] = '-'
		self.mBNAGrowthFV5['+1'] = '-'
		self.mBNAGrowthFV5['+5'] = '-'
		if self.mSFinancialsFV:
			table = self.mSFinancialsFV.find( 'table', class_='snapshot-table2' )
			tr = table.find( 'tr' ).find_next_sibling().find_next_sibling().find_next_sibling()
			td = tr.find( string='EPS this Y' ).parent
			td_value = td.find_next_sibling().string
			self.mBNAGrowthFV5['0'] = td_value
			
			tr = tr.find_next_sibling()
			td = tr.find( string='EPS next Y' ).parent
			td_value = td.find_next_sibling().string
			self.mBNAGrowthFV5['+1'] = td_value
		
			tr = tr.find_next_sibling()
			td = tr.find( string='EPS next 5Y' ).parent
			td_value = td.find_next_sibling().string
			self.mBNAGrowthFV5['+5'] = td_value
		
			tr = tr.find_next_sibling()
			td = tr.find( string='EPS past 5Y' ).parent
			td_value = td.find_next_sibling().string
			self.mBNAGrowthFV5['-5'] = td_value
		
		#---
		
		self.mBNAGrowthR5['-1'] = '-'
		self.mBNAGrowthR5['-3'] = '-'
		self.mBNAGrowthR5['-5'] = '-'
		if self.mSFinancialsR:
			td = self.mSFinancialsR.find( string='EPS (TTM) %' ).parent.find_next_sibling()
			td_value = td.string
			self.mBNAGrowthR5['-1'] = td_value
			
			td = td.find_next_sibling()
			td_value = td.string
			self.mBNAGrowthR5['-3'] = td_value
		
			td = td.find_next_sibling()
			td_value = td.string
			self.mBNAGrowthR5['-5'] = td_value
		
		#---
		
		self.mGrowthYF5['-5'] = '-'
		self.mGrowthYF5['0'] = '-'
		self.mGrowthYF5['+1'] = '-'
		self.mGrowthYF5['+5'] = '-'
		if self.mSFinancialsYF and self.mSFinancialsYF.find( string='Past 5 Years (per annum)' ):
			td = self.mSFinancialsYF.find( string='Past 5 Years (per annum)' ).find_parent( 'td' ).find_next_sibling()
			td_value = td.string
			self.mGrowthYF5['-5'] = td_value
			
			td = td.find_parent( 'tr' ).find_previous_sibling().find( 'td' ).find_next_sibling()
			td_value = td.string
			self.mGrowthYF5['+5'] = td_value
		
			td = td.find_parent( 'tr' ).find_previous_sibling().find( 'td' ).find_next_sibling()
			td_value = td.string
			self.mGrowthYF5['+1'] = td_value
		
			td = td.find_parent( 'tr' ).find_previous_sibling().find( 'td' ).find_next_sibling()
			td_value = td.string
			self.mGrowthYF5['0'] = td_value
		
		#---
		
		self.mYearsB = []
		self.mPERB = []
		self.mBNAB = []
		self.mBNAGrowthB = []
		self.mBNAGrowthAverageB = 0
		self.mBNAGrowthAverageLast5YB = 0
		self.mDividendB = []
		self.mDividendGrowthB = []
		self.mDividendGrowthAverageB = 0
		self.mDividendGrowthAverageLast5YB = 0
		self.mDividendYieldB = []
		if self.mSFinancialsB and not self.mSFinancialsB.find( string=re.compile('Bilanz \(\)') ):
			td = self.mSFinancialsB.find( id='rentabilitaet' ).find_next_sibling( 'table' ).find( 'tr' ).find( 'th' ).find_next_sibling()
			while td:
				self.mYearsB.append( td.string )
				td = td.find_next_sibling( 'th' )
			
			td = self.mSFinancialsB.find( id='rentabilitaet' ).find_next_sibling( 'table' ).find( 'td', string='Dividendenrendite' ).find_next_sibling()
			while td:
				self.mDividendYieldB.append( td.string )
				td = td.find_next_sibling( 'td' )

			td = self.mSFinancialsB.find( id='kennzahlen' ).find_next_sibling( 'table' ).find_next_sibling( 'table' ).find( 'td' ).find( 'a', string='KGV' ).parent.find_next_sibling()
			while td:
				s = td.string.strip().replace( ',', '.' ) if td.string is not None else '0'
				if 'n.v.' in s:
					s = '0'
				if '-' in s:
					s = '0'
				self.mPERB.append( float( s ) )
				td = td.find_next_sibling( 'td' )

			td = self.mSFinancialsB.find( id='kennzahlen' ).find_next_sibling( 'table' ).find( 'td', string='Dividende je Aktie' ).find_next_sibling()
			while td:
				s = td.string.strip().replace( ',', '.' ) if td.string is not None else '0'
				self.mDividendB.append( float( s ) )
				td = td.find_next_sibling( 'td' )

			self.mDividendGrowthB, self.mDividendGrowthAverageB, self.mDividendGrowthAverageLast5YB = self.ComputeCroissance( self.mDividendB )

			td = self.mSFinancialsB.find( id='kennzahlen' ).find_next_sibling( 'table' ).find( 'td', string='Gewinn je Aktie (unverwässert)' ).find_next_sibling()
			while td:
				s = td.string.strip().replace( ',', '.' ) if td.string is not None else '0'
				self.mBNAB.append( float( s ) )
				td = td.find_next_sibling( 'td' )

			self.mBNAGrowthB, self.mBNAGrowthAverageB, self.mBNAGrowthAverageLast5YB = self.ComputeCroissance( self.mBNAB )

		#---
		
		previous_local = locale.setlocale( locale.LC_ALL )
		
		with open( self.SourceFileHTMLFinancialsMorningstarIncomeStatement(), newline='' ) as csvfile:
			reader = csv.reader( csvfile )
			
			self.is_years = []
			self.is_year = ''
			self.ebitdas = []
			self.ebitda = ''
			for row in reader:
				if len( row ) <= 1:
					continue
				if row[0].startswith( 'Fiscal year ends' ):
					self.is_years = row[1:-1]
					self.is_year = row[-1]
				if row[0].startswith( 'EBITDA' ):
					self.ebitdas = row[1:-1]
					self.ebitda = row[-1]
			
			locale.setlocale( locale.LC_ALL, 'en_US.UTF8' )
			self.ebitdas = list( map( self.MyAtof, self.ebitdas ) )
			self.ebitda = self.MyAtof( self.ebitda )
		
			# print('is')
			# print( self.is_years )
			# print( self.is_year )
			# print( self.ebitdas )
			# print( self.ebitda )

		with open( self.SourceFileHTMLFinancialsMorningstarBalanceSheet(), newline='' ) as csvfile:
			reader = csv.reader( csvfile )
			
			self.bs_years = []
			self.ltd = []
			for row in reader:
				if len( row ) <= 1:
					continue
				if row[0].startswith( 'Fiscal year ends' ):
					self.bs_years = row[1:]
				if row[0].startswith( 'Total non-current liabilities' ):
					self.ltd = row[1:]
			
			locale.setlocale( locale.LC_ALL, 'en_US.UTF8' )
			self.ltd = list( map( self.MyAtof, self.ltd ) )
		
			# print('bs')
			# print( self.bs_years )
			# print( self.ltd )

		with open( self.SourceFileHTMLFinancialsMorningstarRatios(), newline='' ) as csvfile:
			reader = csv.reader( csvfile )
			
			self.financials_years = []
			self.financials_year = ''
			self.revenues = []
			self.revenue = ''
			self.earnings = []
			self.earning = ''
			
			self.profitability_years = []
			self.profitability_year = ''
			self.roes = []
			self.roe = ''
			self.rois = []
			self.roi = ''
			self.ics = []
			self.ic = ''
			
			self.fcf_ss = []
			self.fcf_s = ''
			
			self.health_years = []
			self.health_year = ''
			self.currentratios = []
			self.currentratio = ''
			self.d_es = []
			self.d_e = ''
			
			for row in reader:
				if len( row ) <= 1:
					continue
				if row[0].startswith( 'Profitability' ):
					self.financials_years = row[1:-1]
					self.financials_year = row[-1]
					self.profitability_years = row[1:-1]
					self.profitability_year = row[-1]
				if row[0].startswith( 'Revenue' ) and row[0].endswith( 'Mil' ):
					self.revenues = row[1:-1]
					self.revenue = row[-1]
				if row[0].startswith( 'Earnings' ):
					self.earnings = row[1:-1]
					self.earning = row[-1]
					
				if row[0].startswith( 'Return on Equity' ):
					self.roes = row[1:-1]
					self.roe = row[-1]
				if row[0].startswith( 'Return on Invested Capital' ):
					self.rois = row[1:-1]
					self.roi = row[-1]
				if row[0].startswith( 'Interest Coverage' ):
					self.ics = row[1:-1]
					self.ic = row[-1]
					
				if row[0].startswith( 'Free Cash Flow/Sales' ):
					self.fcf_ss = row[1:-1]
					self.fcf_s = row[-1]
			
				if row[0].startswith( 'Liquidity/Financial Health' ):
					self.health_years = row[1:-1]
					self.health_year = row[-1]
				if row[0].startswith( 'Current Ratio' ):
					self.currentratios = row[1:-1]
					self.currentratio = row[-1]
				if row[0].startswith( 'Debt/Equity' ):
					self.d_es = row[1:-1]
					self.d_e = row[-1]
					
			locale.setlocale( locale.LC_ALL, 'en_US.UTF8' )
			self.revenues = list( map( self.MyAtof, self.revenues ) )
			self.revenue = self.MyAtof( self.revenue )
			locale.setlocale( locale.LC_ALL, 'fr_FR.UTF8' )
			self.earnings = list( map( self.MyAtof, self.earnings ) )
			self.earning = self.MyAtof( self.earning )
			
			locale.setlocale( locale.LC_ALL, 'fr_FR.UTF8' )
			self.roes = list( map( self.MyAtof, self.roes ) )
			self.roe = self.MyAtof( self.roe )
			self.rois = list( map( self.MyAtof, self.rois ) )
			self.roi = self.MyAtof( self.roi )
			self.ics = list( map( self.MyAtof, self.ics ) )
			self.ic = self.MyAtof( self.ic )
			
			self.fcf_ss = list( map( self.MyAtof, self.fcf_ss ) )
			self.fcf_s = self.MyAtof( self.fcf_s )
		
			self.currentratios = list( map( self.MyAtof, self.currentratios ) )
			self.currentratio = self.MyAtof( self.currentratio )
			self.d_es = list( map( self.MyAtof, self.d_es ) )
			self.d_e = self.MyAtof( self.d_e )
		
			# print('ratios')
			# print( self.financials_years )
			# print( self.financials_year )
			# print( self.revenues )
			# print( self.revenue )
			# print( self.earnings )
			# print( self.earning )
			
			# print('ratios2')
			# print( self.profitability_years )
			# print( self.profitability_year )
			# print( self.roes )
			# print( self.roe )
			# print( self.rois )
			# print( self.roi )
			# print( self.ics )
			# print( self.ic )
			
			# print('ratios3')
			# print( self.health_years )
			# print( self.health_year )
			# print( self.currentratios )
			# print( self.currentratio )
			# print( self.d_es )
			# print( self.d_e )
			
		locale.setlocale( locale.LC_ALL, previous_local )

		# sys.exit( 0 )





