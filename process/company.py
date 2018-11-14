#!/usr/bin/python3

import os
import re
import sys
import csv
import shutil
import locale
import requests
from enum import Enum, auto
from datetime import date, datetime

from bs4 import BeautifulSoup

from download.zonebourse import cZoneBourse as cDLZoneBourse
from download.finviz import cFinviz as cDLFinviz
from download.morningstar import cMorningstar as cDLMorningstar
from download.yahoofinance import cYahooFinance as cDLYahooFinance
from download.reuters import cReuters as cDLReuters
from download.boerse import cBoerse as cDLBoerse
from download.tradingsat import cTradingSat as cDLTradingSat
from download.finances import cFinances as cDLFinances

class cDataMorningstar:
	def __init__( self, iRow=None, iParent=None, iComputeGrowthAverage=False ):
		self.mData = []
		
		self.mTTM = ''
		self.mLatestQuarter = ''
		
		self.mCurrent = ''
		self.m5Years = ''
		self.mIndex = ''
		
		self.mComputeGrowthAverage=iComputeGrowthAverage
		self.mGrowthAverage = ''
		
		self.mParent = iParent
		
		if iRow is not None:
			self.SetRow( iRow )
	
	def __repr__(self):
		return 'cDataMorningstar( [{}], "{}", "{}" )'.format( ', '.join( map( str, self.mData ) ), self.mTTM, self.mLatestQuarter )
	
	def ComputeAverage( self, iData, iYears=8 ):
		if not iData:
			return
		
		data = []
		for value in iData:
			if not value:
				continue
			data.append( float( value ) )
			
		data = sorted( data[-1*iYears:] )
		if len( data ) >= 5:
			del( data[0] )
			del( data[-1] )
		
		return sum( data ) / float( len( data ) )
	
	def Update( self ):
		if self.mComputeGrowthAverage:
			self.mGrowthAverage = '{:.02f}'.format( self.ComputeAverage( self.mData ) )
	
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
		
		self.Update()
			
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
		
		self.Update()
			
	def _FixLocale2( self, iString ):
		return iString.replace( ',', '' ).replace( '—', '' )
		
#---

class cZoneBourse:
	class eAppletMode( Enum ):
		kStatic = auto()
		kDynamic = auto()
	
	def __init__( self, iCompany, iName, iCode, iSymbol ):
		self.mCompany = iCompany
		self.mName = iName
		self.mCode = iCode
		self.mSymbol = iSymbol
		
	def Name( self ):
		return self.mName
	def Code( self ):
		return self.mCode
	def Symbol( self ):
		return self.mSymbol
		
	def UrlData( self ):
		return 'https://www.zonebourse.com/{}-{}/{}/'.format( self.mName, self.mCode, 'fondamentaux' )
	def FileNameData( self ):
		return '{}.{}.zonebourse-data.html'.format( self.mCompany.Name(), self.mCompany.ISIN() )
		
	def UrlSociety( self ):
		return 'https://www.zonebourse.com/{}-{}/{}/'.format( self.mName, self.mCode, 'societe' )
	def FileNameSociety( self ):
		return '{}.{}.zonebourse-society.html'.format( self.mCompany.Name(), self.mCompany.ISIN() )
		
	def UrlGraphic( self, iAppletMode ):
		applet_mode = 'statique'
		if iAppletMode is self.eAppletMode.kDynamic:
			applet_mode = 'dynamic2'
		return 'https://www.zonebourse.com/{}-{}/{}/&applet_mode={}'.format( self.mName, self.mCode, 'graphiques', applet_mode )
		
	def UrlPricesSimple( self, iDuration, iWidth, iHeight ):
		return 'https://www.zonebourse.com/zbcache/charts/ObjectChart.aspx?Name={0}&Type=Custom&Intraday=1&Width={2}&Height={3}&Cycle=NONE&Duration={1}&TopMargin=10&Render=Candle&ShowName=0'.format( self.mCode, iDuration, iWidth, iHeight )
	def FileNamePricesSimple( self, iYears ):
		return '{}.{}.{}.{}.gif'.format( self.mCompany.Name(), self.mCompany.ISIN(), self.mCode, iYears )
	
	def UrlPricesIchimoku( self ):
		return self.UrlGraphic( self.eAppletMode.kDynamic )
	def FileNamesPricesIchimoku( self ):
		return ( '{}.{}.{}.{}-{}.png'.format( self.mCompany.Name(), self.mCompany.ISIN(), self.mCode, 'content', 'ichimoku' ),
				'{}.{}.{}.{}-{}.png'.format( self.mCompany.Name(), self.mCompany.ISIN(), self.mCode, 'prices', 'ichimoku' ),
				'{}.{}.{}.{}-{}.png'.format( self.mCompany.Name(), self.mCompany.ISIN(), self.mCode, 'times', 'ichimoku' ) )
	
