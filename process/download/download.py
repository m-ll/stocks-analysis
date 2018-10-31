#!/usr/bin/python3

import os
import io
import sys
import time
import shutil
import base64
import tempfile
import requests

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from colorama import init, Fore, Back, Style
# from PIL import Image

from ..company import *

os.environ["PATH"] += os.pathsep + '.'
sgBrowser = None
sgTempDir = ''
sgForceDownload = False;

def GetForceDownload():
	global sgForceDownload
	return sgForceDownload;
	
def SetForceDownload( iForceDownload ):
	global sgForceDownload
	sgForceDownload = iForceDownload;

def BrowserInit():
	global sgBrowser
	global sgTempDir
	
	if sgBrowser is not None:
		return

	if sys.platform.startswith( 'cygwin' ):
		current_path = os.path.abspath( '.' )
		current_path = current_path.replace( '/cygdrive/c', 'C:' )
		current_path = current_path.replace( '/cygdrive/d', 'D:' )
		current_path = current_path.replace( '/cygdrive/e', 'E:' )
		current_path = current_path.replace( '/', '\\' )
		
		sgTempDir = current_path + '\\tmp'
	
	elif sys.platform.startswith( 'linux' ):
		sgTempDir = tempfile.gettempdir() + '/tmp-stocks'
	
	opts = Options()
	# opts.add_argument( '--headless' )
	
	opts.set_preference( 'browser.privatebrowsing.autostart', True )

	opts.set_preference( 'browser.download.folderList', 2 );
	opts.set_preference( 'browser.download.manager.showWhenStarting', False );
	opts.set_preference( 'browser.download.dir', sgTempDir );
	opts.set_preference( 'browser.helperApps.neverAsk.saveToDisk', 'application/csv,text/csv,application/octet-stream,text/html' );

	sgBrowser = webdriver.Firefox( firefox_options=opts )
	sgBrowser.implicitly_wait( 4 ) # seconds
	
	sgBrowser.set_window_size( 1920, 1500 )
	# sgBrowser.set_window_position( 0, 500 )
	
def BrowserQuit():
	global sgBrowser
	
	if sgBrowser is None:
		return
	
	sgBrowser.quit()
	
#---

def DownloadFinancialsZB( iCompanies ):
	global sgBrowser
	
	BrowserInit()

	for i, company in enumerate( iCompanies, start=1 ):
		print( 'Download financials Zonebourse ({}/{}): {} ...'.format( i, len( iCompanies ), company.mName ) )
		if not GetForceDownload() and os.path.exists( company.SourceFileHTMLFinancialsZB() ):
			print( '	skipping ...' )
			continue
		
		sgBrowser.get( company.SourceUrlFinancialsZB() )

		with open( company.SourceFileHTMLFinancialsZB(), 'w' ) as output:
			output.write( sgBrowser.page_source )

		time.sleep( 1 )

def WaitElement( iXPath ):
	global sgBrowser

	element = sgBrowser.find_elements_by_xpath( iXPath )
	while not element:
		print( Fore.YELLOW + 'sleep wait element: {}'.format( iXPath ) )
		time.sleep( 1 )
		element = sgBrowser.find_elements_by_xpath( iXPath )
	
	time.sleep( 1 )

	return element[0]
	
def WaitNoElement( iXPath ):
	global sgBrowser

	element = sgBrowser.find_elements_by_xpath( iXPath )
	while element:
		print( Fore.YELLOW + 'sleep wait no element: {}'.format( iXPath ) )
		time.sleep( 1 )
		element = sgBrowser.find_elements_by_xpath( iXPath )
	
	time.sleep( 1 )
	
