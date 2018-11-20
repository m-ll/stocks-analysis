#!/usr/bin/env python3

import copy

from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style

class cZoneBourse:
	def __init__( self ):
		pass
	
	def Parse( self, iCompany ):
		print( '	ZoneBourse ...' )

		if not iCompany.mZoneBourse.Name():
			print( Fore.CYAN + '	skipping ... (no id)' )
			return

		#---

		self._ParseSociety( iCompany )
		
		html_content = ''
		with open( iCompany.DataPathFile( iCompany.mZoneBourse.FileNameData() ), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		soup = BeautifulSoup( html_content, 'html5lib' )
		
		self._ParseData( iCompany, soup )
		self._ParsePrice( iCompany, soup )
		self._ParseGraphics( iCompany, soup )
			
	def _ParseSociety( self, iCompany ):
		html_content = ''
		with open( iCompany.DataPathFile( iCompany.mZoneBourse.FileNameSociety() ), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		soup = BeautifulSoup( html_content, 'html5lib' )
		
		#---
		
		root = soup.find( 'table', class_='tabElemNoBor' ).find( 'td', class_='std_txt' )
		iCompany.mZoneBourse.mSoupSociety = copy.copy( root )
		
	def _ComputeCroissanceTr( self, iTr ):
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

	def _ComputeGrowth( self, iData, iDataGrowth ):
		for i, revenue in enumerate( iData.mData ):
			if not i:
				iDataGrowth.mData.append( '' )
				continue
			if not revenue or not iData.mData[i-1]:
				iDataGrowth.mData.append( '' )
				continue
			
			previous_revenue = iData.mData[i-1]
			ratio = ( float( revenue ) - float( previous_revenue ) ) / abs( float( previous_revenue ) )
			iDataGrowth.mData.append( '{:.02f}'.format( ratio * 100 ) )
			
		data = [ iData.mData[-1] ] + iData.mDataEstimated
		for i, revenue in enumerate( data ):
			if not i:
				iDataGrowth.mDataEstimated.append( '' )
				continue
			if not revenue or not data[i-1]:
				iDataGrowth.mDataEstimated.append( '' )
				continue
			
			previous_revenue = data[i-1]
			ratio = ( float( revenue ) - float( previous_revenue ) ) / abs( float( previous_revenue ) )
			iDataGrowth.mDataEstimated.append( '{:.02f}'.format( ratio * 100 ) )
			
		del iDataGrowth.mDataEstimated[0]
			
		iDataGrowth.Update()
		
	
	def _ParseData( self, iCompany, iSoup ):
		root = iSoup.find( 'table', class_='BordCollapseYear' )
		if not root:
			return
			
		iCompany.mZoneBourse.mSoupData = copy.copy( root )
			
		for tr in iCompany.mZoneBourse.mSoupData.find_all( 'tr' ):
			tr.append( iSoup.new_tag( 'td' ) )
		
		#---
		
		tr = iCompany.mZoneBourse.mSoupData.find( 'tr' ).find_next_sibling()
		iCompany.mZoneBourse.mYears.SetTR2( tr )
		
		tr = tr.find_next_sibling()
		iCompany.mZoneBourse.mRevenue.SetTR2( tr )
		self._ComputeGrowth( iCompany.mZoneBourse.mRevenue, iCompany.mZoneBourse.mGrowthRevenue )
		
		tr = tr.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling()
		iCompany.mZoneBourse.mNetIncome.SetTR2( tr )
		self._ComputeGrowth( iCompany.mZoneBourse.mNetIncome, iCompany.mZoneBourse.mGrowthNetIncome )
		
		tr = tr.find_next_sibling().find_next_sibling()
		iCompany.mZoneBourse.mEarnings.SetTR2( tr )
		self._ComputeGrowth( iCompany.mZoneBourse.mEarnings, iCompany.mZoneBourse.mGrowthEarnings )
		
		tr = tr.find_next_sibling()
		iCompany.mZoneBourse.mDividends.SetTR2( tr )
		self._ComputeGrowth( iCompany.mZoneBourse.mDividends, iCompany.mZoneBourse.mGrowthDividends )
		
		tr = tr.find_next_sibling()
		iCompany.mZoneBourse.mYields.SetTR2( tr )
		
		iCompany.mZoneBourse.mYieldCurrent = float( iCompany.mZoneBourse.mYields.mDataEstimated[0] )
		
		iCompany.mZoneBourse.mUrlDividendCalculator10Years = iCompany.UrlDividendCalculator( float( iCompany.mZoneBourse.mYieldCurrent ), float( iCompany.mZoneBourse.mGrowthDividends.mGrowthAverage ), 10 )
		annual_average = iCompany.AskDividendCalculatorProjection( iCompany.mZoneBourse.mUrlDividendCalculator10Years )
		iCompany.mZoneBourse.mDividendsYield10Years.mGrowthAverage = annual_average
		
		iCompany.mZoneBourse.mUrlDividendCalculator20Years = iCompany.UrlDividendCalculator( float( iCompany.mZoneBourse.mYieldCurrent ), float( iCompany.mZoneBourse.mGrowthDividends.mGrowthAverage ), 20 )
		annual_average = iCompany.AskDividendCalculatorProjection( iCompany.mZoneBourse.mUrlDividendCalculator20Years )
		iCompany.mZoneBourse.mDividendsYield20Years.mGrowthAverage = annual_average
		
	def _ParsePrice( self, iCompany, iSoup ):
		sprice = iSoup.find( id='zbjsfv_dr' )
		scurrency = sprice.find_next_sibling( 'td' )
		
		iCompany.mZoneBourse.mPrice = sprice.string
		iCompany.mZoneBourse.mCurrency = scurrency.string
		
	def _ParseGraphics( self, iCompany, iSoup ):
		root = iSoup.find( id='graphPER' ).find( 'svg' )
		if root:
			iCompany.mZoneBourse.mSoupPER = copy.copy( root )
		
		root = iSoup.find( id='graphBnaDiv' ).find( 'svg' )
		if root:
			iCompany.mZoneBourse.mSoupBNA = copy.copy( root )
		