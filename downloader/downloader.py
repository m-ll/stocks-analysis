#!/usr/bin/env python3

from .zonebourse import cZoneBourse
from .finviz import cFinviz
from .morningstar import cMorningstar
from .yahoofinance import cYahooFinance
from .reuters import cReuters
from .boerse import cBoerse
from .tradingsat import cTradingSat
from .finances import cFinances

class cDownloader:
	def __init__( self ):
		pass
	
	def Download( self, iBrowser, iCompanies ):
		for i, company in enumerate( iCompanies, start=1 ):
			print( 'Download ({}/{}): {} ...'.format( i, len( iCompanies ), company.Name() ) )
			
			dl = cZoneBourse()
			dl.Download( iBrowser, company )
			dl = cFinviz()
			dl.Download( iBrowser, company )
			dl = cMorningstar()
			dl.Download( iBrowser, company )
			dl = cYahooFinance()
			dl.Download( iBrowser, company )
			dl = cReuters()
			dl.Download( iBrowser, company )
			dl = cBoerse()
			dl.Download( iBrowser, company )
			dl = cTradingSat()
			dl.Download( iBrowser, company )
			dl = cFinances()
			dl.Download( iBrowser, company )
		
			print( '' )
	