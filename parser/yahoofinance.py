#!/usr/bin/env python3

from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style

class cYahooFinance:
	def __init__( self ):
		pass
	
	def Parse( self, iCompany ):
		print( '	YahooFinance ...' )

		if not iCompany.mYahooFinance.Symbol():
			print( Fore.CYAN + '	skipping ... (no id)' )
			return
			
		#---
		
		html_content = ''
		with open( iCompany.DataPathFile( iCompany.mYahooFinance.FileName() ), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		soup = BeautifulSoup( html_content, 'html5lib' )
		
		#---
		
		# iCompany.mYahooFinance.mGrowthType = ''
		
		if not soup.find( string='Past 5 Years (per annum)' ):
			return
			
		td = soup.find( string='Past 5 Years (per annum)' ).find_parent( 'td' ).find_next_sibling()
		td_value = td.string
		iCompany.mYahooFinance.mGrowth['-5'] = td_value
		
		td = td.find_parent( 'tr' ).find_previous_sibling().find( 'td' ).find_next_sibling()
		td_value = td.string
		iCompany.mYahooFinance.mGrowth['+5'] = td_value
	
		td = td.find_parent( 'tr' ).find_previous_sibling().find( 'td' ).find_next_sibling()
		td_value = td.string
		iCompany.mYahooFinance.mGrowth['+1'] = td_value
	
		td = td.find_parent( 'tr' ).find_previous_sibling().find( 'td' ).find_next_sibling()
		td_value = td.string
		iCompany.mYahooFinance.mGrowth['0'] = td_value