#!/usr/bin/python3

#---

def Extract( iCompany, iSoup ):
	div_info = iSoup.new_tag( 'div' )
	div_info['class'] = 'clear title'
	
	table = iCompany.mSSocietyZB.find( class_='tabElemNoBor' )
	
	div_info.append( table )
	
	return div_info

