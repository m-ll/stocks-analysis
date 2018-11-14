#!/usr/bin/env python3

import os
import requests
import time

from colorama import init, Fore, Back, Style

class cBoerse:
	def __init__( self ):
		pass
	
	def Download( self, iBrowser, iCompany ):
		print( '	Boerse ...' )

		if not iCompany.mBoerse.Name():
			print( Fore.CYAN + '	skipping ... (no id)' )
			return
			
		if not iBrowser.Options().ForceDownload() and os.path.exists( iCompany.DataFileHTML( iCompany.mBoerse.FileName() ) ):
			print( Fore.CYAN + '	skipping ... (existing file)' )
			return

		r = requests.get( iCompany.mBoerse.Url() )
		with open( iCompany.DataFileHTML( iCompany.mBoerse.FileName() ), 'w' ) as output:
			output.write( r.text )
			
		time.sleep( 1 )
	