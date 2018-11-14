#!/usr/bin/python3

import time
import copy
import requests
from bs4 import BeautifulSoup

from ..company import *

#---

def Extract( iCompany, iSoup ):
	div_data = iSoup.new_tag( 'div' )
	div_data['class'] = 'clear'
	
	if iCompany.mSFinancialsZBTable:
		table = copy.copy( iCompany.mSFinancialsZBTable )
		table['class'] = 'float'
		del table.find( 'td' )['style']		# first td which limit width to 150px
		del table['style']
		tr_years = table.find( 'tr' ).find_next_sibling()
		div_data.append( table )
		
		tr_ca = tr_years.find_next_sibling()
		tr_ebitda = tr_ca.find_next_sibling()
		tr_net = tr_ebitda.find_next_sibling()
		tr_per = tr_net.find_next_sibling()
		tr_bna = tr_per.find_next_sibling()
		tr_dividends = tr_bna.find_next_sibling()
		tr_rendements = tr_dividends.find_next_sibling()
		
		#--- CA colors
		
		td = tr_ca.find( 'td' ).find_next_sibling( 'td' ).find_next_sibling( 'td' )
		while td:
			td_prev = td.find_previous_sibling( 'td' )
			s_prev = td_prev.string.strip().replace( ' ', '' ).replace( ',', '.' )
			s_current = td.string.strip().replace( ' ', '' ).replace( ',', '.' )
			if '-' in [ s_prev, s_current ]:
				td = td.find_next_sibling( 'td' )
				if not td.string:
					break
				continue
				
			previous = float( s_prev )
			current = float( s_current )
			td['class'] = td.get( 'class', [] ) + [ 'plus' if current - previous >= 0 else 'minus' ]
			
			td = td.find_next_sibling( 'td' )
			if not td.string:
				break
		
		#--- EBITDA colors
		
		td = tr_ebitda.find( 'td' ).find_next_sibling( 'td' ).find_next_sibling( 'td' )
		while td:
			td_prev = td.find_previous_sibling( 'td' )
			s_prev = td_prev.string.strip().replace( ' ', '' ).replace( ',', '.' )
			s_current = td.string.strip().replace( ' ', '' ).replace( ',', '.' )
			if '-' in [ s_prev, s_current ]:
				td = td.find_next_sibling( 'td' )
				if not td.string:
					break
				continue
				
			previous = float( s_prev )
			current = float( s_current )
			td['class'] = td.get( 'class', [] ) + [ 'plus' if current - previous >= 0 else 'minus' ]
			
			td = td.find_next_sibling( 'td' )
			if not td.string:
				break
		
		#--- NET colors
		
		td = tr_net.find( 'td' ).find_next_sibling( 'td' ).find_next_sibling( 'td' )
		while td:
			td_prev = td.find_previous_sibling( 'td' )
			s_prev = td_prev.string.strip().replace( ' ', '' ).replace( ',', '.' )
			s_current = td.string.strip().replace( ' ', '' ).replace( ',', '.' )
			if '-' in [ s_prev, s_current ]:
				td = td.find_next_sibling( 'td' )
				if not td.string:
					break
				continue
				
			previous = float( s_prev )
			current = float( s_current )
			td['class'] = td.get( 'class', [] ) + [ 'plus' if current - previous >= 0 else 'minus' ]
			
			td = td.find_next_sibling( 'td' )
			if not td.string:
				break
		
		#--- Add 'croissance' -5/+5 row
		
		tr_croissance_yf = copy.copy( tr_bna )
		tr_croissance_yf['class'] = tr_croissance_yf.get( 'class', [] ) + [ 'croissance5' ]
		td = tr_croissance_yf.find( 'td' )
		td.clear()
		a = iSoup.new_tag( 'a', href=iCompany.mYahooFinance.Url() )
		a.append( 'Croissance (YahooFinance) -5/0/+1/+5' )
		td.append( a )
		td = td.find_next_sibling()
		td.find( 'b' ).string = iCompany.mGrowthYF5['-5']
		td = td.find_next_sibling()
		td.find( 'b' ).string = ''
		td = td.find_next_sibling()
		td.find( 'b' ).string = iCompany.mGrowthYF5['0']
		td = td.find_next_sibling()
		td.find( 'b' ).string = iCompany.mGrowthYF5['+1']
		td = td.find_next_sibling()
		td.find( 'b' ).string = ''
		td = td.find_next_sibling()
		td.find( 'b' ).string = iCompany.mGrowthYF5['+5']
		td = td.find_next_sibling()
		td.string = ''
		td = td.find_next_sibling()
		
		tr_bna.insert_before( tr_croissance_yf )
		
		#--- Add 'croissance bna' row
		
		tr_croissance_bna = copy.copy( tr_bna )
		td = tr_croissance_bna.find( 'td' )
		td.string = 'Croissance BNA.'
		td = td.find_next_sibling()
		td.find( 'b' ).string = ''
		td = td.find_next_sibling()
		for bna_growth in iCompany.mBNAGrowth:
			td.find( 'b' ).string = '{:.2f}%'.format( bna_growth * 100.0 )
			if bna_growth < 0:
				td['style'] = 'background-color: rgba( 255, 0, 0, 0.25 ); ' + td.get( 'style', '' )
			else:
				td['style'] = 'background-color: rgba( 0, 255, 0, 0.25 ); ' + td.get( 'style', '' )
			td = td.find_next_sibling()
			
		td.find( 'b' ).string = ''
		td = td.find_next_sibling()
		if iCompany.mBNAGrowthAverage < 0:
			td['style'] = 'background-color: rgba( 255, 0, 0, 0.25 ); ' + td.get( 'style', '' )
		else:
			td['style'] = 'background-color: rgba( 0, 255, 0, 0.25 ); ' + td.get( 'style', '' )
		td.string = '~{:.2f}%'.format( iCompany.mBNAGrowthAverage * 100.0 )
		
		tr_bna.insert_after( tr_croissance_bna )
		
		#--- Add 'croissance bna' -5/+5 row
		
		tr_croissance_bna_fv = copy.copy( tr_bna )
		tr_croissance_bna_fv['class'] = tr_croissance_bna_fv.get( 'class', [] ) + [ 'croissance5' ]
		td = tr_croissance_bna_fv.find( 'td' )
		# td.string = 'Croissance BNA (Finviz) -5/0/+1/+5'
		td.clear()
		a = iSoup.new_tag( 'a', href=iCompany.mFinviz.Url() )
		a.append( 'Croissance BNA (Finviz) -5/0/+1/+5' )
		td.append( a )
		td = td.find_next_sibling()
		td.find( 'b' ).string = iCompany.mBNAGrowthFV5['-5']
		td = td.find_next_sibling()
		td.find( 'b' ).string = ''
		td = td.find_next_sibling()
		td.find( 'b' ).string = iCompany.mBNAGrowthFV5['0']
		td = td.find_next_sibling()
		td.find( 'b' ).string = iCompany.mBNAGrowthFV5['+1']
		td = td.find_next_sibling()
		td.find( 'b' ).string = ''
		td = td.find_next_sibling()
		td.find( 'b' ).string = iCompany.mBNAGrowthFV5['+5']
		td = td.find_next_sibling()
		td.string = ''
		td = td.find_next_sibling()
		
		tr_bna.insert_before( tr_croissance_bna_fv )
		
		#--- Add 'croissance bna' -5/-3/-1 row
		
		tr_croissance_bna_r = copy.copy( tr_bna )
		tr_croissance_bna_r['class'] = tr_croissance_bna_r.get( 'class', [] ) + [ 'croissance5' ]
		td = tr_croissance_bna_r.find( 'td' )
		# td.string = 'Croissance BNA (Reuters) -5/-3/-1'
		td.clear()
		a = iSoup.new_tag( 'a', href=iCompany.mReuters.Url() )
		a.append( 'Croissance BNA (Reuters) -5/-3/-1' )
		td.append( a )
		td = td.find_next_sibling()
		td.find( 'b' ).string = '{}%'.format( iCompany.mBNAGrowthR5['-5'] )
		td = td.find_next_sibling()
		td.find( 'b' ).string = '{}%'.format( iCompany.mBNAGrowthR5['-3'] )
		td = td.find_next_sibling()
		td.find( 'b' ).string = '{}%'.format( iCompany.mBNAGrowthR5['-1'] )
		td = td.find_next_sibling()
		td.find( 'b' ).string = ''
		td = td.find_next_sibling()
		td.find( 'b' ).string = ''
		td = td.find_next_sibling()
		td.find( 'b' ).string = ''
		td = td.find_next_sibling()
		td.string = ''
		td = td.find_next_sibling()
		
		tr_bna.insert_before( tr_croissance_bna_r )
		
		#--- Add 'croissance div' row
		
		tr_croissance_div = copy.copy( tr_dividends )
		td = tr_croissance_div.find( 'td' )
		td.string = 'Croissance Div.'
		td = td.find_next_sibling()
		td.find( 'b' ).string = ''
		td = td.find_next_sibling()
		for dividend_growth in iCompany.mDividendsGrowth:
			td.find( 'b' ).string = '{:.2f}%'.format( dividend_growth * 100.0 )
			if dividend_growth < 0:
				td['style'] = 'background-color: rgba( 255, 0, 0, 0.25 ); ' + td.get( 'style', '' )
			else:
				td['style'] = 'background-color: rgba( 0, 255, 0, 0.25 ); ' + td.get( 'style', '' )
			td = td.find_next_sibling()
			
		td.find( 'b' ).string = ''
		td = td.find_next_sibling()
		if iCompany.mDividendsGrowthAverage < 0:
			td['style'] = 'background-color: rgba( 255, 0, 0, 0.25 ); ' + td.get( 'style', '' )
		else:
			td['style'] = 'background-color: rgba( 0, 255, 0, 0.25 ); ' + td.get( 'style', '' )
		td.string = '~{:.2f}%'.format( iCompany.mDividendsGrowthAverage * 100.0 )
		
		tr_dividends.insert_after( tr_croissance_div )
		
		#--- Add '10 years result' row
		
		url = iCompany.SourceUrlDividendCalculator( iCompany.mYieldCurrent, iCompany.mDividendsGrowthAverage * 100, 10 )
		
		tr_10yearsresult = copy.copy( tr_dividends )
		itd = tr_10yearsresult.find( 'td' )
		# itd.string = 'After 10 years (dividend-calculator)'
		itd.clear()
		a = iSoup.new_tag( 'a', href=url )
		a.append( 'After 10 years (dividend-calculator)' )
		itd.append( a )
		itd = itd.find_next_sibling()
		itd.find( 'b' ).decompose()
		itd = itd.find_next_sibling()
		itd.find( 'b' ).decompose()
		itd = itd.find_next_sibling()
		itd.find( 'b' ).decompose()
		itd = itd.find_next_sibling()
		itd.find( 'b' ).decompose()
		td = itd
		itd = itd.find_next_sibling()
		itd.find( 'b' ).decompose()
		itd = itd.find_next_sibling()
		itd.find( 'b' ).decompose()
		# itd = itd.find_next_sibling()
		
		time.sleep( 2 )
		
		annual_average = iCompany.AskDividendCalculatorProjection( url )
		td.string = '{}'.format( annual_average )
		
		tr_rendements.insert_after( tr_10yearsresult )
		
		#--- Add '20 years result' row
		
		url = iCompany.SourceUrlDividendCalculator( iCompany.mYieldCurrent, iCompany.mDividendsGrowthAverage * 100, 20 )
		
		tr_20yearsresult = copy.copy( tr_dividends )
		itd = tr_20yearsresult.find( 'td' )
		# itd.string = 'After 20 years (dividend-calculator)'
		itd.clear()
		a = iSoup.new_tag( 'a', href=url )
		a.append( 'After 20 years (dividend-calculator)' )
		itd.append( a )
		itd = itd.find_next_sibling()
		itd.find( 'b' ).decompose()
		itd = itd.find_next_sibling()
		itd.find( 'b' ).decompose()
		itd = itd.find_next_sibling()
		itd.find( 'b' ).decompose()
		itd = itd.find_next_sibling()
		itd.find( 'b' ).decompose()
		td = itd
		itd = itd.find_next_sibling()
		itd.find( 'b' ).decompose()
		itd = itd.find_next_sibling()
		itd.find( 'b' ).decompose()
		# itd = itd.find_next_sibling()
		
		time.sleep( 2 )

		annual_average = iCompany.AskDividendCalculatorProjection( url )
		td.string = '{}'.format( annual_average )
		
		tr_10yearsresult.insert_after( tr_20yearsresult )
		
		
	per = iCompany.mSFinancialsZB.find( id='graphPER' )
	if per is not None:
		per['class'] = 'float'
		div_data.append( copy.copy( per ) )
	
	bnadiv = iCompany.mSFinancialsZB.find( id='graphBnaDiv' )
	if bnadiv is not None:
		bnadiv['class'] = 'float'
		div_data.append( copy.copy( bnadiv ) )
	
	img_max = iSoup.new_tag( 'img' )
	img_max['src'] = iCompany.DestinationFile( iCompany.mZoneBourse.FileNamePricesSimple( 9999 ) )
	div_data.append( img_max )

	#---
	
	for a in div_data.find_all( 'a', href='/formation/espace_pedagogique/BNA-440/' ):
		a.parent.parent['class'] = 'imp'

	for a in div_data.find_all( 'a', href='/formation/espace_pedagogique/Dividende-446/' ):
		a.parent.parent['class'] = 'imp'

	for a in div_data.find_all( 'a', href='/formation/espace_pedagogique/Rendement-267/' ):
		a.parent.parent['class'] = 'imp'
		
	return div_data;

