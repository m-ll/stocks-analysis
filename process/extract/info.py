#!/usr/bin/python3

import os
from bs4 import BeautifulSoup

from ..company import *

#---

def Extract( iCompany, iSoup ):
	div_info = iSoup.new_tag( 'div' )
	div_info['class'] = 'clear title'
	
	table = iCompany.mSSocietyZB.find( class_='tabElemNoBor' )
	
	div_info.append( table )
	
	return div_info