class cFinviz:
	def __init__( self, iCompany, iSymbol ):
		self.mCompany = iCompany
		self.mSymbol = iSymbol
		
	def Symbol( self ):
		return self.mSymbol
		
	def Url( self ):
		return 'https://finviz.com/quote.ashx?t={}'.format( self.mSymbol )
	def FileName( self ):
		return '{}.{}.finviz.html'.format( self.mCompany.Name(), self.mCompany.ISIN() )
	
class cYahooFinance:
	def __init__( self, iCompany, iSymbol ):
		self.mCompany = iCompany
		self.mSymbol = iSymbol
		
	def Symbol( self ):
		return self.mSymbol
		
	def Url( self ):
		if self.mCompany.ISIN() == 'GB0008847096':
			return 'https://uk.finance.yahoo.com/quote/{}/analysis?p={}'.format( self.mSymbol, self.mSymbol )
		else:
			return 'https://finance.yahoo.com/quote/{}/analysis?p={}'.format( self.mSymbol, self.mSymbol )
	def FileName( self ):
		return '{}.{}.yahoofinance.html'.format( self.mCompany.Name(), self.mCompany.ISIN() )
	
class cReuters:
	def __init__( self, iCompany, iSymbol ):
		self.mCompany = iCompany
		self.mSymbol = iSymbol
		
	def Symbol( self ):
		return self.mSymbol
		
	def Url( self ):
		return 'https://www.reuters.com/finance/stocks/financial-highlights/{}'.format( self.mSymbol )
	def FileName( self ):
		return '{}.{}.reuters.html'.format( self.mCompany.Name(), self.mCompany.ISIN() )
	
class cBoerse:
	def __init__( self, iCompany, iName ):
		self.mCompany = iCompany
		self.mName = iName
		
	def Name( self ):
		return self.mName
		
	def Url( self ):
		return 'https://www.boerse.de/fundamental-analyse/{}-Aktie/{}'.format( self.mName, self.mCompany.ISIN() )
	def FileName( self ):
		return '{}.{}.boerse.html'.format( self.mCompany.Name(), self.mCompany.ISIN() )
	
class cTradingSat:
	def __init__( self, iCompany, iName ):
		self.mCompany = iCompany
		self.mName = iName
		
	def Name( self ):
		return self.mName
		
	def Url( self ):
		return 'https://www.tradingsat.com/{}-{}/dividende.html'.format( self.mName, self.mCompany.ISIN() )
	def FileName( self ):
		return '{}.{}.tradingsat.html'.format( self.mCompany.Name(), self.mCompany.ISIN() )
	
class cFinances:
	def __init__( self, iCompany, iName ):
		self.mCompany = iCompany
		self.mName = iName
		
	def Name( self ):
		return self.mName
		
	def Url( self ):
		return 'http://www.finances.net/dividendes/{}'.format( self.mName )
	def FileName( self ):
		return '{}.{}.finances.html'.format( self.mCompany.Name(), self.mCompany.ISIN() )
	
