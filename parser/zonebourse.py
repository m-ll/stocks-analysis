#!/usr/bin/env python3

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
		iCompany.mZoneBourse.mSoupSociety = root
		
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

	def _ParseData( self, iCompany, iSoup ):
		iCompany.mZoneBourse.mSoupData = iSoup.find( 'table', class_='BordCollapseYear' )
		if not iCompany.mZoneBourse.mSoupData:
			return
			
		for tr in iCompany.mZoneBourse.mSoupData.find_all( 'tr' ):
			tr.append( iSoup.new_tag( 'td' ) )
		
		tr_years = iCompany.mZoneBourse.mSoupData.find( 'tr' ).find_next_sibling()
		tr_ca = tr_years.find_next_sibling()
		tr_ebitda = tr_ca.find_next_sibling()
		tr_ebitda.find_next_sibling().decompose()
		tr_ebitda.find_next_sibling().decompose()
		tr_net = tr_ebitda.find_next_sibling()
		
		tr_bna = tr_net.find_next_sibling().find_next_sibling()
		tr_dividends = tr_bna.find_next_sibling()
		tr_rendements = tr_dividends.find_next_sibling()
		
		#---
		
		iCompany.mZoneBourse.mDividendsGrowth, iCompany.mZoneBourse.mDividendsGrowthAverage = self._ComputeCroissanceTr( tr_dividends )
		
		iCompany.mZoneBourse.mBNAGrowth, iCompany.mZoneBourse.mBNAGrowthAverage = self._ComputeCroissanceTr( tr_bna )
		
		td_rendement = tr_rendements.find( 'td' ).find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find( 'b' ).string
		iCompany.mZoneBourse.mYieldCurrent = float( td_rendement.strip().replace( '%', '' ).replace( ',', '.' ) )
		
	def _ParsePrice( self, iCompany, iSoup ):
		sprice = iSoup.find( id='zbjsfv_dr' )
		scurrency = sprice.find_next_sibling( 'td' )
		
		iCompany.mZoneBourse.mPrice = sprice.string
		iCompany.mZoneBourse.mCurrency = scurrency.string
		
	def _ParseGraphics( self, iCompany, iSoup ):
		iCompany.mZoneBourse.mSoupPER = iSoup.find( id='graphPER' ).find( 'svg' )
		iCompany.mZoneBourse.mSoupBNA = iSoup.find( id='graphBnaDiv' ).find( 'svg' )
		