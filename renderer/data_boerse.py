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

#---

def Data( iCompany, iSoup ):
	root = iSoup.new_tag( 'div' )
	root['class'] = ['boerse', 'last10']
	
	if not iCompany.mBoerse.mYears:
		return root
	
	tbody = iSoup.new_tag( 'tbody' )
	
	#---
	
	td = iSoup.new_tag( 'th' )
	td.string = ''
	tr = iSoup.new_tag( 'tr' )
	tr.append( td )
	for year in iCompany.mBoerse.mYears:
		td = iSoup.new_tag( 'th' )
		td.string = year
		tr.append( td )
	td = iSoup.new_tag( 'th' )
	td.string = 'Last 5 Years'
	tr.append( td )
	tbody.append( tr )
	
	#---
	
	td = iSoup.new_tag( 'th' )
	td.string = 'PER'
	tr = iSoup.new_tag( 'tr' )
	tr.append( td )
	for value in iCompany.mBoerse.mPER:
		td = iSoup.new_tag( 'td' )
		td.string = '{}'.format( value )
		tr.append( td )
	td = iSoup.new_tag( 'td' )
	tr.append( td )
	tbody.append( tr )
	
	#---
	
	td = iSoup.new_tag( 'th' )
	td.string = 'BNA'
	tr = iSoup.new_tag( 'tr' )
	tr['class'] = 'imp'
	tr.append( td )
	for value in iCompany.mBoerse.mBNA:
		td = iSoup.new_tag( 'td' )
		td.string = '{}'.format( value )
		tr.append( td )
	td = iSoup.new_tag( 'td' )
	tr.append( td )
	tbody.append( tr )
	
	td = iSoup.new_tag( 'th' )
	td.string = 'Croissance BNA'
	tr = iSoup.new_tag( 'tr' )
	tr.append( td )
	td = iSoup.new_tag( 'td' )	# empty first td
	tr.append( td )
	for value in iCompany.mBoerse.mBNAGrowth:
		td = iSoup.new_tag( 'td' )
		td.string = '{:.2f}%'.format( value * 100 )
		td['class'] = 'plus' if value >= 0 else 'minus'
		tr.append( td )
	td = iSoup.new_tag( 'td' )
	td.string = '~{:.2f}%'.format( iCompany.mBoerse.mBNAGrowthAverageLast5Y * 100 )
	td['class'] = 'plus' if iCompany.mBoerse.mBNAGrowthAverageLast5Y >= 0 else 'minus'
	tr.append( td )
	tbody.append( tr )
	
	#---
	
	td = iSoup.new_tag( 'th' )
	td.string = 'Dividende'
	tr = iSoup.new_tag( 'tr' )
	tr['class'] = 'imp'
	tr.append( td )
	for value in iCompany.mBoerse.mDividend:
		td = iSoup.new_tag( 'td' )
		td.string = '{}'.format( value )
		tr.append( td )
	td = iSoup.new_tag( 'td' )
	tr.append( td )
	tbody.append( tr )
	
	td = iSoup.new_tag( 'th' )
	td.string = 'Croissance Dividende'
	tr = iSoup.new_tag( 'tr' )
	tr.append( td )
	td = iSoup.new_tag( 'td' )	# empty first td
	tr.append( td )
	for value in iCompany.mBoerse.mDividendGrowth:
		td = iSoup.new_tag( 'td' )
		td.string = '{:.2f}%'.format( value * 100 )
		td['class'] = 'plus' if value >= 0 else 'minus'
		tr.append( td )
	td = iSoup.new_tag( 'td' )
	td.string = '~{:.2f}%'.format( iCompany.mBoerse.mDividendGrowthAverageLast5Y * 100 )
	td['class'] = 'plus' if iCompany.mBoerse.mDividendGrowthAverageLast5Y >= 0 else 'minus'
	tr.append( td )
	tbody.append( tr )
	
	#---
	
	td = iSoup.new_tag( 'th' )
	td.string = 'Rendement'
	tr = iSoup.new_tag( 'tr' )
	tr['class'] = 'imp'
	tr.append( td )
	for value in iCompany.mBoerse.mDividendYield:
		td = iSoup.new_tag( 'td' )
		td.string = value
		tr.append( td )
	td = iSoup.new_tag( 'td' )
	tr.append( td )
	tbody.append( tr )
	
	#---
	
	table = iSoup.new_tag( 'table' )
	table.append( tbody )
	
	root.append( table )
	
	return root
