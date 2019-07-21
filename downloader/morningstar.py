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

import os
import shutil
import time

from selenium.webdriver.common.keys import Keys

from colorama import init, Fore, Back, Style

class cMorningstar:
	def __init__( self ):
		pass
	
	def Download( self, iBrowser, iCompany ):
		print( '	Morningstar ...' )

		if os.path.exists( iBrowser.Options().TempDirectory() ):
			shutil.rmtree( iBrowser.Options().TempDirectory() )
		os.makedirs( iBrowser.Options().TempDirectory() )

		if not iCompany.mMorningstar.Region():
			print( Fore.CYAN + '	skipping ... (no id)' )
			return

		#---

		self._DownloadIncomeStatement( iBrowser, iCompany )
		self._DownloadBalanceSheet( iBrowser, iCompany )
		self._DownloadRatios( iBrowser, iCompany )
		self._DownloadQuote( iBrowser, iCompany )
		self._DownloadValuation( iBrowser, iCompany )
		self._DownloadDividends( iBrowser, iCompany )
		
		shutil.rmtree( iBrowser.Options().TempDirectory() )
	
	#---
		
	def _DownloadIncomeStatement( self, iBrowser, iCompany ):
		print( '		- Income Statement' )

		if not iBrowser.Options().ForceDownload() and os.path.exists( iCompany.DataPathFile( iCompany.mMorningstar.FileNameIncomeStatement() ) ):
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return
		
		iBrowser.Driver().get( iCompany.mMorningstar.UrlIncomeStatement() )
		time.sleep( 1 )
		
		# with open( iCompany.DataPathFile( iCompany.mMorningstar.FileNameIncomeStatement() ) + '.html', 'w' ) as output:
		#	output.write( iBrowser.Driver().page_source )

		export = iBrowser.WaitElement( '//a[contains(@href,"SRT_stocFund.Export")]', 5 )
		if export is None:
			iBrowser.Driver().get( iCompany.mMorningstar.UrlIncomeStatement() );	# Not refresh, because sometimes the url is something like '...coming-soon.php'
			export = iBrowser.WaitElement( '//a[contains(@href,"SRT_stocFund.Export")]' )
		export.click()
		csv = iBrowser.WaitFileInside( iBrowser.Options().TempDirectory() )
		# Sometimes (now...), the file has 0 octet
		# Try to re-download it by clicking on the button
		# (Try this first, without refreshing the page)
		while not os.stat( os.path.join( iBrowser.Options().TempDirectory(), csv ) ).st_size:
			print( Fore.YELLOW + 'empty csv file: {}'.format( os.path.join( iBrowser.Options().TempDirectory(), csv ) ) )
			iBrowser.RemoveFiles( iBrowser.Options().TempDirectory() )
			export.click()
			csv = iBrowser.WaitFileInside( iBrowser.Options().TempDirectory() )

		shutil.copy( os.path.join( iBrowser.Options().TempDirectory(), csv ), iCompany.DataPathFile( iCompany.mMorningstar.FileNameIncomeStatement() ) )
		time.sleep( 1 )
		iBrowser.RemoveFiles( iBrowser.Options().TempDirectory() )

	def _DownloadBalanceSheet( self, iBrowser, iCompany ):
		print( '		- Balance Sheet' )

		if not iBrowser.Options().ForceDownload() and os.path.exists( iCompany.DataPathFile( iCompany.mMorningstar.FileNameBalanceSheet() ) ):
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return
		
		iBrowser.Driver().get( iCompany.mMorningstar.UrlBalanceSheet() )
		time.sleep( 1 )
		
		export = iBrowser.WaitElement( '//a[contains(@href,"SRT_stocFund.Export")]', 5 )
		if export is None:
			iBrowser.Driver().get( iCompany.mMorningstar.UrlBalanceSheet() )
			export = iBrowser.WaitElement( '//a[contains(@href,"SRT_stocFund.Export")]' )
		export.click()
		csv = iBrowser.WaitFileInside( iBrowser.Options().TempDirectory() )
		while not os.stat( os.path.join( iBrowser.Options().TempDirectory(), csv ) ).st_size:
			print( Fore.YELLOW + 'empty csv file: {}'.format( os.path.join( iBrowser.Options().TempDirectory(), csv ) ) )
			iBrowser.RemoveFiles( iBrowser.Options().TempDirectory() )
			export.click()
			csv = iBrowser.WaitFileInside( iBrowser.Options().TempDirectory() )

		shutil.copy( os.path.join( iBrowser.Options().TempDirectory(), csv ), iCompany.DataPathFile( iCompany.mMorningstar.FileNameBalanceSheet() ) )
		time.sleep( 1 )
		iBrowser.RemoveFiles( iBrowser.Options().TempDirectory() )

	def _DownloadRatios( self, iBrowser, iCompany ):
		print( '		- Ratios' )
		
		if not iBrowser.Options().ForceDownload() and os.path.exists( iCompany.DataPathFile( iCompany.mMorningstar.FileNameRatios() ) ):
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return
		
		iBrowser.Driver().get( iCompany.mMorningstar.UrlRatios() )
		time.sleep( 1 )
		
		export = iBrowser.WaitElement( '//a[contains(@href,"exportKeyStat2CSV")]', 5 )
		if export is None:
			iBrowser.Driver().get( iCompany.mMorningstar.UrlRatios() )
			export = iBrowser.WaitElement( '//a[contains(@href,"exportKeyStat2CSV")]' )
		export.click()
		csv = iBrowser.WaitFileInside( iBrowser.Options().TempDirectory() )
		while not os.stat( os.path.join( iBrowser.Options().TempDirectory(), csv ) ).st_size:
			print( Fore.YELLOW + 'empty csv file: {}'.format( os.path.join( iBrowser.Options().TempDirectory(), csv ) ) )
			iBrowser.RemoveFiles( iBrowser.Options().TempDirectory() )
			export.click()
			csv = iBrowser.WaitFileInside( iBrowser.Options().TempDirectory() )

		shutil.copy( os.path.join( iBrowser.Options().TempDirectory(), csv ), iCompany.DataPathFile( iCompany.mMorningstar.FileNameRatios() ) )
		time.sleep( 1 )
		iBrowser.RemoveFiles( iBrowser.Options().TempDirectory() )
		
	def _DownloadQuote( self, iBrowser, iCompany ):
		print( '		- Quote' )
		
		if not iBrowser.Options().ForceDownload() and os.path.exists( iCompany.DataPathFile( iCompany.mMorningstar.FileNameQuote() ) ):
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return
		
		iBrowser.Driver().get( iCompany.mMorningstar.UrlQuote() )
		time.sleep( 1 )

		iBrowser.Driver().find_element_by_tag_name( 'body' ).send_keys( Keys.HOME )
		
		quote = iBrowser.WaitElement( '//li[@id="stock__tab-quote"]//a' )
		quote.click()
		time.sleep( 1 )
		iBrowser.Driver().execute_script( 'window.scrollTo(0, document.body.scrollHeight);' )
		
		element = iBrowser.WaitElement( '//sal-components-company-profile//div[contains(@class,"sal-row") and not(contains(@class, "sal-blueprint"))]//div[contains(@class,"sal-component-company-profile-body")]', 5 )
		while element is None:
			iBrowser.Driver().refresh()
			quote = iBrowser.WaitElement( '//li[@id="stock__tab-quote"]//a' )
			quote.click()
			time.sleep( 1 )
			iBrowser.Driver().execute_script( 'window.scrollTo(0, document.body.scrollHeight);' )
			element = iBrowser.WaitElement( '//sal-components-company-profile//div[contains(@class,"sal-row") and not(contains(@class, "sal-blueprint"))]//div[contains(@class,"sal-component-company-profile-body")]', 5 )
		iBrowser.WaitElement( '//sal-components-company-profile//div[contains(@class,"sal-row") and not(contains(@class, "sal-blueprint"))]//div[contains(@class,"sal-component-company-profile-body")]' )
		
		with open( iCompany.DataPathFile( iCompany.mMorningstar.FileNameQuote() ), 'w' ) as output:
			output.write( iBrowser.Driver().page_source.replace( '<!---->', '<!-- -->' ) )
			
	def _DownloadValuation( self, iBrowser, iCompany ):
		print( '		- Valuation' )
		
		if not iBrowser.Options().ForceDownload() and os.path.exists( iCompany.DataPathFile( iCompany.mMorningstar.FileNameValuation() ) ):
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return
		
		iBrowser.Driver().get( iCompany.mMorningstar.UrlValuation() )
		time.sleep( 1 )
		
		iBrowser.Driver().find_element_by_tag_name( 'body' ).send_keys( Keys.HOME )
		
		valuation = iBrowser.WaitElement( '//li[@id="stock__tab-valuation"]//a' )
		valuation.click()
		time.sleep( 1 )
		element = iBrowser.WaitElement( '//sal-components//div[@mwc-id="salComponentsValuation"]', 5 )
		while element is None:
			iBrowser.Driver().refresh()
			valuation = iBrowser.WaitElement( '//li[@id="stock__tab-valuation"]//a' )
			valuation.click()
			time.sleep( 1 )
			element = iBrowser.WaitElement( '//sal-components//div[@mwc-id="salComponentsValuation"]', 5 )
		iBrowser.WaitElement( '//sal-components//div[@mwc-id="salComponentsValuation"]//table[contains(@class,"report-table")]' )
		
		with open( iCompany.DataPathFile( iCompany.mMorningstar.FileNameValuation() ), 'w' ) as output:
			output.write( iBrowser.Driver().page_source.replace( '<!---->', '<!-- -->' ) )
			
	def _DownloadDividends( self, iBrowser, iCompany ):
		print( '		- Dividends' )
		
		if not iBrowser.Options().ForceDownload() and os.path.exists( iCompany.DataPathFile( iCompany.mMorningstar.FileNameDividends() ) ):
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return
		
		iBrowser.Driver().get( iCompany.mMorningstar.UrlDividends() )
		time.sleep( 1 )
		
		iBrowser.Driver().find_element_by_tag_name( 'body' ).send_keys( Keys.HOME )
		
		dividends = iBrowser.WaitElement( '//li[@id="stock__tab-dividends"]//a' )
		dividends.click()
		time.sleep( 1 )
		element = iBrowser.WaitElement( '//sal-components//div[@mwc-id="salComponentsDividends"]', 5 )
		while element is None:
			iBrowser.Driver().refresh()
			dividends = iBrowser.WaitElement( '//li[@id="stock__tab-dividends"]//a' )
			dividends.click()
			time.sleep( 1 )
			element = iBrowser.WaitElement( '//sal-components//div[@mwc-id="salComponentsDividends"]', 5 )
		iBrowser.WaitElement( '//sal-components//div[@mwc-id="salComponentsDividends"]//table[contains(@class,"report-table")]' )

		with open( iCompany.DataPathFile( iCompany.mMorningstar.FileNameDividends() ), 'w' ) as output:
			output.write( iBrowser.Driver().page_source.replace( '<!---->', '<!-- -->' ) )
			