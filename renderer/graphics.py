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

import copy

#---

def PER( iCompany, iSoup ):
	root = iSoup.new_tag( 'span' )
	root['class'] = 'per'
	
	per = iCompany.mZoneBourse.mSoupPER
	if per is not None:
		root.append( copy.copy( per ) )
	
	return root

def BNA( iCompany, iSoup ):
	root = iSoup.new_tag( 'span' )
	root['class'] = 'bna'
	
	bna = iCompany.mZoneBourse.mSoupBNA
	if bna is not None:
		root.append( copy.copy( bna ) )
	
	return root

def PricesSimple( iCompany, iSoup, iYears ):
	root = iSoup.new_tag( 'span' )
	root['class'] = 'prices-simple'
	
	img = iSoup.new_tag( 'img', src=iCompany.OutputImgPathFileRelativeToHTMLFile( iCompany.mZoneBourse.FileNamePricesSimple( iYears ) ) )
	root.append( img )
	
	return root
	
def PricesIchimoku( iCompany, iSoup ):
	root = iSoup.new_tag( 'div' )
	root['class'] = ['graphics', 'ichimoku', 'image-holder']
	
	filenames = iCompany.mZoneBourse.FileNamesPricesIchimoku()
	
	img = iSoup.new_tag( 'img', src=iCompany.OutputImgPathFileRelativeToHTMLFile( filenames[0] ) )
	root.append( img )
	img = iSoup.new_tag( 'img', src=iCompany.OutputImgPathFileRelativeToHTMLFile( filenames[1] ) )
	root.append( img )
	
	br = iSoup.new_tag( 'br' )
	root.append( br )
	
	img = iSoup.new_tag( 'img', src=iCompany.OutputImgPathFileRelativeToHTMLFile( filenames[2] ) )
	root.append( img )
	
	return root
	