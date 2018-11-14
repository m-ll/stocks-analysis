#!/usr/bin/env python3

from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style

import company.company

class cFinances:
	def __init__( self ):
		pass
	
	def Parse( self, iCompany ):
		print( '	Finances ...' )

		if not iCompany.mFinances.Name():
			print( Fore.CYAN + '	skipping ... (no id)' )
			return
			
		#---
		
		html_content = ''
		with open( iCompany.DataPathFile( iCompany.mFinances.FileName() ), 'r', encoding='utf-8' ) as fd:
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
