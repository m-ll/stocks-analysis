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
from . import ichimoku
from . import dividendsTS
from . import dividendsFC

#---

def Clean( iCompanies ):
	print( 'Clean ...' )
	for company in iCompanies:
		company.Clean()

#---

def Fill( iCompanies ):
	for i, company in enumerate( iCompanies, start=1 ):
		print( 'Fill ({}/{}): {} ...'.format( i, len( iCompanies ), company.mName ) )
		
		company.Fill()

#---

def Extract( iCompanies ):
	soupout = BeautifulSoup( '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Title of the document</title>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
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
	.fondamentals th,
	.fondamentals td
	{
		padding:	2px 2px;
	}
	.last10 th,
	.fondamentals th
	{
		background-color: rgba( 0, 0, 0, 0.10 );
	}
	.last10 th:first-child,
	.fondamentals th:first-child
	{
		width: 220px;
	}
	.last10 th,
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
	
	/*---*/
	
	.image-holder
	{
		position	: relative;
		display		: inline-block;
		overflow	: hidden; 
	}
	
	.vertical,
	.horizontal
	{ 
		display				: none;
		background-color	: black;
		position			: absolute; 
	}
	.vertical
	{
		width	: 2px;
		height	: 100%;
	}
	.horizontal
	{
		width	: 100%;
		height	: 2px;
	}
</style>
</head>
<body>
</body>
</html>''', 'html5lib' )

	script = '''
	$('.image-holder img').on('mousemove', function(e)
	{
		$h = $( this ).parent().children( '.horizontal' );
		//$v = $( this ).parent().children( '.vertical' );
		
		$h.css( 'top', e.offsetY==undefined ? e.originalEvent.layerY:e.offsetY );
		//$v.css( 'left', e.offsetX==undefined ? e.originalEvent.layerX:e.offsetX );
	});
	
	$('.image-holder').on('mouseenter', function(e)
	{
		$h = $( this ).children( '.horizontal' );
		//$v = $( this ).children( '.vertical' );
		
		if( !$h.length )
		{
			$h = $( document.createElement( 'div' ) );
			$h.addClass( 'horizontal' );
			$h.prependTo( $( this ) );
		}
		/*
		if( !$v.length )
		{
			$v = $( document.createElement( 'div' ) );
			$v.addClass( 'vertical' );
			$v.prependTo( $( this ) );
		}
		*/
		
		$h.show();
		//$v.show();
	}).on('mouseleave', function(e)
	{
		$h = $( this ).children( '.horizontal' );
		//$v = $( this ).children( '.vertical' );
		
		$h.hide();
		//$v.hide();
	});
	'''

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
		soup_script.string = script
		body.append( soup_script )
		
	#---
	
	return soupout.prettify()


