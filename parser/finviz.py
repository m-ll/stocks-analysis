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

class cFinviz:
	def __init__( self ):
		pass
	
	def Parse( self, iCompany ):
		print( '	Finviz ...' )

		if not iCompany.mFinviz.Symbol():
			print( Fore.CYAN + '	skipping ... (no id)' )
			return
			
		#---

		input = iCompany.DataPathFile( iCompany.mFinviz.FileName() )
		
		html_content = ''
		with input.open( 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		soup = BeautifulSoup( html_content, 'html5lib' )
		
		#---
		
		# iCompany.mFinviz.mBNAGrowthType = '%'
		
		table = soup.find( 'table', class_='snapshot-table2' )
		tr = table.find( 'tr' ).find_next_sibling().find_next_sibling().find_next_sibling()
		td = tr.find( string='EPS this Y' ).parent
		td_value = td.find_next_sibling().string
		iCompany.mFinviz.mBNAGrowth['0'] = td_value
		
		tr = tr.find_next_sibling()
		td = tr.find( string='EPS next Y' ).parent
		td_value = td.find_next_sibling().string
		iCompany.mFinviz.mBNAGrowth['+1'] = td_value
	
		tr = tr.find_next_sibling()
		td = tr.find( string='EPS next 5Y' ).parent
		td_value = td.find_next_sibling().string
		iCompany.mFinviz.mBNAGrowth['+5'] = td_value
	
		tr = tr.find_next_sibling()
		td = tr.find( string='EPS past 5Y' ).parent
		td_value = td.find_next_sibling().string
		iCompany.mFinviz.mBNAGrowth['-5'] = td_value