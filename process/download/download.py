#!/usr/bin/python3

import os
import sys
import time
import shutil
import tempfile
import requests

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from ..company import *

os.environ["PATH"] += os.pathsep + '.'
sgBrowser = None
sgTempDir = ''

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
	opts.add_argument( '--headless' )
	
	opts.set_preference( 'browser.privatebrowsing.autostart', True )

	opts.set_preference( 'browser.download.folderList', 2 );
	opts.set_preference( 'browser.download.manager.showWhenStarting', False );
	opts.set_preference( 'browser.download.dir', sgTempDir );
	opts.set_preference( 'browser.helperApps.neverAsk.saveToDisk', 'application/csv,text/csv,application/octet-stream,text/html' );

	sgBrowser = webdriver.Firefox( firefox_options=opts )
	sgBrowser.implicitly_wait( 4 ) # seconds
	
	sgBrowser.set_window_size( 1920, 1200 )
	
def BrowserQuit():
	global sgBrowser
	
	if sgBrowser is None:
		return
	
	sgBrowser.quit()
	
#---

def DownloadFinancialsZB( iCompanies ):
	global sgBrowser
	
	BrowserInit()

	for company in iCompanies:
		print( 'Download financials Zonebourse: {} ...'.format( company.mName ) )
		
		sgBrowser.get( company.SourceUrlFinancialsZB() )

		with open( company.SourceFileHTMLFinancialsZB(), 'w' ) as output:
			output.write( sgBrowser.page_source )

		time.sleep( 1 )

def WaitElement( iXPath ):
	global sgBrowser

	element = sgBrowser.find_elements_by_xpath( iXPath )
	while not element:
		print( 'sleep wait element: {}'.format( iXPath ) )
		time.sleep( 1 )
		element = sgBrowser.find_elements_by_xpath( iXPath )
	
	time.sleep( 1 )

	return element[0]
	
def WaitNoElement( iXPath ):
	global sgBrowser

	element = sgBrowser.find_elements_by_xpath( iXPath )
	while element:
		print( 'sleep wait no element: {}'.format( iXPath ) )
		time.sleep( 1 )
		element = sgBrowser.find_elements_by_xpath( iXPath )
	
	time.sleep( 1 )
	
def WaitFileInside( iDirectory ):
	time.sleep( 1 )
	files = os.listdir( iDirectory )
	while not files:
		print( 'sleep file: {}'.format( iDirectory ) )
		time.sleep( 1 )
		files = os.listdir( iDirectory )

	return files[0]
	
def RemoveFiles( iDirectory ):
	for file in os.listdir( iDirectory ):
		path_file = os.path.join( iDirectory, file )
		if os.path.isfile( path_file ):
			os.unlink( path_file )
			
	time.sleep( 1 )

def DownloadFinancialsMorningstar( iCompanies ):
	global sgBrowser
	global sgTempDir
	
	BrowserInit()

	for company in iCompanies:
		print( 'Download financials Morningstar: {} ...'.format( company.mName ) )
		
		if company.mMorningstarRegion:
			if os.path.exists( sgTempDir ):
				shutil.rmtree( sgTempDir )
			os.makedirs( sgTempDir )

			print( '	- Income Statement' )
			sgBrowser.get( company.SourceUrlFinancialsMorningstarIncomeStatement() )
			time.sleep( 1 )
			
			# with open( company.SourceFileHTMLFinancialsMorningstarIncomeStatement() + '.html', 'w' ) as output:
			#	output.write( sgBrowser.page_source )

			export = WaitElement( '//a[contains(@href,"SRT_stocFund.Export")]' )
			export.click()
			csv = WaitFileInside( sgTempDir )

			shutil.move( sgTempDir + '/' + csv, company.SourceFileHTMLFinancialsMorningstarIncomeStatement() )
			RemoveFiles( sgTempDir )

			#---

			print( '	- Balance Sheet' )
			sgBrowser.get( company.SourceUrlFinancialsMorningstarBalanceSheet() )
			time.sleep( 1 )
			
			# with open( company.SourceFileHTMLFinancialsMorningstarBalanceSheet() + '.html', 'w' ) as output:
			#	output.write( sgBrowser.page_source )

			if os.path.exists( sgTempDir ):
				shutil.rmtree( sgTempDir )
			os.makedirs( sgTempDir )

			export = WaitElement( '//a[contains(@href,"SRT_stocFund.Export")]' )
			export.click()
			csv = WaitFileInside( sgTempDir )

			shutil.move( sgTempDir + '/' + csv, company.SourceFileHTMLFinancialsMorningstarBalanceSheet() )
			RemoveFiles( sgTempDir )

			#---

			print( '	- Ratios' )
			sgBrowser.get( company.SourceUrlFinancialsMorningstarRatios() )
			time.sleep( 1 )
			
			# with open( company.SourceFileHTMLFinancialsMorningstarRatios() + '.html', 'w' ) as output:
			#	output.write( sgBrowser.page_source )

			if os.path.exists( sgTempDir ):
				shutil.rmtree( sgTempDir )
			os.makedirs( sgTempDir )

			export = WaitElement( '//a[contains(@href,"exportKeyStat2CSV")]' )
			export.click()
			csv = WaitFileInside( sgTempDir )

			shutil.move( sgTempDir + '/' + csv, company.SourceFileHTMLFinancialsMorningstarRatios() )
			RemoveFiles( sgTempDir )
			
			#---
			
			print( '	- Valuation' )
			sgBrowser.get( company.SourceUrlFinancialsMorningstarValuation() )
			time.sleep( 1 )
			
			valuation = WaitElement( '//li[@data-link="sal-components-valuation"]//button' )
			valuation.click()
			WaitNoElement( '//a[@data-anchor="valuation"]/..//sal-components-valuation' )
			# WaitNoElement( '//a[@data-anchor="valuation"]/..//span[contains(text(), "There is no Valuation data available")]' )

			with open( company.SourceFileHTMLFinancialsMorningstarValuation(), 'w' ) as output:
				output.write( sgBrowser.page_source )
				
			shutil.rmtree( sgTempDir )

		time.sleep( 1 )

