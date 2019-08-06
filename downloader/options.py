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
from pathlib import Path
import re
import sys
import tempfile

class cOptions:
	def __init__( self ):
		self.mForceDownload = False
		self.mTempDirectory = ''
		self.mUserAgent = ''
		self.UserAgent( '' )

	def ForceDownload( self, iForceDownload=None ):
		if iForceDownload is None:
			return self.mForceDownload
		
		previous_value = self.mForceDownload
		self.mForceDownload = iForceDownload
		return previous_value
	
	def UserAgent( self, iUserAgent=None ):
		if iUserAgent is None:
			return self.mUserAgent
		
		previous_value = self.mUserAgent
		self.mUserAgent = iUserAgent
		if not self.mUserAgent:
			self.mUserAgent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
		return previous_value
	
	def TempDirectory( self, iTempDirectory=None ):
		if iTempDirectory is None:
			return Path( self.mTempDirectory )
		
		previous_value = self.mTempDirectory

		if not iTempDirectory:
			if sys.platform.startswith( 'cygwin' ):
				# current_path = os.path.abspath( '.' )
				# r'...' = raw string
				# >>> "\1"
				# '\x01'
				# >>> r"\1"
				# '\\1'
				# >>>
				# current_path = re.sub( r'/cygdrive/([a-z])', r'\1:', current_path ).upper() # '/cygdrive/c' -> 'C:'
				# current_path = current_path.replace( '/', '\\' )
				# self.mTempDirectory = current_path + '\\tmp'
				return 110, 'custom tmp folder must be set for cygwin' # Not a good idea to create/remove/create/remove/... many files on a USB key
			elif sys.platform.startswith( 'linux' ):
				self.mTempDirectory = tempfile.gettempdir() + '/tmp-stocks'
			else:
				return 100, 'platform is not managed'
		else:
			# if os.path.exists( os.path.normpath( iTempDirectory ) ) and os.listdir( iTempDirectory ):
			# 	return 200, 'custom tmp folder already exists and not empty'
			
			parent_dir = os.path.dirname( os.path.normpath( iTempDirectory ) )
			if not os.path.exists( parent_dir ):
				return 210, 'parent of custom tmp folder doesn\'t exist'

			if sys.platform.startswith( 'cygwin' ):
				iTempDirectory = re.sub( r'/cygdrive/([a-z])', r'\1:', iTempDirectory ) # '/cygdrive/c' -> 'c:'
				iTempDirectory = iTempDirectory.replace( '/', '\\' )

			self.mTempDirectory = iTempDirectory
		
		return Path( previous_value )
