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

import base64
import requests
import time

# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from colorama import init, Fore, Back, Style

class cZoneBourse:
	def __init__( self ):
		pass
	
	def Download( self, iBrowser, iCompany ):
		print( '	ZoneBourse ...' )

		if not iCompany.mZoneBourse.Name():
			print( Fore.CYAN + '	skipping ... (no id)' )
			return
			
		self._DownloadData( iBrowser, iCompany )
		self._DownloadSociety( iBrowser, iCompany )
		self._DownloadPricesSimple( iBrowser, iCompany )
		self._DownloadPricesIchimoku( iBrowser, iCompany )
			
	#---
	
	def _DownloadData( self, iBrowser, iCompany ):
		print( '		- Data ' + Style.DIM + '[' + iCompany.mZoneBourse.UrlData() + ']' )

		output = iCompany.DataPathFile( iCompany.mZoneBourse.FileNameData() )

		if not iBrowser.Options().ForceDownload() and output.exists():
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return

		iBrowser.Driver().get( iCompany.mZoneBourse.UrlData() )
		time.sleep( 2 )

		with output.open( 'w' ) as o:
			o.write( iBrowser.Driver().page_source )
			
		time.sleep( 1 )
		
	def _DownloadSociety( self, iBrowser, iCompany ):
		print( '		- Society ' + Style.DIM + '[' + iCompany.mZoneBourse.UrlSociety() + ']' )

		output = iCompany.DataPathFile( iCompany.mZoneBourse.FileNameSociety() )

		if not iBrowser.Options().ForceDownload() and output.exists():
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return

		r = requests.get( iCompany.mZoneBourse.UrlSociety(), headers={ 'User-Agent' : iBrowser.Options().UserAgent() } )
		with output.open( 'w' ) as o:
			o.write( r.text )
			
		time.sleep( 1 )
		
	#---
		
	def _DownloadPricesSimple( self, iBrowser, iCompany ):
		print( '		- Prices Simple' )
		
		self._DownloadPricesSimpleMax( iBrowser, iCompany )
		self._DownloadPricesSimple10Y( iBrowser, iCompany )
		self._DownloadPricesSimple5Y( iBrowser, iCompany )
		self._DownloadPricesSimple2Y( iBrowser, iCompany )
		
	def _DownloadPricesSimpleMax( self, iBrowser, iCompany ):
		output = iCompany.DataPathFile( iCompany.mZoneBourse.FileNamePricesSimple( 9999 ) )

		if not iBrowser.Options().ForceDownload() and output.exists():
			print( Fore.CYAN + '		skipping (max) ... (existing file)' )
			return
			
		r = requests.get( iCompany.mZoneBourse.UrlPricesSimple( 9999, 320, 260 ), headers={ 'User-Agent' : iBrowser.Options().UserAgent() } )
		with output.open( 'wb' ) as o:
			o.write( r.content )
			
		time.sleep( 1 )
		
	def _DownloadPricesSimple10Y( self, iBrowser, iCompany ):
		output = iCompany.DataPathFile( iCompany.mZoneBourse.FileNamePricesSimple( 10 ) )

		if not iBrowser.Options().ForceDownload() and output.exists():
			print( Fore.CYAN + '		skipping (10y) ... (existing file)' )
			return
			
		r = requests.get( iCompany.mZoneBourse.UrlPricesSimple( 120, 570, 430 ), headers={ 'User-Agent' : iBrowser.Options().UserAgent() } )
		with output.open( 'wb' ) as o:
			o.write( r.content )
			
		time.sleep( 1 )

	def _DownloadPricesSimple5Y( self, iBrowser, iCompany ):
		output = iCompany.DataPathFile( iCompany.mZoneBourse.FileNamePricesSimple( 5 ) )

		if not iBrowser.Options().ForceDownload() and output.exists():
			print( Fore.CYAN + '		skipping (5y) ... (existing file)' )
			return
			
		r = requests.get( iCompany.mZoneBourse.UrlPricesSimple( 60, 570, 430 ), headers={ 'User-Agent' : iBrowser.Options().UserAgent() } )
		with output.open( 'wb' ) as o:
			o.write( r.content )
			
		time.sleep( 1 )

	def _DownloadPricesSimple2Y( self, iBrowser, iCompany ):
		output = iCompany.DataPathFile( iCompany.mZoneBourse.FileNamePricesSimple( 2 ) )

		if not iBrowser.Options().ForceDownload() and output.exists():
			print( Fore.CYAN + '		skipping (2y) ... (existing file)' )
			return
			
		r = requests.get( iCompany.mZoneBourse.UrlPricesSimple( 24, 570, 430 ), headers={ 'User-Agent' : iBrowser.Options().UserAgent() } )
		with output.open( 'wb' ) as o:
			o.write( r.content )
			
		time.sleep( 1 )

	#---
		
	def _DownloadPricesIchimoku( self, iBrowser, iCompany ):
		print( '		- Prices Ichimoku ' + Style.DIM + '[' + iCompany.mZoneBourse.UrlPricesIchimoku() + ']' )
		
		filenames = iCompany.mZoneBourse.FileNamesPricesIchimoku()
		if( not iBrowser.Options().ForceDownload() and 
			iCompany.DataPathFile( filenames[0] ).exists() and 
			iCompany.DataPathFile( filenames[1] ).exists() and 
			iCompany.DataPathFile( filenames[2] ).exists() ):
			print( Fore.CYAN + '		skipping (ichimoku) ...' )
			return
			
		driver = iBrowser.Driver()

		driver.get( iCompany.mZoneBourse.UrlPricesIchimoku() )
		
		#---
		
		time.sleep( 5 )
		
		# Remove rgpd popup
		element = driver.find_elements_by_xpath( '//div[@id="qcCmpButtons"]/button[contains(@class, "qc-cmp-button") and not(contains(@class, "qc-cmp-secondary-button"))]' )
		if element:
			element[0].click()
		
		# Remove account creation
		element = driver.find_elements_by_xpath( '//div[@id="PopupCertif" and not(contains(@style, "display:none"))]//img[@alt="fermer"]' )
		if element:
			element[0].click()

		element = driver.find_elements_by_xpath( '//div[@id="dPubInter" and not(contains(@style, "display: none"))]//img[@alt="fermer"]' )
		if element:
			element[0].click()

		# Remove cookie popup
		element = driver.find_elements_by_xpath( '//a[@id="cookieChoiceDismiss"]' )
		if element:
			element[0].click()

		js = "var h=document.getElementById('dPubBg');h.parentNode.removeChild(h)"
		driver.execute_script( js )
		js = "var h=document.getElementById('dPubInter');h.parentNode.removeChild(h)"
		driver.execute_script( js )
		js = "var h=document.getElementById('back_g_d');h.parentNode.removeChild(h)"
		driver.execute_script( js )
			
		# Find the offer iframe and switch to it
		iframe = driver.find_elements_by_xpath( '//iframe[@id="offerIframe"]' )
		if iframe:
			driver.switch_to.frame( iframe[0] )
			element = driver.find_elements_by_xpath( '//img[@alt="fermer"]' )
			if element:
				element[0].click()

			driver.switch_to.default_content()
		
		#---

		js = "var h=document.getElementById('myHeader');h.parentNode.removeChild(h)"
		driver.execute_script( js )
		
		driver.execute_script( 'document.getElementById("mydiv").style.width = "1800px"' )
		driver.execute_script( 'document.getElementById("mydiv").firstElementChild.style.width = "1800px"' )
		driver.execute_script( 'document.getElementById("mydiv").firstElementChild.lastElementChild.style.width = "1800px"' )
		time.sleep( 1 )
		
		# Find the first iframe and switch to it
		iframe = iBrowser.WaitElement( '//iframe[contains(@src, "inc_dyna_graph")]' )
		driver.switch_to.frame( iframe )
		
		# Resize the iframe container
		driver.execute_script( 'document.getElementById("tv_chart_container").style.width = "1800px"' )
		time.sleep( 1 )
		
		# Find the iframe and switch to it
		iframe = iBrowser.WaitElement( '//iframe[contains(@id, "tradingview_") and contains(@name, "tradingview_")]' )
		driver.switch_to.frame( iframe )
		
		#---
		
		# Disable the technic analysis
		remove_technic_analysis = iBrowser.WaitElement( '//div[contains(@class, "header-chart-panel")]//div[@id="_btAT"]/..' )
		remove_technic_analysis.click()
		
		#---
		
		# Open the indicator list
		open_indicators = iBrowser.WaitElement( '//div[contains(@class, "header-chart-panel")]//a[contains(@class, "indicators")]' )
		open_indicators.click()
		
		# Scroll the indicator list to have the 'ichimoku' indicator displayed
		rows = iBrowser.WaitElement( '//div[contains(@class, "insert-study-dialog")]//div[contains(@class, "insert-study-pages") and contains(@class, "insert-study-row")]' )
		# t = driver.execute_script( 'var t = arguments[0].scrollTop; arguments[0].scrollTop = 400; return t;', rows )
		# print( t )
		# rows.send_keys(Keys.PAGE_DOWN)
		
		# Activate the ichimoku indicator
		# first scroll to an entry above ichimoku, because when calling 'scroll', the entry selected will at the top of the page and below the header (so not clickable)
		# indicators = iBrowser.WaitElement( '//div[contains(@class, "insert-study-dialog")]//span[contains(@title, "Ichimoku")]/..' )
		indicators = iBrowser.WaitElement( '//div[contains(@class, "insert-study-dialog")]//span[contains(@title, "Directional Movement Index")]/..' )
		indicators.location_once_scrolled_into_view
		indicators = iBrowser.WaitElement( '//div[contains(@class, "insert-study-dialog")]//span[contains(@title, "Ichimoku")]/..' )
		indicators.click()
		
		# Close the indicator list
		close_indicators = iBrowser.WaitElement( '//div[contains(@class, "insert-study-dialog")]//a[contains(@class, "tv-dialog-title-close")]' )
		close_indicators.location_once_scrolled_into_view
		close_indicators.click()
		
		#---

		# Move to right to display the right part of the 'future' cloud
		move_right = iBrowser.WaitElement( '//div[contains(@class, "control-bar-wrapper")]//*[name()="svg" and contains(@class, "move-right-button-control-bar")]' )
		for _ in range( 21 ):
			move_right.click()
		
		time.sleep( 1 )
		
		# Zoom out to compute more left cloud
		zoom_out = iBrowser.WaitElement( '//div[contains(@class, "control-bar-wrapper")]//*[name()="svg" and contains(@class, "zoom-out-right-button-control-bar")]' )
		for _ in range( 5 ):
			zoom_out.click()
			time.sleep( 0.5 )
		
		time.sleep( 1 )
		
		# Zoom in to not display the not computed left part of the cloud
		zoom_in = iBrowser.WaitElement( '//div[contains(@class, "control-bar-wrapper")]//*[name()="svg" and contains(@class, "zoom-in-button-control-bar")]' )
		for _ in range( 2 ):
			zoom_in.click()
			time.sleep( 1 )
			
		time.sleep( 1 )
		
		#---
		
		# Disable the default volume indicator
		close_volume = iBrowser.WaitElement( '//td[contains(@class, "chart-markup-table") and contains(@class, "pane")]//table[contains(@class, "pane-legend")]//span[contains(text(), "Volume")]/..//a[contains(@class, "delete")]' )
		close_volume.click()
		time.sleep( 0.5 )
		# Disable the default MA(*) indicator
		close_mma = iBrowser.WaitElement( '//td[contains(@class, "chart-markup-table") and contains(@class, "pane")]//table[contains(@class, "pane-legend")]//span[contains(text(), "MA (20)")]/..//a[contains(@class, "delete")]' )
		close_mma.click()
		time.sleep( 0.5 )
		# Disable the default MA(*) indicator
		close_mma = iBrowser.WaitElement( '//td[contains(@class, "chart-markup-table") and contains(@class, "pane")]//table[contains(@class, "pane-legend")]//span[contains(text(), "MA (50)")]/..//a[contains(@class, "delete")]' )
		close_mma.click()
		time.sleep( 0.5 )
		# Disable the default MA(*) indicator
		close_mma = iBrowser.WaitElement( '//td[contains(@class, "chart-markup-table") and contains(@class, "pane")]//table[contains(@class, "pane-legend")]//span[contains(text(), "MA (100)")]/..//a[contains(@class, "delete")]' )
		close_mma.click()
		time.sleep( 0.5 )
		
		#---
		
		# Get the data of the image chart
		canvas = iBrowser.WaitElement( '(//td[contains(@class, "chart-markup-table") and contains(@class, "pane")]//canvas)[1]' )
		canvas_base64 = driver.execute_script( 'return arguments[0].toDataURL("image/png").substring( 21 );', canvas )
		canvas_data = base64.b64decode( canvas_base64 )
		
		# Get the data of the image time axis
		prices = iBrowser.WaitElement( '((//td[contains(@class, "chart-markup-table") and contains(@class, "price-axis")])[2]//canvas)[1]' )
		prices_base64 = driver.execute_script( 'return arguments[0].toDataURL("image/png").substring( 21 );', prices )
		prices_data = base64.b64decode( prices_base64 )
		
		# Get the data of the image price axis
		times = iBrowser.WaitElement( '((//td[contains(@class, "chart-markup-table") and contains(@class, "time-axis")])//canvas)[1]' )
		times_base64 = driver.execute_script( 'return arguments[0].toDataURL("image/png").substring( 21 );', times )
		times_data = base64.b64decode( times_base64 )
		
		with open( iCompany.DataPathFile( filenames[0] ), 'wb' ) as output:
			output.write( canvas_data )

		with open( iCompany.DataPathFile( filenames[1] ), 'wb' ) as output:
			output.write( prices_data )

		with open( iCompany.DataPathFile( filenames[2] ), 'wb' ) as output:
			output.write( times_data )

		#---
			
