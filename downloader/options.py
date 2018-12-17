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
import re
import sys
import tempfile

class cOptions:
	def __init__( self ):
		self.mForceDownload = False
		self.mTempDirectory = ''

	def ForceDownload( self, iForceDownload=None ):
		if iForceDownload is None:
			return self.mForceDownload
		
		previous_value = self.mForceDownload
		self.mForceDownload = iForceDownload
		return previous_value
	
	def TempDirectory( self, iTempDirectory=None ):
		if iTempDirectory is None:
			return self.mTempDirectory
		
		previous_value = self.mTempDirectory
		
		if not iTempDirectory:
			if sys.platform.startswith( 'cygwin' ):
				current_path = os.path.abspath( '.' )
				# r'...' = raw string
				# >>> "\1"
				# '\x01'
				# >>> r"\1"
				# '\\1'
				# >>>
				current_path = re.sub( r'/cygdrive/([a-z])', r'\1:', current_path ).upper() # '/cygdrive/c' -> 'C:'
				current_path = current_path.replace( '/', '\\' )
				self.mTempDirectory = current_path + '\\tmp'
			elif sys.platform.startswith( 'linux' ):
				self.mTempDirectory = tempfile.gettempdir() + '/tmp-stocks'
		else:
			self.mTempDirectory = iTempDirectory
		
		return previous_value
