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
from datetime import date, datetime

from bs4 import BeautifulSoup

import company.company

#---

def Title( iCompany, iSoup ):
	price_value = iSoup.new_tag( 'span' )
	price_value['class'] = 'value'
	price_value.append( iCompany.mZoneBourse.mPrice )
	
	price = iSoup.new_tag( 'span' )
	price['class'] = [ 'price', 'origin' ]
	price.append( '[' )
	price.append( price_value )
	price.append( ' {} ] '.format( iCompany.mZoneBourse.mCurrency ) )
	
	#---
	
	price_realtime_value = iSoup.new_tag( 'span' )
	price_realtime_value['class'] = 'value'
	price_realtime_value.append( copy.copy( iCompany.mZoneBourse.mPrice ) )
	
	price_realtime = iSoup.new_tag( 'span' )
	price_realtime['class'] = [ 'price', 'realtime' ]
	price_realtime.append( '[' )
	price_realtime.append( price_realtime_value )
	price_realtime.append( ' {} ] '.format( iCompany.mZoneBourse.mCurrency ) )
	
	#---
	
	name = iSoup.new_tag( 'span' )
	name['class'] = 'name'
	name.append( '{}: {}'.format( iCompany.Name(), iCompany.ISIN() ) )
	
	#---
	
	link_graph = iSoup.new_tag( 'a', href=iCompany.mZoneBourse.UrlGraphic( company.company.cZoneBourse.eAppletMode.kStatic ) )
	link_graph.append( ' [Prices]' )
	
	link_graph2 = iSoup.new_tag( 'a', href=iCompany.mZoneBourse.UrlGraphic( company.company.cZoneBourse.eAppletMode.kDynamic ) )
	link_graph2.append( ' [Prices Dynamic]' )
	
	link_fond = iSoup.new_tag( 'a', href=iCompany.mZoneBourse.UrlData() )
	link_fond.append( ' [Fondamentaux]' )
	
	link_societe = iSoup.new_tag( 'a', href=iCompany.mZoneBourse.UrlSociety() )
	link_societe.append( ' [Societe]' )
	
	#---
	
	invest_svg = _InfoInvestedSVG( iCompany, iSoup )
	invest_total = _InfoInvestedTotal( iCompany, iSoup )
	
	#---
	
	# Always return a root because it can be customized (like for Dividends() size)
	root = iSoup.new_tag( 'span' )
	root['class'] = 'title'
	root.append( price )
	root.append( price_realtime )
	root.append( name )
	root.append( link_graph )
	root.append( link_graph2 )
	root.append( link_fond )
	root.append( link_societe )
	root.append( iSoup.new_tag( 'br' ) )
	root.append( invest_svg )
	root.append( invest_total )
		
	return root

def _InfoInvestedTotal( iCompany, iSoup ):
	invest = iSoup.new_tag( 'span' )
	invest['class'] = 'invested'
	
	if iCompany.Invested() is None:
		return invest

	cto_total = sum( d['count'] * d['unit-price'] for d in iCompany.Invested()['cto'] )
	pea_total = sum( d['count'] * d['unit-price'] for d in iCompany.Invested()['pea'] )
	
	invest.append( ' => {:.2f}'.format( cto_total + pea_total ) )

	return invest

class cBox:
	def __init__( self, iX, iY, iWidth, iHeight ):
		self.mX = iX
		self.mY = iY
		self.mWidth = iWidth
		self.mHeight = iHeight

def _InfoInvestedSVG( iCompany, iSoup ):
	if iCompany.Invested() is None:
		return iSoup.new_tag( 'span' )

	padding_x = 25
	padding_y = 15
	box_full = cBox( 0, 0, 500+2*padding_x, 100+2*padding_y )
	inner_box = cBox( padding_x, padding_y, 500, 100 )

	invest = iSoup.new_tag( 'svg', width=box_full.mWidth, height=box_full.mHeight, style='background: rgb(230,230,230)' )
	invest['class'] = 'invested'

	unit_price_all = [ d['unit-price'] for d in iCompany.Invested()['cto'] ] + [ d['unit-price'] for d in iCompany.Invested()['pea'] ]

	price_current = float(iCompany.mZoneBourse.mPrice)
	if iCompany.mZoneBourse.mCurrency.lower() == 'gbp':
		price_current /= 100.0
	price_min = min( unit_price_all + [price_current] )
	price_max = max( unit_price_all + [price_current] )

	for i, unit_price in enumerate( unit_price_all ):
		cx = _ComputeX( inner_box.mWidth, len(unit_price_all) + 1, i )
		cy = _ComputeY( inner_box.mHeight, price_min, price_max, unit_price )

		circle = _NewCircle( iSoup, inner_box, cx, cy, 2 )
		invest.append( circle )

		text = _NewText( iSoup, inner_box, cx, cy, str(unit_price) )
		invest.append( text )
		
	cx = _ComputeX( inner_box.mWidth, len(unit_price_all) + 1, len(unit_price_all) )
	cy = _ComputeY( inner_box.mHeight, price_min, price_max, price_current )

	circle = _NewCircle( iSoup, inner_box, cx, cy, 2, 'red' )
	invest.append( circle )

	text = _NewText( iSoup, inner_box, cx, cy, str(price_current), 'red' )
	invest.append( text )

	line = _NewHorizontal( iSoup, inner_box, cy, 'red' )
	invest.append( line )

	return invest

def _ComputeX( iWidth, iCount, iIndex ):
	return iIndex / ( iCount - 1 ) * iWidth

def _ComputeY( iHeight, iPriceMin, iPriceMax, iPrice ):
	return iHeight - ( iPrice - iPriceMin ) / ( iPriceMax - iPriceMin ) * iHeight

def _NewCircle( iSoup, iInnerBox, iCenterX, iCenterY, iRadius, iColor='black' ):
	return iSoup.new_tag( 'circle', cx=iInnerBox.mX + iCenterX, cy=iInnerBox.mY + iCenterY, r=iRadius, fill=iColor )

def _NewText( iSoup, iInnerBox, iX, iY, iText, iColor='black' ):
	text = iSoup.new_tag( 'text', x=iInnerBox.mX + iX, y=iInnerBox.mY + iY - 3, fill=iColor )
	text['font-size'] = 12
	text['text-anchor'] = 'middle'
	text.append( iText )
	return text

def _NewHorizontal( iSoup, iInnerBox, iY, iColor='black' ):
	line = iSoup.new_tag( 'path' )
	line['stroke'] = 'red'
	line['stroke-width'] = 2
	line['stroke-dasharray'] = '10,10'
	line['d'] = f'M {iInnerBox.mX} {iInnerBox.mY + iY} L {iInnerBox.mX+iInnerBox.mWidth} {iInnerBox.mY + iY}'
	return line

#---

def Society( iCompany, iSoup ):
	root = iSoup.new_tag( 'div' )
	root['class'] = 'society'

	sector = iSoup.new_tag( 'div' )
	sector.string = '{}-{}'.format( iCompany.mMorningstar.mQuoteSector, iCompany.mMorningstar.mQuoteIndustry )
	root.append( sector )	
	
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
