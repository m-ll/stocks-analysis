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
from io import BytesIO
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup

import company.company

#---

def _CreateSVGStar( iSoup ):
	svg = iSoup.new_tag( 'svg' )
	svg['aria-hidden'] = 'true'
	svg['focusable'] = 'false'
	svg['data-prefix'] = 'fas'
	svg['data-icon'] = 'star'
	svg['class'] = 'svg-inline--fa fa-star fa-w-18'
	svg['role'] = 'img'
	svg['xmlns'] = 'http://www.w3.org/2000/svg'
	svg['viewBox'] = '0 0 576 512'
	svg['width'] = '22'
	svg['height'] = '22'

	path = iSoup.new_tag( 'path' )
	path['fill'] = 'currentColor'
	path['d'] = 'M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z'

	svg.append( path )

	return svg

def Summary( iCompany, iSoup ):
	beta = iSoup.new_tag( 'span' )
	beta['class'] = [ 'beta' ]
	beta.append( 'β={}'.format( iCompany.mMorningstar.mQuoteBeta ) )
	
	#---

	price_value = iSoup.new_tag( 'span' )
	price_value['class'] = 'value'
	price_value.append( copy.copy( iCompany.mZoneBourse.mPrice ) )
	
	price = iSoup.new_tag( 'span' )
	price['class'] = [ 'price', 'origin' ]
	price.append( '[' )
	price.append( price_value )
	price.append( ' {} ] '.format( iCompany.mZoneBourse.mCurrency ) )
	
	#---
	
	price_realtime_value = iSoup.new_tag( 'span' )
	price_realtime_value['class'] = ['value']
	price_old = float( iCompany.mZoneBourse.mPrice )
	price_new = float( iCompany.mZoneBourse.mPriceRealTime )
	if price_new > price_old:
		price_realtime_value['class'].append( 'up' )
	elif price_new < price_old:
		price_realtime_value['class'].append( 'down' )
	price_realtime_value.append( copy.copy( iCompany.mZoneBourse.mPriceRealTime ) )
	
	price_realtime_link = iSoup.new_tag( 'a', href=iCompany.mZoneBourse.UrlGraphic( company.company.cZoneBourse.eAppletMode.kDynamic ), target='_blank' )
	price_realtime_link.append( '[' )
	price_realtime_link.append( price_realtime_value )
	price_realtime_link.append( ' {} ] '.format( iCompany.mZoneBourse.mCurrency ) )
	
	price_realtime = iSoup.new_tag( 'span' )
	price_realtime['class'] = [ 'price', 'realtime' ]
	price_realtime['title'] = datetime.now().strftime( '%d/%m/%Y - %H:%M:%S' )
	price_realtime.append( price_realtime_link )
	
	#---
	
	notation = iSoup.new_tag( 'span' )
	notation['class'] = [ 'notation', f'star{iCompany.Notation().StarsCount()}' ]
	if iCompany.Notation().Note() > 9.5:
		notation['class'].append( 'jackpot' )
	notation['title'] = '{:.02f} / 10'.format( iCompany.Notation().Note() )
	
	for _ in range( iCompany.Notation().StarsCount() ):
		notation.append( _CreateSVGStar( iSoup ) )
	
	#---
	
	name = iSoup.new_tag( 'span' )
	name['class'] = 'name'
	
	link_name = iSoup.new_tag( 'a', href='#' )
	link_name.append( '{}'.format( iCompany.Name() ) )

	name.append( link_name )
	
	#---
	
	invest_total = _InfoInvestedTotal( iCompany, iSoup )

	#---
	
	dividend_yield = iSoup.new_tag( 'span' )
	dividend_yield['class'] = 'yield'
	
	dividend_yield_current = iSoup.new_tag( 'span' )
	dividend_yield_current['class'] = ['current']
	yield_current = float( iCompany.mMorningstar.mFinancialsDividendsYield.mTTM )
	if yield_current >= 4.3:
		dividend_yield_current['class'].append( 'plus' )
	elif yield_current >= 3.6:
		dividend_yield_current['class'].append( 'bof' )
	else:
		dividend_yield_current['class'].append( 'minus' )
	dividend_yield_current.append( '{}%'.format( iCompany.mMorningstar.mFinancialsDividendsYield.mTTM ) )
	
	dividend_yield_growth = iSoup.new_tag( 'span' )
	dividend_yield_growth['class'] = 'growth'
	dividend_yield_growth.append( ' ( growth: {}% )'.format( iCompany.mMorningstar.mFinancialsGrowthDividends.mGrowthAverage ) )
	
	dividend_yield_10_years = iSoup.new_tag( 'span' )
	dividend_yield_10_years['class'] = 'years-10'
	dividend_yield_10_years.append( ' ( 10-years: {}% )'.format( iCompany.mMorningstar.mFinancialsDividendsYield10Years.mTTM ) )

	dividend_yield.append( dividend_yield_current )
	dividend_yield.append( dividend_yield_growth )
	dividend_yield.append( dividend_yield_10_years )
	
	#---
	
	# Always return a root because it can be customized outside
	root = iSoup.new_tag( 'span' )
	root['class'] = 'summary'
	root.append( beta )
	root.append( price )
	root.append( price_realtime )
	root.append( invest_total )
	root.append( notation )
	root.append( name )
	root.append( dividend_yield )
		
	return root

