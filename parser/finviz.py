#!/usr/bin/env python3

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
		
		html_content = ''
		with open( iCompany.DataPathFile( iCompany.mFinviz.FileName() ), 'r', encoding='utf-8' ) as fd:
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