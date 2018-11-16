#!/usr/bin/env python3

from .zonebourse import cZoneBourse
from .finviz import cFinviz
from .morningstar import cMorningstar
from .yahoofinance import cYahooFinance
from .reuters import cReuters
from .boerse import cBoerse
from .tradingsat import cTradingSat
from .finances import cFinances

class cParser:
	def __init__( self ):
		pass
	
	def Parse( self, iCompanies ):
		for i, company in enumerate( iCompanies, start=1 ):
			print( 'Parse ({}/{}): {} ...'.format( i, len( iCompanies ), company.Name() ) )
			
			parser = cZoneBourse()
			parser.Parse( company )
			parser = cFinviz()
			parser.Parse( company )
			parser = cMorningstar()
			parser.Parse( company )
			parser = cReuters()
			parser.Parse( company )
			parser = cYahooFinance()
			parser.Parse( company )
			parser = cBoerse()
			parser.Parse( company )
			parser = cFinances()
			parser.Parse( company )
			parser = cTradingSat()
			parser.Parse( company )
			
			print( '' )
	