class cMorningstar:
	def __init__( self, iCompany, iSymbol, iRegion, iCity ):
		self.mCompany = iCompany
		self.mSymbol = iSymbol
		self.mRegion = iRegion
		self.mCity = iCity
		
	def Symbol( self ):
		return self.mSymbol
	def Region( self ):
		return self.mRegion
	def City( self ):
		return self.mCity
		
	def UrlIncomeStatement( self ):
		if self.mCity == 'xetr':
			return 'http://financials.morningstar.com/income-statement/is.html?t={}:{}&region={}&culture=en-US'.format( self.mCity, self.mSymbol, self.mRegion )
		return 'http://financials.morningstar.com/income-statement/is.html?t={}&region={}&culture=en-US'.format( self.mSymbol, self.mRegion )
	def FileNameIncomeStatement( self ):
		return '{}.{}.{}.csv'.format( self.mCompany.Name(), self.mCompany.ISIN(), 'morningstar-income-statement' )
		
	def UrlBalanceSheet( self ):
		if self.mCity == 'xetr':
			return 'http://financials.morningstar.com/balance-sheet/bs.html?t={}:{}&region={}&culture=en-US'.format( self.mCity, self.mSymbol, self.mRegion )
		return 'http://financials.morningstar.com/balance-sheet/bs.html?t={}&region={}&culture=en-US'.format( self.mSymbol, self.mRegion )
	def FileNameBalanceSheet( self ):
		return '{}.{}.{}.csv'.format( self.mCompany.Name(), self.mCompany.ISIN(), 'morningstar-balance-sheet' )
		
	def UrlRatios( self ):
		if self.mCity == 'xetr':
			return 'http://financials.morningstar.com/ratios/r.html?t={}:{}&region={}&culture=en-US'.format( self.mCity, self.mSymbol, self.mRegion )
		return 'http://financials.morningstar.com/ratios/r.html?t={}&region={}&culture=en-US'.format( self.mSymbol, self.mRegion )
	def FileNameRatios( self ):
		return '{}.{}.{}.csv'.format( self.mCompany.Name(), self.mCompany.ISIN(), 'morningstar-ratios' )
		
	def UrlValuation( self ):
		return 'https://www.morningstar.com/stocks/{}/{}/quote.html'.format( self.mCity, self.mSymbol.lower() )
	def FileNameValuation( self ):
		return '{}.{}.{}.html'.format( self.mCompany.Name(), self.mCompany.ISIN(), 'morningstar-valuation' )
		
	def UrlDividends( self ):
		return 'https://www.morningstar.com/stocks/{}/{}/quote.html'.format( self.mCity, self.mSymbol.lower() )
	def FileNameDividends( self ):
		return '{}.{}.{}.html'.format( self.mCompany.Name(), self.mCompany.ISIN(), 'morningstar-dividends' )

