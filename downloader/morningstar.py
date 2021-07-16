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

import shutil
import time

from selenium.webdriver.common.keys import Keys

from colorama import init, Fore, Back, Style

class cMorningstar:
	def __init__( self ):
		pass
	
	def Download( self, iBrowser, iCompany ):
		print( '	Morningstar ...' )

		tmp_path = iBrowser.Options().TempDirectory()

		if tmp_path.exists():
			shutil.rmtree( tmp_path )
		tmp_path.mkdir( parents=True, exist_ok=True )

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
		
		shutil.rmtree( tmp_path )
	
	#---
		
	def _DownloadIncomeStatement( self, iBrowser, iCompany ):
		print( '		- Income Statement ' + Style.DIM + '[' + iCompany.mMorningstar.UrlIncomeStatement() + ']' )

		output = iCompany.DataPathFile( iCompany.mMorningstar.FileNameIncomeStatement() )

		if not iBrowser.Options().ForceDownload() and output.exists():
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return
		
		iBrowser.Driver().get( iCompany.mMorningstar.UrlIncomeStatement() )
		time.sleep( 1 )
		
		export = iBrowser.WaitElement( '//a[contains(@href,"SRT_stocFund.Export")]', 5 )
		if export is None:
			iBrowser.Driver().get( iCompany.mMorningstar.UrlIncomeStatement() );	# Not refresh, because sometimes the url is something like '...coming-soon.php'
			export = iBrowser.WaitElement( '//a[contains(@href,"SRT_stocFund.Export")]' )
		export.click()
		csv = iBrowser.WaitFileInside( iBrowser.Options().TempDirectory() )
		# Sometimes (now...), the file has 0 octet
		# Try to re-download it by clicking on the button
		# (Try this first, without refreshing the page)
		while not csv.stat().st_size:
			print( Fore.YELLOW + 'empty csv file: {}'.format( csv ) )
			iBrowser.RemoveFiles( iBrowser.Options().TempDirectory() )
			export.click()
			csv = iBrowser.WaitFileInside( iBrowser.Options().TempDirectory() )

		shutil.copyfile( csv, output ) # Just copy the content, doens't care of metadata (problem with wsl2)
		# shutil.copy( csv, output ) # Can't copy metadata ?! (https://bugs.python.org/issue38633)
		iBrowser.RemoveFiles( iBrowser.Options().TempDirectory() )

	def _DownloadBalanceSheet( self, iBrowser, iCompany ):
		print( '		- Balance Sheet ' + Style.DIM + '[' + iCompany.mMorningstar.UrlBalanceSheet() + ']' )

		output = iCompany.DataPathFile( iCompany.mMorningstar.FileNameBalanceSheet() )

		if not iBrowser.Options().ForceDownload() and output.exists():
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
		while not csv.stat().st_size:
			print( Fore.YELLOW + 'empty csv file: {}'.format( csv ) )
			iBrowser.RemoveFiles( iBrowser.Options().TempDirectory() )
			export.click()
			csv = iBrowser.WaitFileInside( iBrowser.Options().TempDirectory() )

		shutil.copyfile( csv, output ) # Just copy the content, doens't care of metadata (problem with wsl2)
		# shutil.copy( csv, output ) # Can't copy metadata ?! (https://bugs.python.org/issue38633)
		iBrowser.RemoveFiles( iBrowser.Options().TempDirectory() )

	def _DownloadRatios( self, iBrowser, iCompany ):
		print( '		- Ratios ' + Style.DIM + '[' + iCompany.mMorningstar.UrlRatios() + ']' )

		output = iCompany.DataPathFile( iCompany.mMorningstar.FileNameRatios() )
		
		if not iBrowser.Options().ForceDownload() and output.exists():
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
		while not csv.stat().st_size:
			print( Fore.YELLOW + 'empty csv file: {}'.format( csv ) )
			iBrowser.RemoveFiles( iBrowser.Options().TempDirectory() )
			export.click()
			csv = iBrowser.WaitFileInside( iBrowser.Options().TempDirectory() )

		shutil.copyfile( csv, output ) # Just copy the content, doens't care of metadata (problem with wsl2)
		# shutil.copy( csv, output ) # Can't copy metadata ?! (https://bugs.python.org/issue38633)
		iBrowser.RemoveFiles( iBrowser.Options().TempDirectory() )

	#---
		
	def _DownloadQuote( self, iBrowser, iCompany ):
		print( '		- Quote ' + Style.DIM + '[' + iCompany.mMorningstar.UrlQuote() + ']' )

		output = iCompany.DataPathFile( iCompany.mMorningstar.FileNameQuote() )
		
		if not iBrowser.Options().ForceDownload() and output.exists():
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return
		
		iBrowser.Driver().get( iCompany.mMorningstar.UrlQuote() )
		time.sleep( 1 )

		iBrowser.Driver().find_element_by_tag_name( 'body' ).send_keys( Keys.HOME )
		
		# Remove ads
		# Now, sometime it crashes inside the click (with <span class="mdc-button__content"> element), but can't find "mdc-button__content" and even "mdc-intro-ad" oO
		# elements = iBrowser.Driver().find_elements_by_xpath( '//div[contains(@class,"mdc-intro-ad")]//span[contains(text(), "Continue to Site")]' )
		# if elements:
		# 	elements[0].click()
		# 	time.sleep( 1 )
		
		# Beta ratio
		element = iBrowser.WaitElement( '//ul[contains(@class,"sal-component-band-grid")]//div[contains(text(), "Beta")]', 5 )
		while element is None:
			iBrowser.Driver().refresh()
			element = iBrowser.WaitElement( '//ul[contains(@class,"sal-component-band-grid")]//div[contains(text(), "Beta")]', 5 )
		iBrowser.WaitElement( '//ul[contains(@class,"sal-component-band-grid")]//div[contains(text(), "Beta")]', 5 )

		# iBrowser.Driver().execute_script( 'window.scrollTo(0, document.body.scrollHeight);' )
		
		# element = iBrowser.WaitElement( '//sal-components-company-profile//div[contains(@class,"sal-row") and not(contains(@class, "sal-blueprint"))]//div[contains(@class,"sal-component-company-profile-body")]', 5 )
		# while element is None:
		# 	iBrowser.Driver().refresh()
		# 	quote = iBrowser.WaitElement( '//a[@id="stock__tab-quote"]' )
		# 	quote.click()
		# 	time.sleep( 1 )
		# 	iBrowser.Driver().execute_script( 'window.scrollTo(0, document.body.scrollHeight);' )
		# 	element = iBrowser.WaitElement( '//sal-components-company-profile//div[contains(@class,"sal-row") and not(contains(@class, "sal-blueprint"))]//div[contains(@class,"sal-component-company-profile-body")]', 5 )
		# iBrowser.WaitElement( '//sal-components-company-profile//div[contains(@class,"sal-row") and not(contains(@class, "sal-blueprint"))]//div[contains(@class,"sal-component-company-profile-body")]' )
		
		with output.open( 'w' ) as o:
			o.write( iBrowser.Driver().page_source.replace( '<!---->', '<!-- -->' ) )
			
	def _DownloadValuation( self, iBrowser, iCompany ):
		print( '		- Valuation ' + Style.DIM + '[' + iCompany.mMorningstar.UrlValuation() + ']' )
		
		output = iCompany.DataPathFile( iCompany.mMorningstar.FileNameValuation() )

		if not iBrowser.Options().ForceDownload() and output.exists():
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return
		
		iBrowser.Driver().get( iCompany.mMorningstar.UrlValuation() )
		time.sleep( 1 )
		element = iBrowser.WaitElement( '//sal-components//div[@mwc-id="salComponentsValuation"]', 5 )
		while element is None:
			iBrowser.Driver().get( iCompany.mMorningstar.UrlValuation() )
			time.sleep( 1 )
			element = iBrowser.WaitElement( '//sal-components//div[@mwc-id="salComponentsValuation"]', 5 )
		iBrowser.WaitElement( '//sal-components//div[@mwc-id="salComponentsValuation"]//table[contains(@class,"report-table")]' )
		
		with output.open( 'w' ) as o:
			o.write( iBrowser.Driver().page_source.replace( '<!---->', '<!-- -->' ) )
			
	def _DownloadDividends( self, iBrowser, iCompany ):
		print( '		- Dividends ' + Style.DIM + '[' + iCompany.mMorningstar.UrlDividends() + ']' )

		output = iCompany.DataPathFile( iCompany.mMorningstar.FileNameDividends() )
		
		if not iBrowser.Options().ForceDownload() and output.exists():
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return
		
		iBrowser.Driver().get( iCompany.mMorningstar.UrlDividends() )
		time.sleep( 1 )
		element = iBrowser.WaitElement( '//sal-components//div[@mwc-id="salComponentsDividends"]', 5 )
		while element is None:
			iBrowser.Driver().get( iCompany.mMorningstar.UrlDividends() )
			time.sleep( 1 )
			element = iBrowser.WaitElement( '//sal-components//div[@mwc-id="salComponentsDividends"]', 5 )
		iBrowser.WaitElement( '//sal-components//div[@mwc-id="salComponentsDividends"]//table[contains(@class,"report-table")]' )

		with output.open( 'w' ) as o:
			o.write( iBrowser.Driver().page_source.replace( '<!---->', '<!-- -->' ) )
			