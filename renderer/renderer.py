#!/usr/bin/env python3

import copy
import os

from bs4 import BeautifulSoup

from . import info
from . import graphics
from . import data
from . import data_boerse
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
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.bundle.min.js"></script>
<style type="text/css">
''' + css + '''
</style>
</head>
<body>
</body>
</html>''', 'html5lib' )

		body = soup.find( 'body' )
		
		for i, company in enumerate( self.mCompanies, start=1 ):
			print( 'Render ({}/{}): {} ...'.format( i, len( self.mCompanies ), company.mName ) )
			
			#---
			
			sep = soup.new_tag( 'hr' )
			body.append( sep )
			
			subtag_society = info.Society( company, soup )
			subtag_title = info.Title( company, soup )
			subtag_next_dividend_date = info.NextDividendDate( company, soup )
			
			subtag_dividends_finances = info.Dividends( company, soup, 'finances' )
			subtag_dividends_tradingsat = info.Dividends( company, soup, 'tradingsat' )
			
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
			
			root = soup.new_tag( 'header' )
			root.append( subtag_society )
			# root.append( subtag_data_boerse )
			root.append( subtag_title )
			root.append( subtag_next_dividend_date )
			body.append( root )
			
			root = soup.new_tag( 'article' )
			# data
			root.append( subtag_data )
			# (zb/)per/bna/max/
			tag = soup.new_tag( 'div' )
			tag['class'] = ['graphics']
			tag.append( subtag_data_growth )
			tag.append( subtag_per )
			tag.append( subtag_bna )
			tag.append( subtag_prices_simple[0] )
			root.append( tag )
			# title again
			root.append( copy.copy( subtag_title ) )
			# years 10/5/2
			tag = soup.new_tag( 'div' )
			tag['class'] = ['graphics', 'simple']
			tag.append( subtag_prices_simple[1] )
			tag.append( subtag_prices_simple[2] )
			tag.append( subtag_prices_simple[3] )
			root.append( tag )
			root.append( subtag_prices_ichimoku )
			body.append( root )
			
			root = soup.new_tag( 'footer' )
			root.append( subtag_dividends_finances )
			root.append( subtag_dividends_tradingsat )
			body.append( root )
			
		#---
		
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
		
		outputpathfile = os.path.join( iOutputPath, '{}-[{}].html'.format( groups, len( self.mCompanies ) ) )
		with open( outputpathfile, 'w' ) as output:
			output.write( self.mHTML )
			
		for i, company in enumerate( self.mCompanies, start=1 ):
			print( 'WriteImages ({}/{}): {} ...'.format( i, len( self.mCompanies ), company.Name() ) )
			company.WriteImages( iOutputPath )
			