def Title( iCompany, iSoup ):
	price_value = iSoup.new_tag( 'span' )
	price_value['class'] = 'value'
	price_value.append( copy.copy( iCompany.mZoneBourse.mPrice ) )
	
	price = iSoup.new_tag( 'span' )
	price['class'] = [ 'price', 'origin' ]
	price.append( '[' )
	price.append( price_value )
	price.append( ' {} ] '.format( iCompany.mZoneBourse.mCurrency ) )
	
	#---
	
	price_realtime_value = iSoup.new_tag( 'span' )
	price_realtime_value['class'] = ['value']
	price_old = float( iCompany.mZoneBourse.mPrice )
	price_new = float( iCompany.mZoneBourse.mPriceRealTime )
	if price_new > price_old:
		price_realtime_value['class'].append( 'up' )
	elif price_new < price_old:
		price_realtime_value['class'].append( 'down' )
	price_realtime_value.append( copy.copy( iCompany.mZoneBourse.mPriceRealTime ) )
	
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
	
	link_graph = iSoup.new_tag( 'a', href=iCompany.mZoneBourse.UrlGraphic( company.company.cZoneBourse.eAppletMode.kStatic ), target='_blank' )
	link_graph.append( ' [Prices]' )
	
	# link_graph2 = iSoup.new_tag( 'a', href=iCompany.mZoneBourse.UrlGraphic( company.company.cZoneBourse.eAppletMode.kDynamic ), target='_blank' )
	# link_graph2.append( ' [Prices Dynamic]' )
	
	link_fond = iSoup.new_tag( 'a', href=iCompany.mZoneBourse.UrlData(), target='_blank' )
	link_fond.append( ' [Fondamentaux]' )
	
	link_societe = iSoup.new_tag( 'a', href=iCompany.mZoneBourse.UrlSociety(), target='_blank' )
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
	# root.append( link_graph2 )
	root.append( link_fond )
	root.append( link_societe )
	root.append( iSoup.new_tag( 'br' ) )
	root.append( invest_svg )
	root.append( ' => ' )
	root.append( invest_total )
		
	return root

def _InfoInvestedTotal( iCompany, iSoup ):
	invest = iSoup.new_tag( 'span' )
	invest['class'] = ['invested']
	
	if not iCompany.HasInvested():
		return invest
	
	total = iCompany.GetInvested().ComputeTotalPrice()
	if total >= 3000:
		invest['class'].append( 'high' )
	elif total >= 1000:
		invest['class'].append( 'mid' )
	else:
		invest['class'].append( 'low' )
	
	invest.append( '{:.2f} {}'.format( total, iCompany.mZoneBourse.mCurrency ) )

	return invest

class cBox:
	def __init__( self, iX, iY, iWidth, iHeight ):
		self.mX = iX
		self.mY = iY
		self.mWidth = iWidth
		self.mHeight = iHeight

def _InfoInvestedSVG( iCompany, iSoup ):
	if not iCompany.HasInvested():
		return iSoup.new_tag( 'span' )
	if not iCompany.GetInvested().GetData():
		return iSoup.new_tag( 'span' )
	
	plt.gcf().set_size_inches( 10, 2 )

	plt.margins(0.05, 0.2)

	# first line
	x1 = [ d['date'] for d in iCompany.GetInvested().GetData() ]
	y1 = [ d['unit-price'] for d in iCompany.GetInvested().GetData() ]
	t1 = [ d['unit-price'] for d in iCompany.GetInvested().GetData() ]
	# t1 = [ f"{d['unit-price']}\n(x{d['count']})" for d in iCompany.GetInvested().GetData() ] #TODO: add more info on tooltip
	max_count = max( [ d['count'] for d in iCompany.GetInvested().GetData() ] )
	scale_count = 100 if max_count < 20 else 20 if max_count < 100 else 2
	s1 = [ d['count'] * scale_count for d in iCompany.GetInvested().GetData() ]
	c1 = None # [ d['count'] * 100 for d in iCompany.GetInvested().GetData() ]
	# plotting the line 1 points
	plt.scatter( x1, y1, s=s1, c=c1, alpha=0.5, label=iCompany.Name())
	# plt.plot( x1, y1, '.', label=iCompany.Name())
	for x, y, t in zip( x1, y1, t1 ):
		plt.text( x, y, t, horizontalalignment='center', verticalalignment='center' )

	# second line
	x2 = [ date( 2018, 4, 1 ), datetime.now().date() ]
	y2 = [ float(iCompany.mZoneBourse.mPriceRealTime), float(iCompany.mZoneBourse.mPriceRealTime) ]
	if iCompany.mZoneBourse.mCurrency.lower() == 'gbp' or iCompany.mZoneBourse.mCurrency.lower() == 'gbx':
		y2 = list( map( lambda v: v / 100.0, y2 ) )
	# plotting the line 2 points
	plt.plot( x2, y2, '--', c='red', label='current price' )
	plt.text( x2[-1], y2[-1] + 0.5, str(y2[-1]), horizontalalignment='center' )

	# show a legend on the plot
	plt.legend()

	# function to show the plot
	f = BytesIO()
	plt.savefig( f, format="svg" )
	plt.close()

	#---

	soup_xml = BeautifulSoup( f.getvalue().decode( 'utf-8' ), 'xml' )

	return soup_xml.find( 'svg' )

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
	
	link2 = iSoup.new_tag( 'a', href=company_data.Url(), target='_blank' )
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