def WaitFileInside( iDirectory ):
	global sgBrowser
	
	# Try during 5s max, then refresh the page and test again the file
	# for i in range(5):
		# files = os.listdir( iDirectory )
		# if files:
			# return files[0]
			
		# print( Fore.YELLOW + 'sleep file ({}): {}'.format( i, iDirectory ) )
		# time.sleep( 1 )
			
	# sgBrowser.refresh()	# Doesn't work -_-
	# print( sgBrowser.current_url )
	# sgBrowser.get( sgBrowser.current_url );	# Doesn't work -_-
	# time.sleep( 1 )

	files = os.listdir( iDirectory )
	while not files:
		print( Fore.YELLOW + 'sleep file refresh: {}'.format( iDirectory ) )
		time.sleep( 1 )
		files = os.listdir( iDirectory )

	return files[0]
	
def RemoveFiles( iDirectory ):
	for file in os.listdir( iDirectory ):
		path_file = os.path.join( iDirectory, file )
		if os.path.isfile( path_file ):
			os.unlink( path_file )
			
	time.sleep( 1 )

def DownloadFinancialsMorningstarIncomeStatement( iCompany ):
	global sgBrowser
	global sgTempDir
	
	print( '	- Income Statement' )

	if not GetForceDownload() and os.path.exists( iCompany.SourceFileHTMLFinancialsMorningstarIncomeStatement() ):
		print( '	skipping ...' )
		return
	
	sgBrowser.get( iCompany.SourceUrlFinancialsMorningstarIncomeStatement() )
	time.sleep( 1 )
	
	# with open( iCompany.SourceFileHTMLFinancialsMorningstarIncomeStatement() + '.html', 'w' ) as output:
	#	output.write( sgBrowser.page_source )

	export = WaitElement( '//a[contains(@href,"SRT_stocFund.Export")]' )
	export.click()
	csv = WaitFileInside( sgTempDir )

	shutil.move( sgTempDir + '/' + csv, iCompany.SourceFileHTMLFinancialsMorningstarIncomeStatement() )
	RemoveFiles( sgTempDir )

def DownloadFinancialsMorningstarBalanceSheet( iCompany ):
	global sgBrowser
	global sgTempDir
	
	print( '	- Balance Sheet' )

	if not GetForceDownload() and os.path.exists( iCompany.SourceFileHTMLFinancialsMorningstarBalanceSheet() ):
		print( '	skipping ...' )
		return
	
	sgBrowser.get( iCompany.SourceUrlFinancialsMorningstarBalanceSheet() )
	time.sleep( 1 )
	
	export = WaitElement( '//a[contains(@href,"SRT_stocFund.Export")]' )
	export.click()
	csv = WaitFileInside( sgTempDir )

	shutil.move( sgTempDir + '/' + csv, iCompany.SourceFileHTMLFinancialsMorningstarBalanceSheet() )
	RemoveFiles( sgTempDir )

def DownloadFinancialsMorningstarRatios( iCompany ):
	global sgBrowser
	global sgTempDir

	print( '	- Ratios' )
	
	if not GetForceDownload() and os.path.exists( iCompany.SourceFileHTMLFinancialsMorningstarRatios() ):
		print( '	skipping ...' )
		return
	
	sgBrowser.get( iCompany.SourceUrlFinancialsMorningstarRatios() )
	time.sleep( 1 )
	
	export = WaitElement( '//a[contains(@href,"exportKeyStat2CSV")]' )
	export.click()
	csv = WaitFileInside( sgTempDir )

	shutil.move( sgTempDir + '/' + csv, iCompany.SourceFileHTMLFinancialsMorningstarRatios() )
	RemoveFiles( sgTempDir )
	
def DownloadFinancialsMorningstarValuations( iCompany ):
	global sgBrowser
	
	print( '	- Valuation' )
	
	if not GetForceDownload() and os.path.exists( iCompany.SourceFileHTMLFinancialsMorningstarValuation() ):
		print( '	skipping ...' )
		return
	
	sgBrowser.get( iCompany.SourceUrlFinancialsMorningstarValuation() )
	time.sleep( 1 )
	
	valuation = WaitElement( '//li[@data-link="#sal-components-valuation"]//button' )
	valuation.click()
	WaitNoElement( '//a[@data-anchor="valuation"]/..//sal-components-valuation' )
	WaitNoElement( '//a[@data-anchor="valuation"]/..//sal-components-report-table' )

	with open( iCompany.SourceFileHTMLFinancialsMorningstarValuation(), 'w' ) as output:
		output.write( sgBrowser.page_source )
		
