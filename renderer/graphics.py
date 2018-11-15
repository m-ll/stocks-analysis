#!/usr/bin/env python3

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
	