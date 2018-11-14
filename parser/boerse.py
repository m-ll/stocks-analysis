#!/usr/bin/env python3

import re

from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style

class cBoerse:
	def __init__( self ):
		pass
	
	def Parse( self, iCompany ):
		print( '	Boerse ...' )

		if not iCompany.mBoerse.Name():
			print( Fore.CYAN + '	skipping ... (no id)' )
			return
			
		#---
		
		html_content = ''
		with open( iCompany.DataPathFile( iCompany.mBoerse.FileName() ), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		soup = BeautifulSoup( html_content, 'html5lib' )
		
		#---
		
		if soup.find( string=re.compile('Bilanz \(\)') ):
			return
		if soup.find( id='rentabilitaet' ) is None:
			return
		if soup.find( id='kennzahlen' ) is None:
			return
			
		td = soup.find( id='rentabilitaet' ).find_next_sibling( 'table' ).find( 'tr' ).find( 'th' ).find_next_sibling()
		while td:
			iCompany.mBoerse.mYears.append( td.string )
			td = td.find_next_sibling( 'th' )
		
		td = soup.find( id='rentabilitaet' ).find_next_sibling( 'table' ).find( 'td', string='Dividendenrendite' ).find_next_sibling()
		while td:
			iCompany.mBoerse.mDividendYield.append( td.string )
			td = td.find_next_sibling( 'td' )

		td = soup.find( id='kennzahlen' ).find_next_sibling( 'table' ).find_next_sibling( 'table' ).find( 'td' ).find( 'a', string='KGV' ).parent.find_next_sibling()
		while td:
			s = td.string.strip().replace( ',', '.' ) if td.string is not None else '0'
			if 'n.v.' in s:
				s = '0'
			if '-' in s:
				s = '0'
			iCompany.mBoerse.mPER.append( float( s ) )
			td = td.find_next_sibling( 'td' )

		td = soup.find( id='kennzahlen' ).find_next_sibling( 'table' ).find( 'td', string='Dividende je Aktie' ).find_next_sibling()
		while td:
			if td.string is None or td.string.strip() == '-':
				s = '0'
			else:
				s = td.string.strip().replace( ',', '.' )
			iCompany.mBoerse.mDividend.append( float( s ) )
			td = td.find_next_sibling( 'td' )

		iCompany.mBoerse.mDividendGrowth, iCompany.mBoerse.mDividendGrowthAverage, iCompany.mBoerse.mDividendGrowthAverageLast5Y = self._ComputeCroissance( iCompany.mBoerse.mDividend )

		td = soup.find( id='kennzahlen' ).find_next_sibling( 'table' ).find( 'td', string='Gewinn je Aktie (unverwässert)' ).find_next_sibling()
		while td:
			if td.string is None or td.string.strip() == '-':
				s = '0'
			else:
				s = td.string.strip().replace( ',', '.' )
			iCompany.mBoerse.mBNA.append( float( s ) )
			td = td.find_next_sibling( 'td' )

		iCompany.mBoerse.mBNAGrowth, iCompany.mBoerse.mBNAGrowthAverage, iCompany.mBoerse.mBNAGrowthAverageLast5Y = self._ComputeCroissance( iCompany.mBoerse.mBNA )
	
	#---
		
	def _ComputeCroissance( self, iList ):
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
		