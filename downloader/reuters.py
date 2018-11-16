#!/usr/bin/env python3

import os
import requests
import time

from colorama import init, Fore, Back, Style

class cReuters:
	def __init__( self ):
		pass
	
	def Download( self, iBrowser, iCompany ):
		print( '	Reuters ...' )

		if not iCompany.mReuters.Symbol():
			print( Fore.CYAN + '	skipping ... (no id)' )
			return
			
		if not iBrowser.Options().ForceDownload() and os.path.exists( iCompany.DataPathFile( iCompany.mReuters.FileName() ) ):
			print( Fore.CYAN + '	skipping ... (existing file)' )
			return

		r = requests.get( iCompany.mReuters.Url() )
		with open( iCompany.DataPathFile( iCompany.mReuters.FileName() ), 'w' ) as output:
			output.write( r.text )
			
		time.sleep( 1 )
	