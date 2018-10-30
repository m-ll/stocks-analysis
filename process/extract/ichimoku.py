#!/usr/bin/python3

from bs4 import BeautifulSoup

from ..company import *

#---

def Extract( iCompany, iSoup ):
	div_graph = iSoup.new_tag( 'div' )
	div_graph['class'] = 'clear'
	
	img = iSoup.new_tag( 'img' )
	img['src'] = iCompany.DestinationFileIMGIchimoku( 'chart' )
	div_graph.append( img )
	img = iSoup.new_tag( 'img' )
	img['src'] = iCompany.DestinationFileIMGIchimoku( 'prices' )
	div_graph.append( img )
	
	br = iSoup.new_tag( 'br' )
	div_graph.append( br )
	
	img = iSoup.new_tag( 'img' )
	img['src'] = iCompany.DestinationFileIMGIchimoku( 'times' )
	div_graph.append( img )
	
	return div_graph
	
