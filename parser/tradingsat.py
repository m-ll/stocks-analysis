#!/usr/bin/env python3

import re

from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style

import company.company

class cTradingSat:
	def __init__( self ):
		pass
	
	def Parse( self, iCompany ):
		print( '	TradingSat ...' )

		if not iCompany.mTradingSat.Name():
			print( Fore.CYAN + '	skipping ... (no id)' )
			return
			
		#---
		
		html_content = ''
		with open( iCompany.DataPathFile( iCompany.mTradingSat.FileName() ), 'r', encoding='utf-8' ) as fd:
			html_content = fd.read()
			
		soup = BeautifulSoup( html_content, 'html5lib' )
		
		#---
		
		body = soup.find( string=re.compile( 'Historique des dividendes' ) ).find_parent().find_parent().find_next_sibling().find( 'tbody' )
		for tr in body.find_all( 'tr' ):
			entry = company.company.cTradingSat.cDividend()
			if tr.get( 'class' ) and 'sous-entete' in tr.get( 'class' ):
				entry.mType = company.company.cTradingSat.cDividend.eType.kSplit
				iCompany.mTradingSat.mDividends.append( entry )
				continue
			
			tds = tr.find_all( 'td' )
			
			if tr.find( string=re.compile( 'En actions uniquement' ) ):
				entry.mType = company.company.cTradingSat.cDividend.eType.kActionOnly
				entry.mYear = int( tds[0].find( 'strong' ).string.strip() )
			else:
				entry.mType = company.company.cTradingSat.cDividend.eType.kDividend
				entry.mYear = int( tds[0].find( 'strong' ).string.strip() )
				entry.mPrice = float( tds[4].string.strip()[:-1] )
			
			iCompany.mTradingSat.mDividends.append( entry )
