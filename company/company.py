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

from datetime import datetime, date, time
from enum import Enum, auto
import os
# import requests
import shutil

# from bs4 import BeautifulSoup

from .data import cData

class cZoneBourse:
	class eAppletMode( Enum ):
		kStatic = auto()
		kDynamic = auto()
	
	def __init__( self, iCompany, iName, iCode, iSymbol ):
		self.mCompany = iCompany
		self.mName = iName
		self.mCode = iCode
		self.mSymbol = iSymbol
		
		self.mSoupSociety = None
		
		self.mSoupPER = None
		self.mSoupBNA = None
		self.mPrice = ''
		self.mPriceRealTime = ''
		self.mCurrency = ''
		
		self.mYears = cData()
		self.mRevenue = cData( iParent=self.mYears )
		self.mGrowthRevenue = cData( iParent=self.mYears )
		self.mNetIncome = cData( iParent=self.mYears )
		self.mGrowthNetIncome = cData( iParent=self.mYears )
		self.mEarnings = cData( iParent=self.mYears )
		self.mGrowthEarnings = cData( iParent=self.mYears, iComputeGrowthAverage=True )
		self.mDividends = cData( iParent=self.mYears )
		self.mGrowthDividends = cData( iParent=self.mYears, iComputeGrowthAverage=True )
		self.mYields = cData( iParent=self.mYears )
		
		self.mYieldCurrent = 0				# 0.0 < ... < 100.0
		self.mDividendsYield10Years = cData( iParent=self.mYears )
		self.mDividendsYield20Years = cData( iParent=self.mYears )
		self.mUrlDividendCalculator10Years = ''
		self.mUrlDividendCalculator20Years = ''
		
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
			applet_mode = 'dynamique2'
		return 'https://www.zonebourse.com/{}-{}/{}/'.format( self.mName, self.mCode, 'graphiques' )
		# return 'https://www.zonebourse.com/{}-{}/{}/&applet_mode={}'.format( self.mName, self.mCode, 'graphiques', applet_mode ) # '&applet_mode=' doesn't work anymore ... -_-
		
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
	
class cMorningstar:
	def __init__( self, iCompany, iSymbol, iRegion, iCity ):
		self.mCompany = iCompany
		self.mSymbol = iSymbol
		self.mRegion = iRegion
		self.mCity = iCity
		
		self.mISYears = cData()
		self.mEBITDA = cData( iParent=self.mISYears )
		
		self.mBSYears = cData()
		self.mLongTermDebt = cData( iParent=self.mBSYears )
		self.mLTDOnEBITDA = cData( iParent=self.mBSYears )
		
		self.mFinancialsYears = cData()
		self.mFinancialsRevenue = cData( iParent=self.mFinancialsYears )
		self.mFinancialsNetIncome = cData( iParent=self.mFinancialsYears )
		self.mFinancialsDividends = cData( iParent=self.mFinancialsYears )
		self.mFinancialsGrowthDividends = cData( iParent=self.mFinancialsYears, iComputeGrowthAverage=True )
		self.mFinancialsPayoutRatio = cData( iParent=self.mFinancialsYears )
		self.mFinancialsEarnings = cData( iParent=self.mFinancialsYears )
		self.mFinancialsBook = cData( iParent=self.mFinancialsYears )
		self.mFinancialsGrowthBook = cData( iParent=self.mFinancialsYears )
		
		self.mProfitabilityYears = cData()
		self.mProfitabilityROE = cData( iParent=self.mProfitabilityYears )
		self.mProfitabilityROI = cData( iParent=self.mProfitabilityYears )
		self.mProfitabilityIC = cData( iParent=self.mProfitabilityYears )
		self.mGrowthYears = cData()
		self.mGrowthRevenue = cData( iParent=self.mGrowthYears )
		self.mGrowthNetIncome = cData( iParent=self.mGrowthYears )
		self.mGrowthEarnings = cData( iParent=self.mGrowthYears, iComputeGrowthAverage=True )
		self.mCashFlowFCFOnSales = cData( iParent=self.mProfitabilityYears )
		self.mHealthYears = cData()
		self.mHealthCurrentRatio = cData( iParent=self.mHealthYears )
		self.mHealthDebtOnEquity = cData( iParent=self.mHealthYears )

		self.mQuoteBeta = 0.0
		self.mQuoteSector = ''
		self.mQuoteIndustry = ''
		
		self.mValuationYears = cData()
		self.mValuationP2S = cData( iParent=self.mValuationYears )
		self.mValuationPER = cData( iParent=self.mValuationYears )
		self.mValuationP2CF = cData( iParent=self.mValuationYears )
		self.mValuationP2B = cData( iParent=self.mValuationYears )
		self.mValuationEVOnEBITDA = cData( iParent=self.mValuationYears )
		
		self.mFinancialsDividendsYield = cData( iParent=self.mValuationYears )
		self.mYieldCurrent = 0				# 0.0 < ... < 100.0
		self.mFinancialsDividendsYield10Years = cData( iParent=self.mValuationYears )
		self.mFinancialsDividendsYield20Years = cData( iParent=self.mValuationYears )
		self.mUrlDividendCalculator10Years = ''
		self.mUrlDividendCalculator20Years = ''
		self.mFinancialsDividendsYears = cData( iParent=self.mValuationYears )
		
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
		
	def UrlQuote( self ):
		return 'https://www.morningstar.com/stocks/{}/{}/quote.html'.format( self.mCity, self.mSymbol.lower() )
	def FileNameQuote( self ):
		return '{}.{}.{}.html'.format( self.mCompany.Name(), self.mCompany.ISIN(), 'morningstar-quote' )
		
	def UrlValuation( self ):
		return 'https://www.morningstar.com/stocks/{}/{}/quote.html'.format( self.mCity, self.mSymbol.lower() )
	def FileNameValuation( self ):
		return '{}.{}.{}.html'.format( self.mCompany.Name(), self.mCompany.ISIN(), 'morningstar-valuation' )
		
	def UrlDividends( self ):
		return 'https://www.morningstar.com/stocks/{}/{}/quote.html'.format( self.mCity, self.mSymbol.lower() )
	def FileNameDividends( self ):
		return '{}.{}.{}.html'.format( self.mCompany.Name(), self.mCompany.ISIN(), 'morningstar-dividends' )

