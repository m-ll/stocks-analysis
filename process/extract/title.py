#!/usr/bin/python3

import os
from bs4 import BeautifulSoup

from ..company import *

#---

def Extract( iCompany, iSoup ):
	link_graph = iSoup.new_tag( 'a' )
	link_graph['href'] = iCompany.SourceUrlChartZB()
	link_graph.append( ' [Graphique]' )
	
	link_fond = iSoup.new_tag( 'a' )
	link_fond['href'] = iCompany.SourceUrlFinancialsZB()
	link_fond.append( ' [Fondamentaux]' )
	
	link_societe = iSoup.new_tag( 'a' )
	link_societe['href'] = iCompany.SourceUrlSocietyZB()
	link_societe.append( ' [Societe]' )
	
	link_dividends_fc = None
	if iCompany.mFCName:
		link_dividends_fc = iSoup.new_tag( 'a' )
		link_dividends_fc['href'] = iCompany.SourceUrlDividendsFC()
		link_dividends_fc.append( ' [DividendsFC]' )
		
	link_dividends_ts = None
	if iCompany.mTSName:
		link_dividends_ts = iSoup.new_tag( 'a' )
		link_dividends_ts['href'] = iCompany.SourceUrlDividendsTS()
		link_dividends_ts.append( ' [DividendsTS]' )
	
	sprice = iCompany.mSFinancialsZB.find( id='zbjsfv_dr' )
	price = iSoup.new_tag( 'span' )
	price['class'] = 'price'
	price.append( sprice.string )
	
	currency = sprice.find_next_sibling( 'td' ).string
	
	# ---
	
	h_title = iSoup.new_tag( 'h1' )
	h_title['class'] = 'clear title'
	h_title.append( '[' )
	h_title.append( price )
	h_title.append( ' {} ] '.format( currency ) )
	h_title.append( '{}: {}'.format( iCompany.mZBName, iCompany.mISIN ) )
	h_title.append( link_graph )
	h_title.append( link_fond )
	h_title.append( link_societe )
	if link_dividends_fc is not None:
		h_title.append( link_dividends_fc )
	if link_dividends_ts is not None:
		h_title.append( link_dividends_ts )
	
	return h_title

