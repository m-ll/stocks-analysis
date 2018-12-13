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
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from colorama import init, Fore, Back, Style

class cBrowser:
	def __init__( self, iOptions ):
		self.mDriver = None
		self.mOptions = iOptions
		
	def Options( self, iOptions=None ):
		if iOptions is None:
			return self.mOptions
		
		previous_value = self.mOptions
		self.mOptions = iOptions
		return previous_value
	
	def Driver( self ):
		return self.mDriver
		
	#---

	def Init( self ):
		if self.mDriver is not None:
			return

		opts = Options()
		# opts.add_argument( '--headless' )
		
		opts.set_preference( 'browser.privatebrowsing.autostart', True )

		opts.set_preference( 'browser.download.folderList', 2 );
		opts.set_preference( 'browser.download.manager.showWhenStarting', False );
		opts.set_preference( 'browser.download.dir', self.mOptions.TempDirectory() );
		opts.set_preference( 'browser.helperApps.neverAsk.saveToDisk', 'application/csv,text/csv,application/octet-stream,text/html' );

		self.mDriver = webdriver.Firefox( firefox_options=opts, executable_path=os.path.join( os.getcwd(), 'geckodriver' ) )
		self.mDriver.implicitly_wait( 2 ) # seconds
		
		self.mDriver.set_window_size( 1920, 1500 )
		# sgBrowser.set_window_position( 0, 500 )
		
	def Quit( self ):
		if self.mDriver is None:
			return
		
		self.mDriver.quit()
		
	#---
		
	def WaitElement( self, iXPath, iRange=0 ):
		for i in range(iRange):
			element = self.mDriver.find_elements_by_xpath( iXPath )
			if element and element[0].is_displayed():
				return element[0]
				
			print( Fore.YELLOW + 'sleep ({}) wait element: {}'.format( i, iXPath ) )
			time.sleep( 1 )
		
		if iRange:
			return None
		
		element = self.mDriver.find_elements_by_xpath( iXPath )
		while not element or not element[0].is_displayed():
			# print( self.mDriver.current_url )
			# self.mDriver.get( self.mDriver.current_url );
			# self.mDriver.refresh()
			
			print( Fore.YELLOW + 'sleep wait element: {}'.format( iXPath ) )
			time.sleep( 1 )
			element = self.mDriver.find_elements_by_xpath( iXPath )
		
		time.sleep( 1 )

		return element[0]
		
	def WaitFileInside( self, iDirectory ):
		files = os.listdir( iDirectory )
		while not files:
			print( Fore.YELLOW + 'sleep file refresh: {}'.format( iDirectory ) )
			time.sleep( 1 )
			files = os.listdir( iDirectory )

		return files[0]
		
	def RemoveFiles( self, iDirectory ):
		for file in os.listdir( iDirectory ):
			path_file = os.path.join( iDirectory, file )
			if os.path.isfile( path_file ):
				os.unlink( path_file )
				
		time.sleep( 1 )