class cFinviz:
	def __init__( self, iCompany, iSymbol ):
		self.mCompany = iCompany
		self.mSymbol = iSymbol
		
		# string 'xx%'
		self.mBNAGrowth = { '-5': '', '0': '', '+1': '', '+5':'' }
		
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
		
		# string 'xx%'
		self.mGrowth = { '-5': '', '0': '', '+1': '', '+5':'' }
		self.mHistoric = [] # [ { 'date': date(), 'price': xxxx.xx }, {...}, ... ]
		
	def Symbol( self ):
		return self.mSymbol
		
	def Url( self ):
		if self.mCompany.ISIN() == 'GB0008847096':
			return 'https://uk.finance.yahoo.com/quote/{}/analysis?p={}'.format( self.mSymbol, self.mSymbol )
		else:
			return 'https://finance.yahoo.com/quote/{}/analysis?p={}'.format( self.mSymbol, self.mSymbol )
	def FileName( self ):
		return '{}.{}.yahoofinance.html'.format( self.mCompany.Name(), self.mCompany.ISIN() )
		
	def UrlHistoric( self ):
		start_date = date( 2019, 1, 1 )
		start_timestamp = datetime.combine( start_date, time() ).timestamp()
		now = datetime.now().date()
		stop_timestamp = datetime.combine( now, time() ).timestamp()
		return 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1wk&events=history'.format( self.mSymbol, int(start_timestamp), int(stop_timestamp) )
		# https://query1.finance.yahoo.com/v7/finance/download/SAN.PA?period1=1546560000&period2=1601769600&interval=1wk&events=history
	def FileNameHistoric( self ):
		return '{}.{}.yahoofinance-historic.csv'.format( self.mCompany.Name(), self.mCompany.ISIN() )
	
class cReuters:
	def __init__( self, iCompany, iSymbol ):
		self.mCompany = iCompany
		self.mSymbol = iSymbol
		
		# string 'xx'
		self.mBNAGrowth = { '-5': '', '-3': '', '-1': '' }
		
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
		
		self.mYears = []
		self.mPER = []
		self.mBNA = []
		self.mBNAGrowth = []
		self.mBNAGrowthAverage = 0
		self.mBNAGrowthAverageLast5Y = 0
		self.mDividend = []
		self.mDividendGrowth = []
		self.mDividendGrowthAverage = 0
		self.mDividendGrowthAverageLast5Y = 0
		self.mDividendYield = []
		
	def Name( self ):
		return self.mName
		
	def Url( self ):
		return 'https://www.boerse.de/fundamental-analyse/{}-Aktie/{}'.format( self.mName, self.mCompany.ISIN() )
	def FileName( self ):
		return '{}.{}.boerse.html'.format( self.mCompany.Name(), self.mCompany.ISIN() )
	
