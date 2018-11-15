#!/usr/bin/env python3

import copy
from datetime import date, datetime

from bs4 import BeautifulSoup

import company.company

#---

def Title( iCompany, iSoup ):
	link_graph = iSoup.new_tag( 'a', href=iCompany.mZoneBourse.UrlGraphic( company.company.cZoneBourse.eAppletMode.kStatic ) )
	link_graph.append( ' [Prices]' )
	
	link_graph2 = iSoup.new_tag( 'a', href=iCompany.mZoneBourse.UrlGraphic( company.company.cZoneBourse.eAppletMode.kDynamic ) )
	link_graph2.append( ' [Prices Dynamic]' )
	
	link_fond = iSoup.new_tag( 'a', href=iCompany.mZoneBourse.UrlData() )
	link_fond.append( ' [Fondamentaux]' )
	
	link_societe = iSoup.new_tag( 'a', href=iCompany.mZoneBourse.UrlSociety() )
	link_societe.append( ' [Societe]' )
	
	price_value = iSoup.new_tag( 'span' )
	price_value['class'] = 'value'
	price_value.append( iCompany.mZoneBourse.mPrice )
	
	price = iSoup.new_tag( 'span' )
	price['class'] = 'price'
	price.append( '[' )
	price.append( price_value )
	price.append( ' {} ] '.format( iCompany.mZoneBourse.mCurrency ) )
	
	name = iSoup.new_tag( 'span' )
	name['class'] = 'name'
	name.append( '{}: {}'.format( iCompany.Name(), iCompany.ISIN() ) )
	
	#---
	
	# Always return a root because it can be customized (like for Dividends() size)
	root = iSoup.new_tag( 'span' )
	root['class'] = 'title'
	root.append( price )
	root.append( name )
	root.append( link_graph )
	root.append( link_graph2 )
	root.append( link_fond )
	root.append( link_societe )
		
	return root

def NextDividendDate( iCompany, iSoup ):
	root = iSoup.new_tag( 'span' )
	root['class'] = 'next-dividend-date'
	
	for next_date in iCompany.mMorningstar.mDividendNextDates:
		entry = iSoup.new_tag( 'span' )
		entry['class'] = 'entry'
		
		date_next = iSoup.new_tag( 'span' )
		diff = next_date - date.today()
		date_next['class'] = 'far' if diff.days > 7 else 'close'
		date_next.append( next_date.strftime( '%d/%m/%Y' ) )
		
		entry.append( 'Next Dividend Date: ' )
		entry.append( date_next )
		
		root.append( entry )
	
	return root

def Society( iCompany, iSoup ):
	root = iSoup.new_tag( 'div' )
	root['class'] = 'society'
	
	root.append( copy.copy( iCompany.mZoneBourse.mSoupSociety ) )
	
	return root

#---

def _CreateCanvasChart( iName, iLabels, iData, iColors ):
	return '<div class="chart">\
<canvas id="' + iName + '" width="400" height="50"></canvas>\
<script>\
var ctx = document.getElementById("' + iName + '");\
var myChart = new Chart(ctx, {\
	type: \'bar\',\
	data: {\
		labels: ["' + '", "'.join( iLabels ) + '"],\
		datasets: [{\
			label: \'# of Dividends\',\
			data: [' + ', '.join( iData ) + '],\
			backgroundColor: [\
			"' + '", "'.join( iColors ) + '"\
			],\
			borderColor: [\
			],\
			borderWidth: 3\
		}]\
	},\
	options: {\
		scales: {\
			yAxes: [{\
				ticks: {\
					beginAtZero:true\
				}\
			}]\
		}\
	}\
});\
</script>\
</div>'
	
def Dividends( iCompany, iSoup, iTag ):
	root = iSoup.new_tag( 'div' )
	root['class'] = 'dividend-chart'
	
	if iTag == 'finances':
		company_data = iCompany.mFinances
		etype = company.company.cFinances.cDividend.eType
	elif iTag == 'tradingsat':
		company_data = iCompany.mTradingSat
		etype = company.company.cTradingSat.cDividend.eType
		
	if not company_data.Name():
		return root
		
	#---
	
	title = iSoup.new_tag( 'div' )
	title['class'] = 'title'
	
	link = iSoup.new_tag( 'a', href='#' )
	link['class'] = 'toggle'
	link.append( 'Dividends' )
	
	link2 = iSoup.new_tag( 'a', href=company_data.Url() )
	link2.append( iTag )
	
	title.append( link )
	title.append( ' : ' )
	title.append( link2 )
	
	root.append( title )
	
	#---
	
	labels = []
	data = []
	colors = []
	last_price = 0
	for entry in reversed( company_data.mDividends ):
		if entry.mType == etype.kDividend:
			labels.append( str( entry.mYear ) )
			data.append( str( entry.mPrice ) )
			if entry.mPrice == last_price:
				colors.append( 'rgba( 150, 150, 150, 255 ) ' )
			elif entry.mPrice > last_price:
				colors.append( 'rgba( 150, 255, 150, 255 ) ' )
			else:
				colors.append( 'rgba( 255, 150, 150, 255 ) ' )
			last_price = entry.mPrice
		elif entry.mType == etype.kActionOnly:
			labels.append( 'AO' )
			data.append( '0' )
			colors.append( 'rgba( 255, 255, 255, 255 ) ' )
		elif entry.mType == etype.kSplit:
			labels.append( 'S' )
			data.append( '0' )
			colors.append( 'rgba( 255, 255, 255, 255 ) ' )
			last_price = entry.mPrice
	
	html_chart = _CreateCanvasChart( 'chart-{}-{}'.format( iTag, iCompany.mName ), labels, data, colors )
	soup_chart = BeautifulSoup( html_chart, 'html.parser' )
	root.append( soup_chart.find( 'div' ) )
	
	return root
