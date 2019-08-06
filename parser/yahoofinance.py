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

		input = iCompany.DataPathFile( iCompany.mYahooFinance.FileName() )
		
		html_content = ''
		with input.open( 'r', encoding='utf-8' ) as fd:
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