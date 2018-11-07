#!/usr/bin/python3

import os
import sys
import json
import argparse
from datetime import datetime
from process.company import *
from process.download.download import *
from process.extract.extract import *

from colorama import init, Fore, Back, Style
init( autoreset=True )

# https://graphseobourse.fr/classement-des-entreprises-les-plus-innovantes-du-monde/

#---

# https://www.suredividend.com/warren-buffett-stocks/

#PATCH: to remove 'pseudo' comments
data = ''
with open( 'companies.json' ) as file:
	for line in file:
		if '#' not in line:
			data += line
#PATCH
			
data_groups = json.loads( data )
	
#---
		
parser = argparse.ArgumentParser( description='Process group(s).' )
parser.add_argument( 'groups', metavar='Group', nargs='*', help='One (or multiple) group(s) name')
parser.add_argument( '--download', choices=['no', 'yes', 'force'], default='yes', help='Download source' )
parser.add_argument( '--suffix', help='Set suffix of output folder', required=True )
args = parser.parse_args()

SetForceDownload( args.download == 'force' )

if not os.path.exists( 'geckodriver' ):
	print( Back.RED + 'You need to download "geckodriver" file and move it next to this file' )
	sys.exit()

#---

# Create output directories (_output-xxx and _output-xxx/img)
output_name = f'_output-{args.suffix}'
os.makedirs( output_name, exist_ok=True )
image_name = 'img'
output_image_name = f'{output_name}/{image_name}'
os.makedirs( output_image_name, exist_ok=True )

# Create input (data) directory (_data-xxx)
data_name = f'_data-{args.suffix}'
os.makedirs( data_name, exist_ok=True )

#---

companies = []

# Create a list of all companies
for data_group_name in data_groups:
	for data in data_groups[data_group_name]:
		company = cCompany( data[0], data[1], data[2], data[3], 
							data[4], data[5], 
							data[6], 
							data[7], data[8], data[9], 
							data[10], data[11] )
		company.Group( data_group_name )
		company.DataDir( data_name )
		company.ImageDir( image_name )
		
		companies.append( company )

#---

# If no group as argument, take them all
if not args.groups:
	for data_group_name in data_groups:
		args.groups.append( data_group_name )

#---

for group in args.groups:
	companies_of_current_group = list( filter( lambda v: v.mGroup == group, companies ) )
	
	print( 'Group: {} ({})'.format( group, len( companies_of_current_group ) ) )
	
	if args.download in ['yes', 'force']:
		DownloadFinancialsMorningstar( companies_of_current_group )
		DownloadFinancialsZB( companies_of_current_group )
		DownloadFinancialsFV( companies_of_current_group )
		DownloadFinancialsR( companies_of_current_group )
		DownloadFinancialsYF( companies_of_current_group )
		DownloadFinancialsB( companies_of_current_group )
		DownloadSociety( companies_of_current_group )
		DownloadStockPrice( companies_of_current_group )
		DownloadDividends( companies_of_current_group )
	
	Fill( companies_of_current_group )
	
	companies_sorted_by_yield = sorted( companies_of_current_group, key=lambda company: company.mYieldCurrent, reverse=True )

	content_html = Extract( companies_sorted_by_yield )

	print( 'Write html ...' )
	with open( '{}/{}-[{}].html'.format( output_name, group, len( companies_sorted_by_yield ) ), 'w' ) as output:
		output.write( content_html )
		
	WriteImages( companies_sorted_by_yield, output_name )
	
	print( '' )
	
#---

# Clean	
BrowserQuit()