class cTradingSat:
	class cDividend:			#TODO: maybe move this to data.py or its own file ?
		class eType( Enum ):
			kNone = 0
			kDividend = 1
			kSplit = 2
			kActionOnly = 3		# add Exceptionel (BIC) ?
			
		def __init__( self ):
			self.mType = self.eType.kNone
			self.mYear = 0
			self.mPrice = 0

	def __init__( self, iCompany, iName ):
		self.mCompany = iCompany
		self.mName = iName
		
		self.mDividends = []
		
	def Name( self ):
		return self.mName
		
	def Url( self ):
		return 'https://www.tradingsat.com/{}-{}/dividende.html'.format( self.mName, self.mCompany.ISIN() )
	def FileName( self ):
		return '{}.{}.tradingsat.html'.format( self.mCompany.Name(), self.mCompany.ISIN() )
	
class cFinances:
	class cDividend:
		class eType( Enum ):
			kNone = 0
			kDividend = 1
			kSplit = 2
			kActionOnly = 3		# add Exceptionel (BIC) ?
			
		def __init__( self ):
			self.mType = self.eType.kNone
			self.mYear = 0
			self.mPrice = 0

	def __init__( self, iCompany, iName ):
		self.mCompany = iCompany
		self.mName = iName
		
		self.mDividends = []
		
	def Name( self ):
		return self.mName
		
	def Url( self ):
		return 'http://www.finances.net/dividendes/{}'.format( self.mName )
	def FileName( self ):
		return '{}.{}.finances.html'.format( self.mCompany.Name(), self.mCompany.ISIN() )
	
#---

class cNotation:
	def __init__( self ):
		self.mRawNotations = []
		self.mCoefficients = []
		self.mValidNotations = []
		self.mValidCoefficients = []
		self.mNote = 0
		self.mStars = 0
	
	def Compute( self, iNotation ):
		self.mRawNotations = iNotation
		if len( self.mRawNotations ) != 5:
			return
		
		self.mCoefficients = [4, 5, 5, 3, 1]
		valid_notations_coefficients = [ ( notation, coefficent ) for notation, coefficent in zip(self.mRawNotations, self.mCoefficients) if notation > 0 ]
		self.mValidNotations, self.mValidCoefficients = zip( *valid_notations_coefficients )

		assert( len( self.mValidNotations ) == len( self.mValidCoefficients ) and len( self.mValidNotations ) > 0 )

		notation_by_coef = [ notation * coefficent for notation, coefficent in zip(self.mValidNotations, self.mValidCoefficients) ]
		self.mNote = sum( notation_by_coef ) / sum( self.mValidCoefficients )
		
		if self.mNote >= 9.0:
			self.mStars = 4
		elif self.mNote >= 8.0:
			self.mStars = 3
		elif self.mNote >= 7.0:
			self.mStars = 2
		elif self.mNote >= 5.0:
			self.mStars = 1
	
	def StarsCount( self ):
		return self.mStars
	
	def Note( self ):
		return self.mNote

