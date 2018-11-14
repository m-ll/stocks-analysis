#!/usr/bin/python3

import re
from bs4 import BeautifulSoup

from .dividends import *

#---

def Extract( iCompany, iSoup ):
	div_dividends = iSoup.new_tag( 'div' )
	div_dividends['class'] = 'clear'
	div_dividends['width'] = '400'
	div_dividends['height'] = '50'
	
	if not iCompany.mSDividendsFC:
		return div_dividends
	
	body = iCompany.mSDividendsFC.find( 'table', class_='news_table' ).find( 'tbody' )
	entries = []
	for tr in body.find_all( 'tr' ):
		tds = tr.find_all( 'td' )
		if not tds:
			continue
			
		entry = cDividend()
		
		entry.mType = eType.kDividend
		entry.mYear = tds[0].string.strip()
		price = tds[3].string.strip().replace( ',', '.' )
		entry.mPrice = float( price if price != '-' else '0' )
		
		entries.append( entry )

	labels = []
	data = []
	colors = []
	last_price = 0
	for entry in reversed( entries ):
		if entry.mType == eType.kDividend:
			labels.append( str( entry.mYear ) )
			data.append( str( entry.mPrice ) )
			if entry.mPrice == last_price:
				colors.append( 'rgba( 150, 150, 150, 255 ) ' )
			elif entry.mPrice > last_price:
				colors.append( 'rgba( 150, 255, 150, 255 ) ' )
			else:
				colors.append( 'rgba( 255, 150, 150, 255 ) ' )
			last_price = entry.mPrice
		elif entry.mType == eType.kActionOnly:
			labels.append( 'AO' )
			data.append( '0' )
			colors.append( 'rgba( 255, 255, 255, 255 ) ' )
		elif entry.mType == eType.kSplit:
			labels.append( 'S' )
			data.append( '0' )
			colors.append( 'rgba( 255, 255, 255, 255 ) ' )
			last_price = entry.mPrice
	
	html_chart = CreateCanvasChart( 'chart-FC-' + iCompany.mName, labels, data, colors )
	soup_chart = BeautifulSoup( html_chart, 'html.parser' )
	div_dividends.append( soup_chart.find( 'div' ) )
	
	return div_dividends
