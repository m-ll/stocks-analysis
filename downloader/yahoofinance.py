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

import csv
import io
import requests
import shutil
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

		#---

		self._DownloadData( iBrowser, iCompany )
		self._DownloadHistoric( iBrowser, iCompany )
	
	def _DownloadData( self, iBrowser, iCompany ):
		print( '		- Data ' + Style.DIM + '[' + iCompany.mYahooFinance.Url() + ']' )

		output = iCompany.DataPathFile( iCompany.mYahooFinance.FileName() )
			
		if not iBrowser.Options().ForceDownload() and output.exists():
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return

		r = requests.get( iCompany.mYahooFinance.Url(), headers={ 'User-Agent' : iBrowser.Options().UserAgent() } )
		with output.open( 'w' ) as o:
			o.write( r.text )
			
		time.sleep( 1 )

	def _DownloadHistoric( self, iBrowser, iCompany ):
		print( '		- Historic ' + Style.DIM + '[' + iCompany.mYahooFinance.UrlHistoric() + ']' )

		output = iCompany.DataPathFile( iCompany.mYahooFinance.FileNameHistoric() )

		if not iBrowser.Options().ForceDownload() and output.exists():
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return
		
		for i in range( 5 ):
			if i:
				time.sleep( 5 )

			r = requests.get( iCompany.mYahooFinance.UrlHistoric(), headers={ 'User-Agent' : iBrowser.Options().UserAgent() } )
			time.sleep( 1 )

			csv_file = io.StringIO( r.text, newline='' )
			csv_reader = csv.DictReader( csv_file, delimiter=',' )

			row_header = next( csv_reader ) # to remove 'header' row
			lengths = [len( row_header )]
			for _ in range( 0, 20, 2 ): # every 2 rows
				row = next( csv_reader )
				lengths.append( len( row ) )

				if lengths[-1] != lengths[0]:
					print( Fore.YELLOW + 'not a csv file: {}'.format( iCompany.mYahooFinance.UrlHistoric() ) )
					break
			
			 # sure to have a valid header row
			if lengths[0]                     and len( set( lengths ) ) == 1:
				break

		with output.open( 'wb' ) as o:
			o.write( r.content )
