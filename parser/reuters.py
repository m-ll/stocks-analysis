#!/usr/bin/env python3

from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style

class cReuters:
	def __init__( self ):
		pass
	
	def Parse( self, iCompany ):
		print( '	Reuters ...' )

		if not iCompany.mReuters.Symbol():
			print( Fore.CYAN + '	skipping ... (no id)' )
			return
			
		#---
		
		html_content = ''
		with open( iCompany.DataPathFile( iCompany.mReuters.FileName() ), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		soup = BeautifulSoup( html_content, 'html5lib' )
		
		#---
		
		# iCompany.mReuters.mBNAGrowthType = ''
		
		td = soup.find( string='EPS (TTM) %' ).parent.find_next_sibling()
		td_value = td.string
		iCompany.mReuters.mBNAGrowth['-1'] = td_value
		
		td = td.find_next_sibling()
		td_value = td.string
		iCompany.mReuters.mBNAGrowth['-3'] = td_value
	
		td = td.find_next_sibling()
		td_value = td.string
		iCompany.mReuters.mBNAGrowth['-5'] = td_value
		