def DownloadFinancialsMorningstarDividends( iCompany ):
	global sgBrowser
	
	print( '	- Dividends' )
	
	if not GetForceDownload() and os.path.exists( iCompany.SourceFileHTMLFinancialsMorningstarDividends() ):
		print( '	skipping ...' )
		return
	
	sgBrowser.get( iCompany.SourceUrlFinancialsMorningstarDividends() )
	time.sleep( 1 )
	
	dividends = WaitElement( '//li[@data-link="#sal-components-dividends"]//button' )
	dividends.click()
	WaitNoElement( '//a[@data-anchor="dividends"]/..//sal-components-dividends' )
	WaitNoElement( '//a[@data-anchor="dividends"]/..//sal-components-report-table' )		# It's maybe needed to make 2 requests for the same page (valuation/dividends) to be sure to have not this element from valuation

	with open( iCompany.SourceFileHTMLFinancialsMorningstarDividends(), 'w' ) as output:
		output.write( sgBrowser.page_source )
		

def DownloadFinancialsMorningstar( iCompanies ):
	global sgBrowser
	global sgTempDir
	
	BrowserInit()

	if os.path.exists( sgTempDir ):
		shutil.rmtree( sgTempDir )
	os.makedirs( sgTempDir )

	for i, company in enumerate( iCompanies, start=1 ):
		print( 'Download financials Morningstar ({}/{}): {} ...'.format( i, len( iCompanies ), company.mName ) )
		
		if not company.mMorningstarRegion:
			continue

		#---

		DownloadFinancialsMorningstarIncomeStatement( company )
		DownloadFinancialsMorningstarBalanceSheet( company )
		DownloadFinancialsMorningstarRatios( company )
		DownloadFinancialsMorningstarValuations( company )
		DownloadFinancialsMorningstarDividends( company )
	
	shutil.rmtree( sgTempDir )

def DownloadFinancialsFV( iCompanies ):
	for i, company in enumerate( iCompanies, start=1 ):
		print( 'Download financials Finviz ({}/{}): {} ...'.format( i, len( iCompanies ), company.mName ) )
		
		if not company.mFVSymbol:
			continue
		if not GetForceDownload() and os.path.exists( company.SourceFileHTMLFinancialsFV() ):
			print( '	skipping ...' )
			continue

		r = requests.get( company.SourceUrlFinancialsFV() )
		with open( company.SourceFileHTMLFinancialsFV(), 'w' ) as output:
			output.write( r.text )
			
		time.sleep( 1 )

def DownloadFinancialsR( iCompanies ):
	for i, company in enumerate( iCompanies, start=1 ):
		print( 'Download financials Reuters ({}/{}): {} ...'.format( i, len( iCompanies ), company.mName ) )
		
		if not company.mRSymbol:
			continue
		if not GetForceDownload() and os.path.exists( company.SourceFileHTMLFinancialsR() ):
			print( '	skipping ...' )
			continue
		
		r = requests.get( company.SourceUrlFinancialsR() )
		with open( company.SourceFileHTMLFinancialsR(), 'w' ) as output:
			output.write( r.text )
			
		time.sleep( 1 )

def DownloadFinancialsYF( iCompanies ):
	for i, company in enumerate( iCompanies, start=1 ):
		print( 'Download financials YahooFinance ({}/{}): {} ...'.format( i, len( iCompanies ), company.mName ) )
		
		if not company.mYFSymbol:
			continue
		if not GetForceDownload() and os.path.exists( company.SourceFileHTMLFinancialsYF() ):
			print( '	skipping ...' )
			continue
		
		r = requests.get( company.SourceUrlFinancialsYF() )
		with open( company.SourceFileHTMLFinancialsYF(), 'w' ) as output:
			output.write( r.text )
			
		time.sleep( 1 )

