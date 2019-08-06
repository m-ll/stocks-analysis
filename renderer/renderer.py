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

import copy

from bs4 import BeautifulSoup

from . import data
from . import data_boerse
from . import graphics
from . import info
from . import menu
import company.company

class cRenderer:
	def __init__( self, iCompanies ):
		self.mHTML = ''
		self.mCompanies = iCompanies
	
	def Render( self ):
		# print( '	Render ...' )

		css = ''
		with open( 'style.css' ) as f:
			css = f.read()
			
		js = ''
		with open( 'js.js' ) as f:
			js = f.read()
			
		#---

		soup = BeautifulSoup( '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Title of the document</title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
<style type="text/css">
''' + css + '''
</style>
</head>
<body>
</body>
</html>''', 'html5lib' )

		body = soup.find( 'body' )
		
		subtag_menu = menu.Sectors( self.mCompanies, soup )
		
		root = soup.new_tag( 'nav' )
		root.append( subtag_menu )
		body.append( root )
		
		main = soup.new_tag( 'main' )
		
		for i, company in enumerate( self.mCompanies, start=1 ):
			print( 'Render ({}/{}): {} ...'.format( i, len( self.mCompanies ), company.mName ) )
			
			#---
			
			sep = soup.new_tag( 'hr' )
			main.append( sep )
			
			subtag_society = info.Society( company, soup )
			subtag_title = info.Title( company, soup )
			
			# subtag_dividends_finances = info.Dividends( company, soup, 'finances' )
			# subtag_dividends_tradingsat = info.Dividends( company, soup, 'tradingsat' )
			
			subtag_prices_simple = [ graphics.PricesSimple( company, soup, 9999 ),
										graphics.PricesSimple( company, soup, 10 ),
										graphics.PricesSimple( company, soup, 5 ),
										graphics.PricesSimple( company, soup, 2 ) ]
			subtag_prices_ichimoku = graphics.PricesIchimoku( company, soup )
			subtag_per = graphics.PER( company, soup )
			subtag_bna = graphics.BNA( company, soup )
			
			subtag_data = data.Data( company, soup )
			subtag_data_growth = data.DataGrowth( company, soup )
			subtag_data_boerse = data_boerse.Data( company, soup )
			
			#---
			
			root = soup.new_tag( 'article', id=company.Name() )
			
			subroot = soup.new_tag( 'header' )
			subroot.append( subtag_society )
			# subroot.append( subtag_data_boerse )
			subroot.append( subtag_title )
			root.append( subroot )
			
			subroot = soup.new_tag( 'article' )
			# data
			subroot.append( subtag_data )
			# (zb/)per/bna/max/
			tag = soup.new_tag( 'div' )
			tag['class'] = ['graphics']
			tag.append( subtag_data_growth )
			tag.append( subtag_per )
			tag.append( subtag_bna )
			tag.append( subtag_prices_simple[0] )
			subroot.append( tag )
			# title again
			subroot.append( copy.copy( subtag_title ) )
			# years 10/5/2
			tag = soup.new_tag( 'div' )
			tag['class'] = ['graphics', 'simple']
			tag.append( subtag_prices_simple[1] )
			tag.append( subtag_prices_simple[2] )
			tag.append( subtag_prices_simple[3] )
			subroot.append( tag )
			subroot.append( subtag_prices_ichimoku )
			root.append( subroot )
			
			subroot = soup.new_tag( 'footer' )
			# subroot.append( subtag_dividends_finances )
			# subroot.append( subtag_dividends_tradingsat )
			root.append( subroot )

			main.append( root )
			
		body.append( main )
			
		#---
		
		soup_script = soup.new_tag( 'script', src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js" )
		body.append( soup_script )
		
		soup_script = soup.new_tag( 'script', src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" )
		body.append( soup_script )
		
		soup_script = soup.new_tag( 'script', src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" )
		body.append( soup_script )
		
		soup_script = soup.new_tag( 'script', src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.bundle.min.js" )
		body.append( soup_script )
		
		soup_script = soup.new_tag( 'script' )
		soup_script.string = js
		body.append( soup_script )
		
		#---
		
		self.mHTML = soup.prettify()

	def Export( self, iOutputPath ):
		print( 'Export html ...' )
		
		groups = [ company.mGroup for company in self.mCompanies ] # Get all groups
		groups = set( groups ) # Get only unique group (should be single most of the time)
		groups = '-'.join( groups ) # Create the name
		
		outputpathfile = iOutputPath / '{}-[{}].html'.format( groups, len( self.mCompanies ) )
		with outputpathfile.open( 'w' ) as output:
			output.write( self.mHTML )
			
		for i, company in enumerate( self.mCompanies, start=1 ):
			print( 'WriteImages ({}/{}): {} ...'.format( i, len( self.mCompanies ), company.Name() ) )
			company.WriteImages( iOutputPath )
			