#!/usr/bin/python3

import os
import re
import sys
import csv
import locale

from bs4 import BeautifulSoup

class cDataMorningstar:
	def __init__( self, iRow=None, iParent=None ):
		self.mData = []
		
		self.mTTM = ''
		self.mLatestQuarter = ''
		
		self.mCurrent = ''
		self.m5Years = ''
		self.mIndex = ''
		
		self.mParent = iParent
		
		if iRow is not None:
			self.SetRow( iRow )
	
	def __repr__(self):
		return 'cDataMorningstar( [{}], "{}", "{}" )'.format( ', '.join( map( str, self.mData ) ), self.mTTM, self.mLatestQuarter )
	
	def SetRow( self, iRow ):
		if self.mParent is None:
			if iRow[-1] == 'TTM':
				self.mData = iRow[1:-1]
				self.mTTM = iRow[-1]
			elif iRow[-1].startswith( 'Latest' ):
				self.mData = iRow[1:-1]
				self.mLatestQuarter = iRow[-1]
			else:
				self.mData = iRow[1:]
		else:
			if self.mParent.mTTM:
				self.mData = iRow[1:-1]
				self.mTTM = iRow[-1]
			elif self.mParent.mLatestQuarter:
				self.mData = iRow[1:-1]
				self.mLatestQuarter = iRow[-1]
			else:
				self.mData = iRow[1:]
		
		self.mData = list( map( self._FixLocale, self.mData ) );
		self.mTTM = self._FixLocale( self.mTTM )
		self.mLatestQuarter = self._FixLocale( self.mLatestQuarter )
			
	def _FixLocale( self, iString ):
		return iString.replace( ',', '.' ).replace( '(', '-' ).replace( ')', '' )
			
	def SetTR( self, iSSection, iTag, iText ):
		td = iSSection.find( iTag, string=iText )
		if not td and self.mParent:		# value doesn't exist, like EBITDA for CNP
			self.mData = [''] * len( self.mParent.mData )
			return
			
		if td.name == 'td':		# for years row
			td = td.find_next_sibling( 'td' )
			while td and 'Current' not in td.string:
				v = td.string
				self.mData.append( v )
				
				td = td.find_next_sibling( 'td' )
				
			self.mCurrent = td.string
			td = td.find_next_sibling( 'td' )
			self.m5Years = td.string
			td = td.find_next_sibling( 'td' )
			self.mIndex = td.string
			
		else:
			td = td.find_parent( 'td' )
			td = td.find_next_sibling( 'td' )
			while len( self.mData ) != len( self.mParent.mData ):
				v = td.find( 'span' ).string
				self.mData.append( v )
				
				td = td.find_next_sibling( 'td' )
			
			self.mCurrent = td.find( 'span' ).string
			td = td.find_next_sibling( 'td' )
			self.m5Years = td.find( 'span' ).string
			td = td.find_next_sibling( 'td' )
			self.mIndex = td.find( 'span' ).string
			
		self.mData = list( map( self._FixLocale2, self.mData ) );
		self.mCurrent = self._FixLocale2( self.mCurrent )
		self.m5Years = self._FixLocale2( self.m5Years )
		self.mIndex = self._FixLocale2( self.mIndex )
			
	def _FixLocale2( self, iString ):
		return iString.replace( ',', '' ).replace( '—', '' )
			

