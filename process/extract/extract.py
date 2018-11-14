#!/usr/bin/python3

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup

from . import title
from . import info
from . import histo
from . import fondamentals
from . import data
from . import images
from . import ichimoku
from . import dividendsTS
from . import dividendsFC

#---

def WriteImages( iCompanies ):
	for i, company in enumerate( iCompanies, start=1 ):
		print( 'WriteImages ({}/{}): {} ...'.format( i, len( iCompanies ), company.mName ) )
		
		company.WriteImages()

#---

def Fill( iCompanies ):
	for i, company in enumerate( iCompanies, start=1 ):
		print( 'Fill ({}/{}): {} ...'.format( i, len( iCompanies ), company.mName ) )
		
		company.Fill()

#---

def Extract( iCompanies ):

	css = ''
	with open( 'style.css' ) as f:
		css = f.read()
		
	js = ''
	with open( 'js.js' ) as f:
		js = f.read()

	soupout = BeautifulSoup( '''<!DOCTYPE html>
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

	body = soupout.find( 'body' )
	
	for i, company in enumerate( iCompanies, start=1 ):
		print( 'Extract ({}/{}): {} ...'.format( i, len( iCompanies ), company.mName ) )
		
		#---
		
		sep = soupout.new_tag( 'hr' )
		body.append( sep )
		
		div = info.Extract( company, soupout )
		body.append( div )
		
		div = histo.Extract( company, soupout )
		body.append( div )
		
		div = title.Extract( company, soupout )
		body.append( div )
		
		div = fondamentals.Extract( company, soupout )
		body.append( div )
		
		div = data.Extract( company, soupout )
		body.append( div )
		
		div = images.Extract( company, soupout )
		body.append( div )
		
		div = ichimoku.Extract( company, soupout )
		body.append( div )
		
		div = dividendsFC.Extract( company, soupout )
		body.append( div )
		
		div = dividendsTS.Extract( company, soupout )
		body.append( div )
		
		#---
		
		soup_script = soupout.new_tag( 'script' )
		soup_script.string = js
		body.append( soup_script )
		
	#---
	
	return soupout.prettify()


