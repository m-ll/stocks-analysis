#!/usr/bin/env python3

import os
import requests
import time

from colorama import init, Fore, Back, Style

class cFinviz:
	def __init__( self ):
		pass
	
	def Download( self, iBrowser, iCompany ):
		print( '	Finviz ...' )

		if not iCompany.mFinviz.Symbol():
			print( Fore.CYAN + '	skipping ... (no id)' )
			return
			
		if not iBrowser.Options().ForceDownload() and os.path.exists( iCompany.DataFileHTML( iCompany.mFinviz.FileName() ) ):
			print( Fore.CYAN + '	skipping ... (existing file)' )
			return

		r = requests.get( iCompany.mFinviz.Url() )
		with open( iCompany.DataFileHTML( iCompany.mFinviz.FileName() ), 'w' ) as output:
			output.write( r.text )
			
		time.sleep( 1 )
	