def DownloadFinancialsB( iCompanies ):
	for i, company in enumerate( iCompanies, start=1 ):
		print( 'Download financials Boerse ({}/{}): {} ...'.format( i, len( iCompanies ), company.mName ) )
		
		if not company.mBName:
			continue
		if not GetForceDownload() and os.path.exists( company.SourceFileHTMLFinancialsB() ):
			print( '	skipping ...' )
			continue
		
		r = requests.get( company.SourceUrlFinancialsB() )
		with open( company.SourceFileHTMLFinancialsB(), 'w' ) as output:
			output.write( r.text )
			
		time.sleep( 1 )

#---

def DownloadSociety( iCompanies ):
	for i, company in enumerate( iCompanies, start=1 ):
		print( 'Download society ({}/{}): {} ...'.format( i, len( iCompanies ), company.mName ) )
		
		if not GetForceDownload() and os.path.exists( company.SourceFileHTMLSocietyZB() ):
			print( '	skipping ...' )
			continue

		r = requests.get( company.SourceUrlSocietyZB() )
		with open( company.SourceFileHTMLSocietyZB(), 'w' ) as output:
			output.write( r.text )
			
		time.sleep( 1 )

#---

def DownloadStockPriceMax( iCompany ):
	if not GetForceDownload() and os.path.exists( iCompany.SourceFileIMG( 9999 ) ):
		print( '	skipping (max) ...' )
		return
		
	r = requests.get( iCompany.SourceUrlStockPriceZB( 9999, 320, 260 ) )
	with open( iCompany.SourceFileIMG( 9999 ), 'wb' ) as output:
		output.write( r.content )
		
	time.sleep( 1 )

def DownloadStockPrice10Years( iCompany ):
	if not GetForceDownload() and os.path.exists( iCompany.SourceFileIMG( 10 ) ):
		print( '	skipping (10y) ...' )
		return

	r = requests.get( iCompany.SourceUrlStockPriceZB( 120, 570, 430 ) )
	with open( iCompany.SourceFileIMG( 10 ), 'wb' ) as output:
		output.write( r.content )

	time.sleep( 1 )

def DownloadStockPrice5Years( iCompany ):
	if not GetForceDownload() and os.path.exists( iCompany.SourceFileIMG( 5 ) ):
		print( '	skipping (5y) ...' )
		return

	r = requests.get( iCompany.SourceUrlStockPriceZB( 60, 570, 430 ) )
	with open( iCompany.SourceFileIMG( 5 ), 'wb' ) as output:
		output.write( r.content )

	time.sleep( 1 )

def DownloadStockPrice2Years( iCompany ):
	if not GetForceDownload() and os.path.exists( iCompany.SourceFileIMG( 2 ) ):
		print( '	skipping (2y) ...' )
		return

	r = requests.get( iCompany.SourceUrlStockPriceZB( 24, 570, 430 ) )
	with open( iCompany.SourceFileIMG( 2 ), 'wb' ) as output:
		output.write( r.content )

	time.sleep( 1 )

