#!/usr/bin/env python3

import os
import requests
import time

from colorama import init, Fore, Back, Style

class cTradingSat:
	def __init__( self ):
		pass
	
	def Download( self, iBrowser, iCompany ):
		print( '	TradingSat ...' )

		if not iCompany.mTradingSat.Name():
			print( Fore.CYAN + '	skipping ... (no id)' )
			return
			
		if not iBrowser.Options().ForceDownload() and os.path.exists( iCompany.DataPathFile( iCompany.mTradingSat.FileName() ) ):
			print( Fore.CYAN + '	skipping ... (existing file)' )
			return

		r = requests.get( iCompany.mTradingSat.Url() )
		with open( iCompany.DataPathFile( iCompany.mTradingSat.FileName() ), 'w' ) as output:
			output.write( r.text )
			
		time.sleep( 1 )
	