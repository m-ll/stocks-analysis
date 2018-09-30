#!/usr/bin/python3

import time
import copy
import requests
from bs4 import BeautifulSoup

from ..company import *

#---

def Extract( iCompany, iSoup ):
	div_data = iSoup.new_tag( 'div' )
	div_data['class'] = 'clear last10'
	
	if not iCompany.mYearsB:
		return div_data
	
	tbody = iSoup.new_tag( 'tbody' )
	
	#---
	
	td = iSoup.new_tag( 'th' )
	td.string = ''
	tr = iSoup.new_tag( 'tr' )
	tr.append( td )
	for year in iCompany.mYearsB:
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
	for value in iCompany.mPERB:
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
	for value in iCompany.mBNAB:
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
	for value in iCompany.mBNAGrowthB:
		td = iSoup.new_tag( 'td' )
		td.string = '{:.2f}%'.format( value * 100 )
		td['class'] = 'plus' if value >= 0 else 'minus'
		tr.append( td )
	td = iSoup.new_tag( 'td' )
	td.string = '~{:.2f}%'.format( iCompany.mBNAGrowthAverageLast5YB * 100 )
	td['class'] = 'plus' if iCompany.mBNAGrowthAverageLast5YB >= 0 else 'minus'
	tr.append( td )
	tbody.append( tr )
	
	#---
	
	td = iSoup.new_tag( 'th' )
	td.string = 'Dividende'
	tr = iSoup.new_tag( 'tr' )
	tr['class'] = 'imp'
	tr.append( td )
	for value in iCompany.mDividendB:
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
	for value in iCompany.mDividendGrowthB:
		td = iSoup.new_tag( 'td' )
		td.string = '{:.2f}%'.format( value * 100 )
		td['class'] = 'plus' if value >= 0 else 'minus'
		tr.append( td )
	td = iSoup.new_tag( 'td' )
	td.string = '~{:.2f}%'.format( iCompany.mDividendGrowthAverageLast5YB * 100 )
	td['class'] = 'plus' if iCompany.mDividendGrowthAverageLast5YB >= 0 else 'minus'
	tr.append( td )
	tbody.append( tr )
	
	#---
	
	td = iSoup.new_tag( 'th' )
	td.string = 'Rendement'
	tr = iSoup.new_tag( 'tr' )
	tr['class'] = 'imp'
	tr.append( td )
	for value in iCompany.mDividendYieldB:
		td = iSoup.new_tag( 'td' )
		td.string = value
		tr.append( td )
	td = iSoup.new_tag( 'td' )
	tr.append( td )
	tbody.append( tr )
	
	#---
	
	table = iSoup.new_tag( 'table' )
	table.append( tbody )
	
	div_data.append( table )
	
	return div_data;