def DownloadStockPriceIchimoku( iCompany ):
	global sgBrowser
	
	if( not GetForceDownload() and 
		os.path.exists( iCompany.SourceFileIMGIchimoku( 'chart' ) ) and 
		os.path.exists( iCompany.SourceFileIMGIchimoku( 'prices' ) ) and 
		os.path.exists( iCompany.SourceFileIMGIchimoku( 'times' ) ) ):
		print( '	skipping (ichimoku) ...' )
		return

	sgBrowser.get( iCompany.SourceUrlChartZB( eZBChartAppletMode.kDynamic ) )
	
	# Resize the iframe container
	sgBrowser.execute_script( 'document.getElementById("tv_chart_container").style.width = "2000px"' )
	
	# Remove cookie popup
	element = sgBrowser.find_elements_by_xpath( '//a[@id="cookieChoiceDismiss"]' )
	if element:
		element[0].click()
	
	# Remove account creation
	element = sgBrowser.find_elements_by_xpath( '//div[@id="PopupCertif" and not(contains(@style, "display:none"))]//img[@alt="fermer"]' )
	if element:
		element[0].click()
	element = sgBrowser.find_elements_by_xpath( '//div[@id="dPubInter" and not(contains(@style, "display: none"))]//img[@alt="fermer"]' )
	if element:
		element[0].click()

	# Find the iframe and switch to it
	iframe = WaitElement( '//iframe[contains(@id, "tradingview_") and contains(@name, "tradingview_")]' )
	sgBrowser.switch_to.frame( iframe )
	
	#---
	
	# Disable the technic analysis
	remove_technic_analysis = WaitElement( '//div[contains(@class, "header-chart-panel")]//div[@id="_btAT"]/..' )
	remove_technic_analysis.click()
	
	#---
	
	# Open the indicator list
	open_indicators = WaitElement( '//div[contains(@class, "header-chart-panel")]//a[contains(@class, "indicators")]' )
	open_indicators.click()
	
	# Scroll the indicator list to have the 'ichimoku' indicator displayed
	rows = WaitElement( '//div[contains(@class, "insert-study-dialog")]//div[contains(@class, "insert-study-pages") and contains(@class, "insert-study-row")]' )
	# t = sgBrowser.execute_script( 'var t = arguments[0].scrollTop; arguments[0].scrollTop = 400; return t;', rows )
	# print( t )
	rows.send_keys(Keys.PAGE_DOWN);
	
	# Activate the ichimoku indicator
	indicators = WaitElement( '//div[contains(@class, "insert-study-dialog")]//span[contains(@title, "Ichimoku")]/..' )
	# actions = ActionChains( sgBrowser )
	# actions.move_to_element( indicators ).perform()
	indicators.click()
	
	# Close the indicator list
	close_indicators = WaitElement( '//div[contains(@class, "insert-study-dialog")]//a[contains(@class, "tv-dialog-title-close")]' )
	close_indicators.click()
	
	#---
	
	# Move to right to display the right part of the 'future' cloud
	move_right = WaitElement( '//div[contains(@class, "control-bar-wrapper")]//*[name()="svg" and contains(@class, "move-right-button-control-bar")]' )
	for _ in range( 21 ):
		move_right.click()
	
	# Zoom out to compute more left cloud
	zoom_out = WaitElement( '//div[contains(@class, "control-bar-wrapper")]//*[name()="svg" and contains(@class, "zoom-out-right-button-control-bar")]' )
	for _ in range( 5 ):
		zoom_out.click()
	
	# Zoom in to not display the not computed left part of the cloud
	zoom_in = WaitElement( '//div[contains(@class, "control-bar-wrapper")]//*[name()="svg" and contains(@class, "zoom-in-button-control-bar")]' )
	for _ in range( 2 ):
		zoom_in.click()
		
	time.sleep( 1 )
	
	#---
	
	# Disable the default volume indicator
	close_volume = WaitElement( '//td[contains(@class, "chart-markup-table") and contains(@class, "pane")]//table[contains(@class, "pane-legend")]//span[contains(text(), "Volume")]/..//a[contains(@class, "delete")]' )
	close_volume.click()
	# Disable the default MA(*) indicator
	close_mma = WaitElement( '//td[contains(@class, "chart-markup-table") and contains(@class, "pane")]//table[contains(@class, "pane-legend")]//span[contains(text(), "MA (20)")]/..//a[contains(@class, "delete")]' )
	close_mma.click()
	# Disable the default MA(*) indicator
	close_mma = WaitElement( '//td[contains(@class, "chart-markup-table") and contains(@class, "pane")]//table[contains(@class, "pane-legend")]//span[contains(text(), "MA (50)")]/..//a[contains(@class, "delete")]' )
	close_mma.click()
	# Disable the default MA(*) indicator
	close_mma = WaitElement( '//td[contains(@class, "chart-markup-table") and contains(@class, "pane")]//table[contains(@class, "pane-legend")]//span[contains(text(), "MA (100)")]/..//a[contains(@class, "delete")]' )
	close_mma.click()
	
	#---
	
	# Get the data of the image chart
	canvas = WaitElement( '(//td[contains(@class, "chart-markup-table") and contains(@class, "pane")]//canvas)[1]' )
	canvas_base64 = sgBrowser.execute_script( 'return arguments[0].toDataURL("image/png").substring( 21 );', canvas )
	canvas_data = base64.b64decode( canvas_base64 )
	
	# Get the data of the image time axis
	prices = WaitElement( '((//td[contains(@class, "chart-markup-table") and contains(@class, "price-axis")])[2]//canvas)[1]' )
	prices_base64 = sgBrowser.execute_script( 'return arguments[0].toDataURL("image/png").substring( 21 );', prices )
	prices_data = base64.b64decode( prices_base64 )
	
	# Get the data of the image price axis
	times = WaitElement( '((//td[contains(@class, "chart-markup-table") and contains(@class, "time-axis")])//canvas)[1]' )
	times_base64 = sgBrowser.execute_script( 'return arguments[0].toDataURL("image/png").substring( 21 );', times )
	times_data = base64.b64decode( times_base64 )
	
	with open( iCompany.SourceFileIMGIchimoku( 'chart' ), 'wb' ) as output:
		output.write( canvas_data )

	with open( iCompany.SourceFileIMGIchimoku( 'prices' ), 'wb' ) as output:
		output.write( prices_data )

	with open( iCompany.SourceFileIMGIchimoku( 'times' ), 'wb' ) as output:
		output.write( times_data )

	#---
		
