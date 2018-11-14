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
	
	if not iCompany.mSDividendsTS:
		return div_dividends
	
	body = iCompany.mSDividendsTS.find( string=re.compile( 'Historique des dividendes' ) ).find_parent().find_parent().find_next_sibling().find( 'tbody' )
	entries = []
	for tr in body.find_all( 'tr' ):
		entry = cDividend()
		if tr.get( 'class' ) and 'sous-entete' in tr.get( 'class' ):
			entry.mType = eType.kSplit
			entries.append( entry )
			continue
		
		tds = tr.find_all( 'td' )
		
		if tr.find( string=re.compile( 'En actions uniquement' ) ):
			entry.mType = eType.kActionOnly
			entry.mYear = int( tds[0].find( 'strong' ).string.strip() )
		else:
			entry.mType = eType.kDividend
			entry.mYear = int( tds[0].find( 'strong' ).string.strip() )
			entry.mPrice = float( tds[4].string.strip()[:-1] )
		
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
	
	html_chart = CreateCanvasChart( 'chart-TS-' + iCompany.mName, labels, data, colors )
	soup_chart = BeautifulSoup( html_chart, 'html.parser' )
	div_dividends.append( soup_chart.find( 'div' ) )
	
	return div_dividends

