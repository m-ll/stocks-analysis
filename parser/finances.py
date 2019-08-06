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

import company.company

class cFinances:
	def __init__( self ):
		pass
	
	def Parse( self, iCompany ):
		return

		print( '	Finances ...' )

		if not iCompany.mFinances.Name():
			print( Fore.CYAN + '	skipping ... (no id)' )
			return
		
		#---

		input = iCompany.DataPathFile( iCompany.mFinances.FileName() )
		
		html_content = ''
		with input.open( 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		soup = BeautifulSoup( html_content, 'html5lib' )
		
		#---
		
		body = soup.find( 'table', class_='news_table' ).find( 'tbody' )
		for tr in body.find_all( 'tr' ):
			tds = tr.find_all( 'td' )
			if not tds:
				continue
				
			entry = company.company.cFinances.cDividend()
			
			entry.mType = company.company.cFinances.cDividend.eType.kDividend
			entry.mYear = tds[0].string.strip()
			price = tds[3].string.strip().replace( ',', '.' )
			entry.mPrice = float( price if price != '-' else '0' )
			
			iCompany.mFinances.mDividends.append( entry )
