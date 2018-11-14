#!/usr/bin/env python3

import os
import requests
import time

from colorama import init, Fore, Back, Style

class cYahooFinance:
	def __init__( self ):
		pass
	
	def Download( self, iBrowser, iCompany ):
		print( '	YahooFinance ...' )

		if not iCompany.mYahooFinance.Symbol():
			print( Fore.CYAN + '	skipping ... (no id)' )
			return
			
		if not iBrowser.Options().ForceDownload() and os.path.exists( iCompany.DataFileHTML( iCompany.mYahooFinance.FileName() ) ):
			print( Fore.CYAN + '	skipping ... (existing file)' )
			return

		r = requests.get( iCompany.mYahooFinance.Url() )
		with open( iCompany.DataFileHTML( iCompany.mYahooFinance.FileName() ), 'w' ) as output:
			output.write( r.text )
			
		time.sleep( 1 )
	