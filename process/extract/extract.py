#!/usr/bin/python3

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup

from ..company import *

from . import title
from . import info
from . import histo
from . import fondamentals
from . import data
from . import images
from . import dividendsTS
from . import dividendsFC

#---

def Clean( iCompanies ):
	print( 'Clean ...' )
	for company in iCompanies:
		company.Clean()

#---

def Fill( iCompanies ):
	for company in iCompanies:
		print( 'Fill: {} ...'.format( company.mName ) )
		
		company.Fill()

#---

def Extract( iCompanies ):
	soupout = BeautifulSoup( '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Title of the document</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.bundle.min.js"></script>
<style type="text/css">
	h1 
	{ 
		text-align: center;
		font-size: 25px; 
	}
	
	hr
	{
	}
	.price
	{
		color:		rgb( 100, 100, 255 ); 
	}
	
	table.BordCollapseYear{ width: 700px; }
	tr.imp td
	{ 
		background-color: rgb( 200, 200, 255 ); 
	}
	tr.croissance5 td
	{ 
		background-color: rgb( 240, 240, 255 ); 
	}
	.clear
	{
		clear: both;
	}
	.float
	{
		float: left; 
	}
	
	.last10 th,
	.last10 td,
	{
		padding:	7px 10px;
	}
	.last10 th,
	.fondamentals th
	{
		background-color: rgba( 0, 0, 0, 0.10 );
	}
	.fondamentals th:first-child
	{
		width: 220px;
	}
	.fondamentals th
	{
		width: 80px;
	}
	.last10 td,
	.fondamentals td
	{
		text-align:		right;
	}
	.left-space
	{
		border-left-width: 50px;
		border-left-style: solid;
		border-left-color: rgba( 255, 255, 255 );
	}
	.minus
	{
		background-color: rgba( 255, 0, 0, 0.25 );
	}
	.bof
	{
		background-color: rgba( 255, 197, 92, 0.25 );
	}
	.plus
	{
		background-color: rgba( 0, 255, 0, 0.25 );
	}
</style>
</head>
<body>
</body>
</html>''', 'html5lib' )

	body = soupout.find( 'body' )
	
	for company in iCompanies:
		print( 'Extract: {} ...'.format( company.mName ) )
		
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
		
		div = dividendsFC.Extract( company, soupout )
		body.append( div )
		
		div = dividendsTS.Extract( company, soupout )
		body.append( div )
		
	#---
	
	return soupout.prettify()