class cCompany:
	def __init__( self, iISIN, iZBName, iZBCode, iZBSymbol, iMorningstarRegion, iMorningstarX, iTradingViewSymbol, iYFSymbol, iRSymbol, iFVSymbol, iTSName, iFCName ):
		self.mISIN = iISIN
		self.mName = iZBName
		
		self.mZoneBourse = cZoneBourse( self, iZBName, iZBCode, iZBSymbol )
		self.mFinviz = cFinviz( self, iFVSymbol )
		self.mMorningstar = cMorningstar( self, iZBSymbol, iMorningstarRegion, iMorningstarX )
		self.mYahooFinance = cYahooFinance( self, iYFSymbol )
		self.mReuters = cReuters( self, iRSymbol )
		self.mBoerse = cBoerse( self, iZBName )
		self.mTradingSat = cTradingSat( self, iTSName )
		self.mFinances = cFinances( self, iFCName )
		
		#---
		
		self.mZBName = iZBName			# ZB = ZoneBourse
		self.mZBCode = iZBCode
		self.mZBSymbol = iZBSymbol

		self.mMorningstarSymbol = iZBSymbol
		self.mMorningstarRegion = iMorningstarRegion	# fra/gbr/usa/...
		self.mMorningstarX = iMorningstarX				# xpar/xlon/...
		
		self.mTradingViewSymbol = iTradingViewSymbol	# NYSE:MMM
		
		self.mYFSymbol = iYFSymbol		# YF = Yahoo Finance
		self.mFVSymbol = iFVSymbol		# FV = FinViz
		self.mRSymbol = iRSymbol		# R = Reuters
		
		self.mTSName = iTSName			# TS = TradingSat
		self.mBName = iZBName			# B = boerse (use the same name as TradingSat, may use anything in fact)
		
		self.mFCName = iFCName			# FC = Finances.net
		
		self.mDataPath = ''
		self.mOutputPath = ''
		self.mOutputImgPath = ''
		self.mImgDirRelativeToHTML = ''
		self.mGroup = ''
		
	#---
	
	def Group( self, iGroup ):
		self.mGroup = iGroup
		
	def ISIN( self ):
		return self.mISIN
	def Name( self ):
		return self.mName
	
	#---
	
	def DataPath( self, iDirectory=None ):
		if iDirectory is None:
			return self.mDataPath
		
		previous_value = self.mDataPath
		self.mDataPath = iDirectory
		return previous_value
	
	def OutputPath( self, iOutputPath=None, iOutputImgPath=None ):
		if iOutputPath is None and iOutputImgPath is None:
			return ( self.mOutputPath, self.mOutputImgPath )
		
		previous_value = ( self.mOutputPath, self.mOutputImgPath )
		if iOutputPath is not None:
			self.mOutputPath = iOutputPath
		if iOutputImgPath is not None:
			self.mOutputImgPath = iOutputImgPath
			
		self.mImgDirRelativeToHTML = os.path.relpath( self.mOutputImgPath, self.mOutputPath )
		
		return previous_value
		
	#---
	
	def DataPathFile( self, iFileName ):
		return os.path.join( self.mDataPath, iFileName )
	
	def OutputPathFile( self, iFileName ):
		return os.path.join( self.mOutputPath, iFileName )
	
	def OutputImgPathFile( self, iFileName ):
		return os.path.join( self.mOutputImgPath, iFileName )
	
	def OutputImgPathFileRelativeToHTMLFile( self, iFileName ):
		return '{}/{}'.format( self.mImgDirRelativeToHTML, iFileName )	# Always '/' as it's for html
	
	#---
	
	@staticmethod
	def Downloads( iBrowser, iCompanies ):
		for i, company in enumerate( iCompanies, start=1 ):
			print( 'Download ({}/{}): {} ...'.format( i, len( iCompanies ), company.Name() ) )
			company.Download( iBrowser )
	
	def Download( self, iBrowser ):
		# print( 'Download: {}'.format( self.mName ) )
		
		dl = cDLZoneBourse()
		dl.Download( iBrowser, self )
		dl = cDLFinviz()
		dl.Download( iBrowser, self )
		dl = cDLMorningstar()
		dl.Download( iBrowser, self )
		dl = cDLYahooFinance()
		dl.Download( iBrowser, self )
		dl = cDLReuters()
		dl.Download( iBrowser, self )
		dl = cDLBoerse()
		dl.Download( iBrowser, self )
		dl = cDLTradingSat()
		dl.Download( iBrowser, self )
		dl = cDLFinances()
		dl.Download( iBrowser, self )
	
	#---
	
	def SourceUrlDividendCalculator( self, iYield, iGrowth, iYears ):
		url = 'http://www.dividend-calculator.com/annually.php?yield={:.2f}&yieldgrowth={:.2f}&shares=100&price=100&years={}&do=Calculate'
		return url.format( iYield, iGrowth, iYears )
	
	def AskDividendCalculatorProjection( self, iUrl ):
		req = requests.get( iUrl, headers={ 'User-Agent' : 'Mozilla/5.0' } )
		
		soup = BeautifulSoup( req.text, 'html5lib' )
		results = soup.find( string='With Reinvestment' ).find_parent().find_next_sibling( 'p' ).find_all( 'b' )
		cost_start = results[0].string
		cost_stop = results[1].string
		annual_average = results[4].string.replace( '%', '' )
		
		return annual_average
	
	#---
	
	def WriteImages( self ):
		#TOIMPROVE: with tuple/dict/... like ichimoku (?)
		filename = self.mZoneBourse.FileNamePricesSimple( 9999 )
		shutil.copy( self.DataPathFile( filename ), self.OutputImgPathFile( filename ) )
		filename = self.mZoneBourse.FileNamePricesSimple( 10 )
		shutil.copy( self.DataPathFile( filename ), self.OutputImgPathFile( filename ) )
		filename = self.mZoneBourse.FileNamePricesSimple( 5 )
		shutil.copy( self.DataPathFile( filename ), self.OutputImgPathFile( filename ) )
		filename = self.mZoneBourse.FileNamePricesSimple( 2 )
		shutil.copy( self.DataPathFile( filename ), self.OutputImgPathFile( filename ) )
		
		filenames = self.mZoneBourse.FileNamesPricesIchimoku()
		shutil.copy( self.DataPathFile( filenames[0] ), self.OutputImgPathFile( filenames[0] ) )
		shutil.copy( self.DataPathFile( filenames[1] ), self.OutputImgPathFile( filenames[1] ) )
		shutil.copy( self.DataPathFile( filenames[2] ), self.OutputImgPathFile( filenames[2] ) )
	
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
		self.mSFinancialsZB = None
		self.mSFinancialsZBTable = None
		self.mSSocietyZB = None
		
		self.mBNAGrowth = []
		self.mBNAGrowthAverage = 0
		self.mDividendsGrowth = []
		self.mDividendsGrowthAverage = 0	# 0.0 < ... < 1.0
		self.mYieldCurrent = 0				# 0.0 < ... < 100.0
		
		#---
		
		html_content = ''
		with open( self.DataPathFile( self.mZoneBourse.FileNameData() ), 'r', encoding='utf-8' ) as fd:
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
		with open( self.DataPathFile( self.mZoneBourse.FileNameSociety() ), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		self.mSSocietyZB = BeautifulSoup( html_content, 'html5lib' )
		
	def FillFinviz( self ):
		self.mSFinancialsFV = None
		self.mBNAGrowthFV5 = {}				# string 'xx%'
		
		self.mBNAGrowthFV5['-5'] = '-'
		self.mBNAGrowthFV5['0'] = '-'
		self.mBNAGrowthFV5['+1'] = '-'
		self.mBNAGrowthFV5['+5'] = '-'
		
		#---
		
		if not self.mFVSymbol:
			return
			
		html_content = ''
		with open( self.DataPathFile( self.mFinviz.FileName() ), 'r', encoding='utf-8' ) as fd:
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
		self.mSFinancialsR = None
		self.mBNAGrowthR5 = {}				# string 'xx'
		
		self.mBNAGrowthR5['-1'] = '-'
		self.mBNAGrowthR5['-3'] = '-'
		self.mBNAGrowthR5['-5'] = '-'
		
		#---
		
		if not self.mRSymbol:
			return
			
		html_content = ''
		with open( self.DataPathFile( self.mReuters.FileName() ), 'r', encoding='utf-8' ) as fd:
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
		self.mSFinancialsYF = None
		self.mGrowthYF5 = {}				# string 'xx%'
		self.mGrowthYF5['-5'] = '-'
		self.mGrowthYF5['0'] = '-'
		self.mGrowthYF5['+1'] = '-'
		self.mGrowthYF5['+5'] = '-'
		
		#---
		
		if not self.mYFSymbol:
			return
			
		html_content = ''
		with open( self.DataPathFile( self.mYahooFinance.FileName() ), 'r', encoding='utf-8' ) as fd:
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
		self.mSFinancialsB = None
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
		
		#---
		
		if not self.mBName:
			return
			
		html_content = ''
		with open( self.DataPathFile( self.mBoerse.FileName() ), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		self.mSFinancialsB = BeautifulSoup( html_content, 'html5lib' )
		
		#---
		
		if not self.mSFinancialsB:
			return
		if self.mSFinancialsB.find( string=re.compile('Bilanz \(\)') ):
			return
		if self.mSFinancialsB.find( id='rentabilitaet' ) is None:
			return
		if self.mSFinancialsB.find( id='kennzahlen' ) is None:
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
		self.mSDividendsFC = None
		
		if not self.mFCName:
			return
			
		html_content = ''
		with open( self.DataPathFile( self.mFinances.FileName() ), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		self.mSDividendsFC = BeautifulSoup( html_content, 'html5lib' )
			
	def FillTradingSat( self ):
		self.mSDividendsTS = None
		
		if not self.mTSName:
			return
			
		html_content = ''
		with open( self.DataPathFile( self.mTradingSat.FileName() ), 'r', encoding='utf-8' ) as fd:
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
		self.mMorningstarFinancialsGrowthDividends = cDataMorningstar( iComputeGrowthAverage=True )
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
		
		self.mMorningstarFinancialsDividendsYield = cDataMorningstar( iParent=self.mMorningstarValuationYears )
		self.mMorningstarFinancialsDividendsYield10Years = cDataMorningstar( iParent=self.mMorningstarValuationYears )
		self.mMorningstarFinancialsDividendsYield20Years = cDataMorningstar( iParent=self.mMorningstarValuationYears )
		self.mUrlMorningstarDividendCalculator10Years = ''
		self.mUrlMorningstarDividendCalculator20Years = ''
		
		self.mMorningstarDividendNextDates = []
		
		if not self.mMorningstarRegion:
			return
			
		with open( self.DataPathFile( self.mMorningstar.FileNameIncomeStatement() ), newline='' ) as csvfile:
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
		
		with open( self.DataPathFile( self.mMorningstar.FileNameBalanceSheet() ), newline='' ) as csvfile:
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
			self.mMorningstarLTDOnEBITDA.Update()
			
		#---
			
		with open( self.DataPathFile( self.mMorningstar.FileNameRatios() ), newline='' ) as csvfile:
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
					self.mMorningstarGrowthEarnings = cDataMorningstar( row, self.mMorningstarGrowthYears, iComputeGrowthAverage=True )	# YoY
					
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
			
			previous_dividend = self.mMorningstarFinancialsDividends.mData[i-1]
			ratio = ( float( dividend ) - float( previous_dividend ) ) / abs( float( previous_dividend ) )
			self.mMorningstarFinancialsGrowthDividends.mData.append( '{:.02f}'.format( ratio * 100 ) )
			self.mMorningstarFinancialsGrowthDividends.Update()
					
		for i, book in enumerate( self.mMorningstarFinancialsBook.mData ):
			if not i:
				self.mMorningstarFinancialsGrowthBook.mData.append( '' )
				continue
			if not book or not self.mMorningstarFinancialsBook.mData[i-1]:
				self.mMorningstarFinancialsGrowthBook.mData.append( '' )
				continue
			
			previous_book = self.mMorningstarFinancialsBook.mData[i-1]
			ratio = ( float( book ) - float( previous_book ) ) / abs( float( previous_book ) )
			self.mMorningstarFinancialsGrowthBook.mData.append( '{:.02f}'.format( ratio * 100 ) )
			self.mMorningstarFinancialsGrowthBook.Update()
		
		#---
			
		html_content = ''
		with open( self.DataPathFile( self.mMorningstar.FileNameValuation() ), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		svaluation = BeautifulSoup( html_content, 'html5lib' )
		section = svaluation.find( 'a', attrs={'data-anchor': 'valuation'} ).parent		# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#the-keyword-arguments
		
		self.mMorningstarValuationYears.SetTR( section, 'td', 'Calendar' )
			
		self.mMorningstarValuationP2S.SetTR( section, 'span', 'Price/Sales' )
		self.mMorningstarValuationPER.SetTR( section, 'span', 'Price/Earnings' )
		self.mMorningstarValuationP2CF.SetTR( section, 'span', 'Price/Cash Flow' )
		self.mMorningstarValuationP2B.SetTR( section, 'span', 'Price/Book' )
		self.mMorningstarValuationEVOnEBITDA.SetTR( section, 'span', 'Enterprise Value/EBITDA' )
		
		#---
		
		html_content = ''
		with open( self.DataPathFile( self.mMorningstar.FileNameDividends() ), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		soup = BeautifulSoup( html_content, 'html5lib' )
		
		div = soup.find( id='sal-components-dividends' ).find( class_='dividend-yield' ).find_all( 'div' )[-1]
		s = div.string.replace( ',', '.' ).replace( '%', '' ).replace( '-', '' ).replace( '—', '' )
		self.mMorningstarFinancialsDividendsYield.mGrowthAverage = s if s else '0'
		self.mMorningstarFinancialsDividendsYield.mCurrent = '{:.02f}'.format( float( s ) * 0.7 ) if s else '0'	# Remove 30% for PS/Impots
		
		self.mUrlMorningstarDividendCalculator10Years = self.SourceUrlDividendCalculator( float( self.mMorningstarFinancialsDividendsYield.mGrowthAverage ), float( self.mMorningstarFinancialsGrowthDividends.mGrowthAverage ), 10 )
		annual_average = self.AskDividendCalculatorProjection( self.mUrlMorningstarDividendCalculator10Years )
		self.mMorningstarFinancialsDividendsYield10Years.mGrowthAverage = annual_average
		self.mMorningstarFinancialsDividendsYield10Years.mCurrent = '{:.02f}'.format( float( annual_average ) * 0.7 )	# Remove 30% for PS/Impots
		
		self.mUrlMorningstarDividendCalculator20Years = self.SourceUrlDividendCalculator( float( self.mMorningstarFinancialsDividendsYield.mGrowthAverage ), float( self.mMorningstarFinancialsGrowthDividends.mGrowthAverage ), 20 )
		annual_average = self.AskDividendCalculatorProjection( self.mUrlMorningstarDividendCalculator20Years )
		self.mMorningstarFinancialsDividendsYield20Years.mGrowthAverage = annual_average
		self.mMorningstarFinancialsDividendsYield20Years.mCurrent = '{:.02f}'.format( float( annual_average ) * 0.7 )	# Remove 30% for PS/Impots
		
		#---
		
		tr = soup.find( id='sal-components-dividends' ).find( 'table', class_='dividends-recent-table' ).find( 'tr', attrs={'ng-show': re.compile( 'upcomingDate.length' ) } )
		trs = tr.find_next_siblings( 'tr' )
		next_dates = []
		for tr in trs:
			next_date = tr.find( 'td' ).get_text( strip=True ).replace( '*', '' )	# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#get-text
			next_date = datetime.strptime( next_date, '%b %d, %Y' ).date()
			if next_date > date.today():
				self.mMorningstarDividendNextDates.append( next_date )
		
		self.mMorningstarDividendNextDates.reverse()
		
		# sys.exit( 0 )