class cCompany:
	def __init__( self, iISIN, iZBName, iZBCode, iZBSymbol, iRawNotation, iZone, iMorningstarRegion, iMorningstarX, iTradingViewSymbol, iYFSymbol, iRSymbol, iFVSymbol, iTSName, iFCName ):
		self.mISIN = iISIN
		self.mName = iZBName
		self.mZone = iZone # eu/us
		
		self.mZoneBourse = cZoneBourse( self, iZBName, iZBCode, iZBSymbol )
		self.mFinviz = cFinviz( self, iFVSymbol )
		self.mMorningstar = cMorningstar( self, iZBSymbol, iMorningstarRegion, iMorningstarX )	# ( ..., fra/gbr/usa/..., xpar/xlon/... )
		self.mYahooFinance = cYahooFinance( self, iYFSymbol )
		self.mReuters = cReuters( self, iRSymbol )
		self.mBoerse = cBoerse( self, iZBName )	# use the same name as ZoneBourse, may use anything actually
		self.mTradingSat = cTradingSat( self, iTSName )
		self.mFinances = cFinances( self, iFCName )
		
		#---
		
		self.mTradingViewSymbol = iTradingViewSymbol	# NYSE:MMM		# Not use yet
		
		self.mDataPath = ''
		self.mImgDirRelativeToHTML = ''
		self.mGroup = ''
		self.mInvested = None
		self.mNotation = self._ComputeNotation( iRawNotation )
		
		self.mInvestment = 0.0
		self.mStartingYield = 0.0
		self.mDividendGrowthRate = 0.0
		self.mYearsToHold = 0
		
	#---
	
	def Group( self, iGroup ):
		self.mGroup = iGroup
		
	def ISIN( self ):
		return self.mISIN
	def Name( self ):
		return self.mName
	def Zone( self ):
		return self.mZone
	
	#---
	
	def Invested( self, iInvested=None ):
		if iInvested is None:
			return self.mInvested
		
		previous_value = self.mInvested
		self.mInvested = iInvested
		return previous_value
	
	def Notation( self ):
		return self.mNotation
	
	def _ComputeNotation( self, iRawNotation ):
		notation = cNotation()
		notation.Compute( iRawNotation )

		return notation
	
	def DataPath( self, iPath=None ):
		if iPath is None:
			return self.mDataPath
		
		previous_value = self.mDataPath
		self.mDataPath = iPath
		return previous_value
	
	def OutputImgPathRelativeToHTMLFile( self, iPath=None ):
		if iPath is None:
			return self.mImgDirRelativeToHTML
		
		previous_value = self.mImgDirRelativeToHTML
		self.mImgDirRelativeToHTML = iPath
		return previous_value
	
	#---
	
	def DataPathFile( self, iFileName ):
		return self.mDataPath / iFileName
	
	def OutputImgPathFileRelativeToHTMLFile( self, iFileName ):
		return '{}/{}'.format( self.mImgDirRelativeToHTML, iFileName )	# Always '/' as it's for html
	
	#---
	
	def UrlDividendCalculator( self, iYield, iGrowth, iYears ):
		self.mInvestment = 10000
		self.mStartingYield = iYield
		self.mDividendGrowthRate = iGrowth
		self.mYearsToHold = iYears
		
		url = 'http://www.dividend-calculator.com/annually.php?yield={:.2f}&yieldgrowth={:.2f}&shares=100&price=100&years={}&do=Calculate'
		return url.format( iYield, iGrowth, iYears )
	
	def AskDividendCalculatorProjection( self, iUrl ):
		# req = requests.get( iUrl, headers={ 'User-Agent' : 'Mozilla/5.0' } )
		
		# soup = BeautifulSoup( req.text, 'html5lib' )
		# results = soup.find( string='With Reinvestment' ).find_parent().find_next_sibling( 'p' ).find_all( 'b' )
		# cost_start = results[0].string
		# cost_stop = results[1].string
		# annual_average = results[4].string.replace( '%', '' )
		
		# return annual_average
		
		data = []
		for _ in range( self.mYearsToHold ):
			if not data:
				data.append( self._DividendCalculator( self.mInvestment, self.mStartingYield, 0 ) )
				continue
			
			previous_data = data[-1]
			data.append( self._DividendCalculator( previous_data[3], previous_data[1], self.mDividendGrowthRate ) )
		
		growth = ( data[-1][3] - self.mInvestment ) / self.mInvestment
		annual_average = growth / self.mYearsToHold
		return '{:.2f}'.format( annual_average * 100.0 )
	
	def _DividendCalculator( self, iInvestment, iYield, iGrowth ):
		investment = iInvestment
		yield_ = iYield + iYield * iGrowth/100.0
		income = investment * yield_/100.0
		total = investment + income
		return ( investment, yield_, income, total )
	
	#---
	
	def WriteImages( self, iOutputPath ):
		# print( 'WriteImages: {}'.format( self.mName ) )
		
		#TOIMPROVE: with tuple/dict/... like ichimoku (?)
		filename = self.mZoneBourse.FileNamePricesSimple( 9999 )
		shutil.copy( self.DataPathFile( filename ), iOutputPath / self.OutputImgPathFileRelativeToHTMLFile( filename ) )
		filename = self.mZoneBourse.FileNamePricesSimple( 10 )
		shutil.copy( self.DataPathFile( filename ), iOutputPath / self.OutputImgPathFileRelativeToHTMLFile( filename ) )
		filename = self.mZoneBourse.FileNamePricesSimple( 5 )
		shutil.copy( self.DataPathFile( filename ), iOutputPath / self.OutputImgPathFileRelativeToHTMLFile( filename ) )
		filename = self.mZoneBourse.FileNamePricesSimple( 2 )
		shutil.copy( self.DataPathFile( filename ), iOutputPath / self.OutputImgPathFileRelativeToHTMLFile( filename ) )
		
		filenames = self.mZoneBourse.FileNamesPricesIchimoku()
		shutil.copy( self.DataPathFile( filenames[0] ), iOutputPath / self.OutputImgPathFileRelativeToHTMLFile( filenames[0] ) )
		shutil.copy( self.DataPathFile( filenames[1] ), iOutputPath / self.OutputImgPathFileRelativeToHTMLFile( filenames[1] ) )
		shutil.copy( self.DataPathFile( filenames[2] ), iOutputPath / self.OutputImgPathFileRelativeToHTMLFile( filenames[2] ) )
	