# pip3 install pillow
# [DON'T WORK ON CYGWIN -_-]
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
	
	sgBrowser.switch_to.default_content()

	time.sleep( 1 )

def DownloadStockPrice( iCompanies ):
	for i, company in enumerate( iCompanies, start=1 ):
		print( 'Download images ({}/{}): {} ...'.format( i, len( iCompanies ), company.mName ) )
		
		DownloadStockPriceMax( company )
		DownloadStockPrice10Years( company )
		DownloadStockPrice5Years( company )
		DownloadStockPrice2Years( company )
		
		DownloadStockPriceIchimoku( company )

#---

def DownloadDividends( iCompanies ):
	global sgBrowser
	
	BrowserInit()

	for i, company in enumerate( iCompanies, start=1 ):
		print( 'Download dividends TS ({}/{}): {} ...'.format( i, len( iCompanies ), company.mName ) )
		
		if not company.mTSName:
			continue
		if not GetForceDownload() and os.path.exists( company.SourceFileHTMLDividendsTS() ):
			print( '	skipping ...' )
			continue

		r = requests.get( company.SourceUrlDividendsTS() )
		with open( company.SourceFileHTMLDividendsTS(), 'w' ) as output:
			output.write( r.text )

		time.sleep( 1 )

	for i, company in enumerate( iCompanies, start=1 ):
		print( 'Download dividends FC ({}/{}): {} ...'.format( i, len( iCompanies ), company.mName ) )
		
		if not company.mFCName:
			continue
		if not GetForceDownload() and os.path.exists( company.SourceFileHTMLDividendsFC() ):
			print( '	skipping ...' )
			continue

		r = requests.get( company.SourceUrlDividendsFC() )
		with open( company.SourceFileHTMLDividendsFC(), 'w' ) as output:
			output.write( r.text )
			
		time.sleep( 1 )