def DownloadFinancialsFV( iCompanies ):
	for company in iCompanies:
		print( 'Download financials Finviz: {} ...'.format( company.mName ) )
		
		if company.mFVSymbol:
			r = requests.get( company.SourceUrlFinancialsFV() )
			with open( company.SourceFileHTMLFinancialsFV(), 'w' ) as output:
				output.write( r.text )
			
		time.sleep( 1 )

def DownloadFinancialsR( iCompanies ):
	for company in iCompanies:
		print( 'Download financials Reuters: {} ...'.format( company.mName ) )
		
		if company.mRSymbol:
			r = requests.get( company.SourceUrlFinancialsR() )
			with open( company.SourceFileHTMLFinancialsR(), 'w' ) as output:
				output.write( r.text )
			
		time.sleep( 1 )

def DownloadFinancialsYF( iCompanies ):
	for company in iCompanies:
		print( 'Download financials YahooFinance: {} ...'.format( company.mName ) )
		
		if company.mYFSymbol:
			r = requests.get( company.SourceUrlFinancialsYF() )
			with open( company.SourceFileHTMLFinancialsYF(), 'w' ) as output:
				output.write( r.text )
			
		time.sleep( 1 )

def DownloadFinancialsB( iCompanies ):
	for company in iCompanies:
		print( 'Download financials Boerse: {} ...'.format( company.mName ) )
		
		if company.mBName:
			r = requests.get( company.SourceUrlFinancialsB() )
			with open( company.SourceFileHTMLFinancialsB(), 'w' ) as output:
				output.write( r.text )
			
		time.sleep( 1 )

#---

def DownloadSociety( iCompanies ):
	for company in iCompanies:
		print( 'Download society: {} ...'.format( company.mName ) )
		
		r = requests.get( company.SourceUrlSocietyZB() )
		with open( company.SourceFileHTMLSocietyZB(), 'w' ) as output:
			output.write( r.text )
			
		time.sleep( 1 )

#---

def DownloadStockPrice( iCompanies ):
	for company in iCompanies:
		print( 'Download images: {} ...'.format( company.mName ) )
		
		r = requests.get( company.SourceUrlStockPriceZB( 9999, 320, 260 ) )
		with open( company.SourceFileIMG( 9999 ), 'wb' ) as output:
			output.write( r.content )
			
		time.sleep( 1 )

		r = requests.get( company.SourceUrlStockPriceZB( 120, 570, 430 ) )
		with open( company.SourceFileIMG( 10 ), 'wb' ) as output:
			output.write( r.content )

		time.sleep( 1 )

		r = requests.get( company.SourceUrlStockPriceZB( 60, 570, 430 ) )
		with open( company.SourceFileIMG( 5 ), 'wb' ) as output:
			output.write( r.content )

		time.sleep( 1 )

		r = requests.get( company.SourceUrlStockPriceZB( 24, 570, 430 ) )
		with open( company.SourceFileIMG( 2 ), 'wb' ) as output:
			output.write( r.content )

		time.sleep( 1 )

#---

def DownloadDividends( iCompanies ):
	global sgBrowser
	
	BrowserInit()

	for company in iCompanies:
		print( 'Download dividends: {} ...'.format( company.mName ) )
		
		if company.mTSName:
			r = requests.get( company.SourceUrlDividendsTS() )
			with open( company.SourceFileHTMLDividendsTS(), 'w' ) as output:
				output.write( r.text )

		time.sleep( 1 )

		if company.mFCName:
			r = requests.get( company.SourceUrlDividendsFC() )
			with open( company.SourceFileHTMLDividendsFC(), 'w' ) as output:
				output.write( r.text )
			
		time.sleep( 1 )




