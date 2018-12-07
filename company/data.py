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

import re

class cData:
	def __init__( self, iParent=None, iComputeGrowthAverage=False ):
		self.mData = []
		self.mDataEstimated = []
		
		self.mTTM = ''
		self.mLatestQuarter = ''
		
		self.mComputeGrowthAverage=iComputeGrowthAverage
		self.mGrowthAverage = ''
		
		self.mParent = iParent
	
	def __repr__(self):
		return 'cData( [{}], [{}], "{}", "{}" )'.format( ', '.join( map( str, self.mData ) ), ', '.join( map( str, self.mDataEstimated ) ), self.mTTM, self.mLatestQuarter )
	
	#---
		
	def ComputeAverage( self, iData, iYears=8 ):
		if not iData:
			return
		
		data = []
		for value in iData:
			if not value:
				continue
			data.append( float( value ) )
			
		data = sorted( data[-1*iYears:] )
		# Remove the min/max value (if enough sample)
		if len( data ) >= 5:
			del( data[0] )
			del( data[-1] )
		
		return sum( data ) / float( len( data ) )
	
	def Update( self ):
		if self.mComputeGrowthAverage:
			self.mGrowthAverage = '{:.02f}'.format( self.ComputeAverage( self.mData + self.mDataEstimated ) )
	
	#---
		
	def SetRow( self, iRow ):
		if self.mParent is None:
			if iRow[-1] == 'TTM':
				self.mData = iRow[1:-1]
				self.mTTM = iRow[-1]
			elif iRow[-1].startswith( 'Latest' ):
				self.mData = iRow[1:-1]
				self.mLatestQuarter = iRow[-1]
			else:
				self.mData = iRow[1:]
		else:
			if self.mParent.mTTM:
				self.mData = iRow[1:-1]
				self.mTTM = iRow[-1]
			elif self.mParent.mLatestQuarter:
				self.mData = iRow[1:-1]
				self.mLatestQuarter = iRow[-1]
			else:
				self.mData = iRow[1:]
		
		self.mData = list( map( self._FixLocale, self.mData ) );
		self.mTTM = self._FixLocale( self.mTTM )
		self.mLatestQuarter = self._FixLocale( self.mLatestQuarter )
		
		self.Update()
			
	def _FixLocale( self, iString ):
		return iString.replace( ',', '.' ).replace( '(', '-' ).replace( ')', '' )
			
	#---
		
	def SetTR( self, iSoupSection, iTag, iText ):
		td = iSoupSection.find( iTag, string=iText )
		if not td and self.mParent:		# value doesn't exist, like EBITDA for CNP
			return
			
		if td.name == 'td':		# for years row
			td = td.find_next_sibling( 'td' )
			while td and 'Current' not in td.get_text( strip=True ):
				v = td.get_text( strip=True )
				self.mData.append( v )
				
				td = td.find_next_sibling( 'td' )
				
			self.mDataEstimated.append( td.get_text( strip=True ) )
			td = td.find_next_sibling( 'td' )
			self.mDataEstimated.append( td.get_text( strip=True ) )
			td = td.find_next_sibling( 'td' )
			self.mDataEstimated.append( td.get_text( strip=True ) )
			
		else:
			td = td.find_parent( 'td' )
			td = td.find_next_sibling( 'td' )
			while len( self.mData ) != len( self.mParent.mData ):
				v = td.get_text( strip=True )
				self.mData.append( v )
				
				td = td.find_next_sibling( 'td' )
			
			self.mDataEstimated.append( td.get_text( strip=True ) )
			td = td.find_next_sibling( 'td' )
			self.mDataEstimated.append( td.get_text( strip=True ) )
			td = td.find_next_sibling( 'td' )
			self.mDataEstimated.append( td.get_text( strip=True ) )
			
		self.mData = list( map( self._FixLocale2, self.mData ) );
		self.mDataEstimated = list( map( self._FixLocale2, self.mDataEstimated ) );
		
		self.Update()
			
	def _FixLocale2( self, iString ):
		return iString.replace( ',', '' ).replace( '—', '' )
		
	#---
		
	def SetTR2( self, iSoupTr ):
		if not self.mParent:		# for years row
			tds_past = iSoupTr.find_all( 'td', style=re.compile( '#eeeeee' ) )
			for td in tds_past:
				v = td.get_text( strip=True )
				self.mData.append( v )
				
			tds_estimated = iSoupTr.find_all( 'td', style=re.compile( '#dedede' ) )
			for td in tds_estimated:
				v = td.get_text( strip=True )
				self.mDataEstimated.append( v )
		
		else:
			td = iSoupTr.find( 'td' ).find_next_sibling( 'td' )
			while len( self.mData ) != len( self.mParent.mData ):
				v = td.get_text( strip=True )
				self.mData.append( v )
				
				td = td.find_next_sibling( 'td' )
			
			while len( self.mDataEstimated ) != len( self.mParent.mDataEstimated ):
				v = td.get_text( strip=True )
				self.mDataEstimated.append( v )
				
				td = td.find_next_sibling( 'td' )
			
		self.mData = list( map( self._FixLocale3, self.mData ) );
		self.mDataEstimated = list( map( self._FixLocale3, self.mDataEstimated ) );
		
		self.Update()
			
	def _FixLocale3( self, iString ):
		return iString.replace( ',', '.' ).replace( ' ', '' ).replace( '-', '' ).replace( '%', '' )
		