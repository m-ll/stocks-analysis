#!/usr/bin/env python3

import os
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
				current_path = current_path.replace( '/cygdrive/c', 'C:' )
				current_path = current_path.replace( '/cygdrive/d', 'D:' )
				current_path = current_path.replace( '/cygdrive/e', 'E:' )
				current_path = current_path.replace( '/', '\\' )
				self.mTempDirectory = current_path + '\\tmp'
			elif sys.platform.startswith( 'linux' ):
				self.mTempDirectory = tempfile.gettempdir() + '/tmp-stocks'
		else:
			self.mTempDirectory = iTempDirectory
		
		return previous_value
