#!/usr/bin/env python3

import os
import requests
import shutil
import time

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

		export = iBrowser.WaitElement( '//a[contains(@href,"SRT_stocFund.Export")]' )
		export.click()
		csv = iBrowser.WaitFileInside( iBrowser.Options().TempDirectory() )

		shutil.move( os.path.join( iBrowser.Options().TempDirectory(), csv ), iCompany.DataPathFile( iCompany.mMorningstar.FileNameIncomeStatement() ) )
		iBrowser.RemoveFiles( iBrowser.Options().TempDirectory() )

	def _DownloadBalanceSheet( self, iBrowser, iCompany ):
		print( '		- Balance Sheet' )

		if not iBrowser.Options().ForceDownload() and os.path.exists( iCompany.DataPathFile( iCompany.mMorningstar.FileNameBalanceSheet() ) ):
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return
		
		iBrowser.Driver().get( iCompany.mMorningstar.UrlBalanceSheet() )
		time.sleep( 1 )
		
		export = iBrowser.WaitElement( '//a[contains(@href,"SRT_stocFund.Export")]' )
		export.click()
		csv = iBrowser.WaitFileInside( iBrowser.Options().TempDirectory() )

		shutil.move( os.path.join( iBrowser.Options().TempDirectory(), csv ), iCompany.DataPathFile( iCompany.mMorningstar.FileNameBalanceSheet() ) )
		iBrowser.RemoveFiles( iBrowser.Options().TempDirectory() )

	def _DownloadRatios( self, iBrowser, iCompany ):
		print( '		- Ratios' )
		
		if not iBrowser.Options().ForceDownload() and os.path.exists( iCompany.DataPathFile( iCompany.mMorningstar.FileNameRatios() ) ):
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return
		
		iBrowser.Driver().get( iCompany.mMorningstar.UrlRatios() )
		time.sleep( 1 )
		
		export = iBrowser.WaitElement( '//a[contains(@href,"exportKeyStat2CSV")]' )
		export.click()
		csv = iBrowser.WaitFileInside( iBrowser.Options().TempDirectory() )

		shutil.move( os.path.join( iBrowser.Options().TempDirectory(), csv ), iCompany.DataPathFile( iCompany.mMorningstar.FileNameRatios() ) )
		iBrowser.RemoveFiles( iBrowser.Options().TempDirectory() )
		
	def _DownloadValuation( self, iBrowser, iCompany ):
		print( '		- Valuation' )
		
		if not iBrowser.Options().ForceDownload() and os.path.exists( iCompany.DataPathFile( iCompany.mMorningstar.FileNameValuation() ) ):
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return
		
		iBrowser.Driver().get( iCompany.mMorningstar.UrlValuation() )
		time.sleep( 1 )
		
		valuation = iBrowser.WaitElement( '//li[@data-link="#sal-components-valuation"]//button' )
		valuation.click()
		iBrowser.WaitNoElement( '//a[@data-anchor="valuation"]/..//sal-components-valuation' )
		iBrowser.WaitNoElement( '//a[@data-anchor="valuation"]/..//sal-components-report-table' )

		with open( iCompany.DataPathFile( iCompany.mMorningstar.FileNameValuation() ), 'w' ) as output:
			output.write( iBrowser.Driver().page_source )
			
	def _DownloadDividends( self, iBrowser, iCompany ):
		print( '		- Dividends' )
		
		if not iBrowser.Options().ForceDownload() and os.path.exists( iCompany.DataPathFile( iCompany.mMorningstar.FileNameDividends() ) ):
			print( Fore.CYAN + '		skipping ... (existing file)' )
			return
		
		iBrowser.Driver().get( iCompany.mMorningstar.UrlDividends() )
		time.sleep( 1 )
		
		dividends = iBrowser.WaitElement( '//li[@data-link="#sal-components-dividends"]//button' )
		dividends.click()
		iBrowser.WaitNoElement( '//a[@data-anchor="dividends"]/..//sal-components-dividends' )
		iBrowser.WaitNoElement( '//a[@data-anchor="dividends"]/..//sal-components-report-table' )		# It's maybe needed to make 2 requests for the same page (valuation/dividends) to be sure to have not this element from valuation

		with open( iCompany.DataPathFile( iCompany.mMorningstar.FileNameDividends() ), 'w' ) as output:
			output.write( iBrowser.Driver().page_source )
			