class cCompany:
	def __init__( self, iISIN, iZBName, iZBCode, iZBSymbol, iMorningstarRegion, iMorningstarX, iYFSymbol, iRSymbol, iFVSymbol, iTSName, iFCName, iSourceDir='', iDestinationDir='' ):
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
	
	def DataDir( self, iDirectory ):
		self.mSourceDir = iDirectory
	
	def ImageDir( self, iDirectory ):
		self.mDestinationDir = iDirectory
	
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
		
	def SourceUrlFinancialsMorningstarValuation( self ):
		return 'https://www.morningstar.com/stocks/{}/{}/quote.html'.format( self.mMorningstarX, self.mMorningstarSymbol.lower() )
	def SourceFileHTMLFinancialsMorningstarValuation( self ):
		return os.path.join( self.mSourceDir, '{}.{}.finMorningstarValuation.html'.format( self.mName, self.mISIN ) )
		
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
		
	def Fill( self ):
		self.FillZoneBourse()
		self.FillFinviz()
		self.FillReuters()
		self.FillYahooFinance()
		self.FillBoerse()
		self.FillFinances()
		self.FillTradingSat()
		self.FillMorningstar()
		
	def FillZoneBourse( self ):
		html_content = ''
		with open( self.SourceFileHTMLFinancialsZB(), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		self.mSFinancialsZB = BeautifulSoup( html_content, 'html5lib' )
		
		#---
		
		self.mSFinancialsZBTable = self.mSFinancialsZB.find( 'table', class_='BordCollapseYear' )
		if not self.mSFinancialsZBTable:
			return
			
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
		
		html_content = ''
		with open( self.SourceFileHTMLSocietyZB(), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		self.mSSocietyZB = BeautifulSoup( html_content, 'html5lib' )
		
	def FillFinviz( self ):
		self.mBNAGrowthFV5['-5'] = '-'
		self.mBNAGrowthFV5['0'] = '-'
		self.mBNAGrowthFV5['+1'] = '-'
		self.mBNAGrowthFV5['+5'] = '-'
		
		if not self.mFVSymbol:
			return
			
		html_content = ''
		with open( self.SourceFileHTMLFinancialsFV(), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		self.mSFinancialsFV = BeautifulSoup( html_content, 'html5lib' )
		
		#---
		
		if not self.mSFinancialsFV:
			return
			
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
		
	def FillReuters( self ):
		self.mBNAGrowthR5['-1'] = '-'
		self.mBNAGrowthR5['-3'] = '-'
		self.mBNAGrowthR5['-5'] = '-'
		
		if not self.mRSymbol:
			return
			
		html_content = ''
		with open( self.SourceFileHTMLFinancialsR(), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		self.mSFinancialsR = BeautifulSoup( html_content, 'html5lib' )
		
		#---
		
		if not self.mSFinancialsR:
			return
			
		td = self.mSFinancialsR.find( string='EPS (TTM) %' ).parent.find_next_sibling()
		td_value = td.string
		self.mBNAGrowthR5['-1'] = td_value
		
		td = td.find_next_sibling()
		td_value = td.string
		self.mBNAGrowthR5['-3'] = td_value
	
		td = td.find_next_sibling()
		td_value = td.string
		self.mBNAGrowthR5['-5'] = td_value
		
	def FillYahooFinance( self ):
		self.mGrowthYF5['-5'] = '-'
		self.mGrowthYF5['0'] = '-'
		self.mGrowthYF5['+1'] = '-'
		self.mGrowthYF5['+5'] = '-'
		
		if not self.mYFSymbol:
			return
			
		html_content = ''
		with open( self.SourceFileHTMLFinancialsYF(), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		self.mSFinancialsYF = BeautifulSoup( html_content, 'html5lib' )
		
		#---
		
		if not self.mSFinancialsYF:
			return
		if not self.mSFinancialsYF.find( string='Past 5 Years (per annum)' ):
			return
			
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
		
	def FillBoerse( self ):
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
		
		if not self.mBName:
			return
			
		html_content = ''
		with open( self.SourceFileHTMLFinancialsB(), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		self.mSFinancialsB = BeautifulSoup( html_content, 'html5lib' )
		
		#---
		
		if not self.mSFinancialsB:
			return
		if self.mSFinancialsB.find( string=re.compile('Bilanz \(\)') ):
			return
			
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
			if td.string is None or td.string.strip() == '-':
				s = '0'
			else:
				s = td.string.strip().replace( ',', '.' )
			self.mDividendB.append( float( s ) )
			td = td.find_next_sibling( 'td' )

		self.mDividendGrowthB, self.mDividendGrowthAverageB, self.mDividendGrowthAverageLast5YB = self.ComputeCroissance( self.mDividendB )

		td = self.mSFinancialsB.find( id='kennzahlen' ).find_next_sibling( 'table' ).find( 'td', string='Gewinn je Aktie (unverwässert)' ).find_next_sibling()
		while td:
			if td.string is None or td.string.strip() == '-':
				s = '0'
			else:
				s = td.string.strip().replace( ',', '.' )
			self.mBNAB.append( float( s ) )
			td = td.find_next_sibling( 'td' )

		self.mBNAGrowthB, self.mBNAGrowthAverageB, self.mBNAGrowthAverageLast5YB = self.ComputeCroissance( self.mBNAB )

	def FillFinances( self ):
		if not self.mFCName:
			return
			
		html_content = ''
		with open( self.SourceFileHTMLDividendsFC(), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		self.mSDividendsFC = BeautifulSoup( html_content, 'html5lib' )
			
	def FillTradingSat( self ):
		if not self.mTSName:
			return
			
		html_content = ''
		with open( self.SourceFileHTMLDividendsTS(), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		self.mSDividendsTS = BeautifulSoup( html_content, 'html5lib' )
		
	def FillMorningstar( self ):
		self.mMorningstarISYears = None
		self.mMorningstarEBITDA = None
		
		self.mMorningstarBSYears = None
		self.mMorningstarLongTermDebt = None
		self.mMorningstarLTDOnEBITDA = cDataMorningstar()
		
		self.mMorningstarFinancialsYears = None
		self.mMorningstarFinancialsRevenue = None
		self.mMorningstarFinancialsNetIncome = None
		self.mMorningstarFinancialsDividends = None
		self.mMorningstarFinancialsGrowthDividends = cDataMorningstar()
		self.mMorningstarFinancialsPayoutRatio = None
		self.mMorningstarFinancialsEarnings = None
		self.mMorningstarFinancialsBook = None
		self.mMorningstarFinancialsGrowthBook = cDataMorningstar()
		self.mMorningstarProfitabilityYears = None
		self.mMorningstarProfitabilityROE = None
		self.mMorningstarProfitabilityROI = None
		self.mMorningstarProfitabilityIC = None
		self.mMorningstarGrowthYears = None
		self.mMorningstarGrowthRevenue = None
		self.mMorningstarGrowthNetIncome = None
		self.mMorningstarGrowthEarnings = None
		self.mMorningstarCashFlowFCFOnSales = None
		self.mMorningstarHealthYears = None
		self.mMorningstarHealthCurrentRatio = None
		self.mMorningstarHealthDebtOnEquity = None
		
		self.mMorningstarValuationYears = cDataMorningstar()
		self.mMorningstarValuationP2S = cDataMorningstar( iParent=self.mMorningstarValuationYears )
		self.mMorningstarValuationPER = cDataMorningstar( iParent=self.mMorningstarValuationYears )
		self.mMorningstarValuationP2CF = cDataMorningstar( iParent=self.mMorningstarValuationYears )
		self.mMorningstarValuationP2B = cDataMorningstar( iParent=self.mMorningstarValuationYears )
		self.mMorningstarValuationEVOnEBITDA = cDataMorningstar( iParent=self.mMorningstarValuationYears )
		
		if not self.mMorningstarRegion:
			return
			
		with open( self.SourceFileHTMLFinancialsMorningstarIncomeStatement(), newline='' ) as csvfile:
			reader = csv.reader( csvfile )
			
			for row in reader:
				if len( row ) <= 1:
					continue
				
				if row[0].startswith( 'Fiscal year ends' ):
					self.mMorningstarISYears = cDataMorningstar( row )
				elif row[0].startswith( 'EBITDA' ):
					self.mMorningstarEBITDA = cDataMorningstar( row, self.mMorningstarISYears )
		
		if self.mMorningstarEBITDA is None:
			self.mMorningstarEBITDA = cDataMorningstar()
			self.mMorningstarEBITDA.mData = [''] * len( self.mMorningstarISYears.mData )
		
		#---
		
		with open( self.SourceFileHTMLFinancialsMorningstarBalanceSheet(), newline='' ) as csvfile:
			reader = csv.reader( csvfile )
			
			for row in reader:
				if len( row ) <= 1:
					continue
				
				if row[0].startswith( 'Fiscal year ends' ):
					self.mMorningstarBSYears = cDataMorningstar( row )
				elif row[0].startswith( 'Total non-current liabilities' ):
					self.mMorningstarLongTermDebt = cDataMorningstar( row, self.mMorningstarBSYears )
				elif row[0].startswith( 'Total liabilities' ) and self.mMorningstarLongTermDebt is None:	# CNP
					self.mMorningstarLongTermDebt = cDataMorningstar( row, self.mMorningstarBSYears )
		
		for i, ltd in enumerate( self.mMorningstarLongTermDebt.mData ):
			ebitda = self.mMorningstarEBITDA.mData[i]
			if not ltd or not ebitda:
				self.mMorningstarLTDOnEBITDA.mData.append( '' )
				continue
			
			ratio = float( ltd ) / float( ebitda )
			self.mMorningstarLTDOnEBITDA.mData.append( '{:.02f}'.format( ratio ) )
					
		#---
			
		with open( self.SourceFileHTMLFinancialsMorningstarRatios(), newline='' ) as csvfile:
			reader = csv.reader( csvfile )
			
			for row in reader:
				if not row:
					continue
				
				if not row[0] and self.mMorningstarFinancialsYears is None:		# 2 lines have the same format, and the first one is the wanted one
					self.mMorningstarFinancialsYears = cDataMorningstar( row )
				elif row[0].startswith( 'Revenue' ) and row[0].endswith( 'Mil' ):
					self.mMorningstarFinancialsRevenue = cDataMorningstar( row, self.mMorningstarFinancialsYears )
				elif row[0].startswith( 'Net Income' ) and row[0].endswith( 'Mil' ):
					self.mMorningstarFinancialsNetIncome = cDataMorningstar( row, self.mMorningstarFinancialsYears )
				elif row[0].startswith( 'Dividends' ):
					self.mMorningstarFinancialsDividends = cDataMorningstar( row, self.mMorningstarFinancialsYears )
				elif row[0].startswith( 'Payout Ratio' ):
					self.mMorningstarFinancialsPayoutRatio = cDataMorningstar( row, self.mMorningstarFinancialsYears )
				elif row[0].startswith( 'Earnings' ):
					self.mMorningstarFinancialsEarnings = cDataMorningstar( row, self.mMorningstarFinancialsYears )
				elif row[0].startswith( 'Book Value Per Share' ):
					self.mMorningstarFinancialsBook = cDataMorningstar( row, self.mMorningstarFinancialsYears )
					
				elif row[0].startswith( 'Profitability' ):
					self.mMorningstarProfitabilityYears = cDataMorningstar( row )
				elif row[0].startswith( 'Return on Equity' ):
					self.mMorningstarProfitabilityROE = cDataMorningstar( row, self.mMorningstarProfitabilityYears )
				elif row[0].startswith( 'Return on Invested Capital' ):
					self.mMorningstarProfitabilityROI = cDataMorningstar( row, self.mMorningstarProfitabilityYears )
				elif row[0].startswith( 'Interest Coverage' ):
					self.mMorningstarProfitabilityIC = cDataMorningstar( row, self.mMorningstarProfitabilityYears )
					
				elif row[0].startswith( 'Key Ratios -> Growth' ):
					row = next( reader )
					self.mMorningstarGrowthYears = cDataMorningstar( row )
				elif row[0].startswith( 'Revenue %' ):
					row = next( reader )
					self.mMorningstarGrowthRevenue = cDataMorningstar( row, self.mMorningstarGrowthYears )	# YoY
				elif row[0].startswith( 'Net Income %' ):
					row = next( reader )
					self.mMorningstarGrowthNetIncome = cDataMorningstar( row, self.mMorningstarGrowthYears )	# YoY
				elif row[0].startswith( 'EPS %' ):
					row = next( reader )
					self.mMorningstarGrowthEarnings = cDataMorningstar( row, self.mMorningstarGrowthYears )	# YoY
					
				elif row[0].startswith( 'Free Cash Flow/Sales' ):
					self.mMorningstarCashFlowFCFOnSales = cDataMorningstar( row, self.mMorningstarProfitabilityYears )
			
				elif row[0].startswith( 'Liquidity/Financial Health' ):
					self.mMorningstarHealthYears = cDataMorningstar( row )
				elif row[0].startswith( 'Current Ratio' ):
					self.mMorningstarHealthCurrentRatio = cDataMorningstar( row, self.mMorningstarHealthYears )
				elif row[0].startswith( 'Debt/Equity' ):
					self.mMorningstarHealthDebtOnEquity = cDataMorningstar( row, self.mMorningstarHealthYears )
				
		for i, dividend in enumerate( self.mMorningstarFinancialsDividends.mData ):
			if not i:
				self.mMorningstarFinancialsGrowthDividends.mData.append( '' )
				continue
			if not dividend or not self.mMorningstarFinancialsDividends.mData[i-1]:
				self.mMorningstarFinancialsGrowthDividends.mData.append( '' )
				continue
			
			ratio = ( float( dividend ) - float( self.mMorningstarFinancialsDividends.mData[i-1] ) ) / abs( float( dividend ) )
			self.mMorningstarFinancialsGrowthDividends.mData.append( '{:.02f}'.format( ratio * 100 ) )
					
		for i, book in enumerate( self.mMorningstarFinancialsBook.mData ):
			if not i:
				self.mMorningstarFinancialsGrowthBook.mData.append( '' )
				continue
			if not book or not self.mMorningstarFinancialsBook.mData[i-1]:
				self.mMorningstarFinancialsGrowthBook.mData.append( '' )
				continue
			
			ratio = ( float( book ) - float( self.mMorningstarFinancialsBook.mData[i-1] ) ) / abs( float( book ) )
			self.mMorningstarFinancialsGrowthBook.mData.append( '{:.02f}'.format( ratio * 100 ) )
					
		#---
			
		html_content = ''
		with open( self.SourceFileHTMLFinancialsMorningstarValuation(), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		svaluation = BeautifulSoup( html_content, 'html5lib' )
		section = svaluation.find( 'a', attrs={'data-anchor': 'valuation'} ).parent
		
		self.mMorningstarValuationYears.SetTR( section, 'td', 'Calendar' )
			
		self.mMorningstarValuationP2S.SetTR( section, 'span', 'Price/Sales' )
		self.mMorningstarValuationPER.SetTR( section, 'span', 'Price/Earnings' )
		self.mMorningstarValuationP2CF.SetTR( section, 'span', 'Price/Cash Flow' )
		self.mMorningstarValuationP2B.SetTR( section, 'span', 'Price/Book' )
		self.mMorningstarValuationEVOnEBITDA.SetTR( section, 'span', 'Enterprise Value/EBITDA' )
		
		# sys.exit( 0 )