# pip3 install pillow
# [DON'T WORK ON CYGWIN -_- as the wheel is not precompiled for it]
# download the corresponding wheel file: https://pypi.org/project/Pillow/#files
# see which name to choose: import pip._internal; print(pip._internal.pep425tags.get_supported())
# rename it to: Pillow-5.3.0-cp36-cp36m-cygwin_2_8_1_x86_64.whl
# pip3 install Pillow-5.3.0-cp36-cp36m-cygwin_2_8_1_x86_64.whl

		# canvas_png = Image.open( io.BytesIO( canvas_data ) )
		# prices_png = Image.open( io.BytesIO( prices_data ) )
		# times_png = Image.open( io.BytesIO( times_data ) )
		
		# total_width = canvas_png.width + prices_png.width
		# total_height = canvas_png.height + times_png.height
		
		# full_image = Image.new( 'RGB', ( total_width, total_height ) )
		# full_image.paste( canvas_png, ( 0, 0 ) )
		# full_image.paste( prices_png, ( canvas_png.width, 0 ) )
		# full_image.paste( times_png, ( 0, canvas_png.height ) )
		
		# with open( iCompany.SourceFileIMGIchimoku(), 'wb' ) as output:
			# output.write( full_image.tobytes() )

		#---
		
		driver.switch_to.default_content()

		time.sleep( 1 )