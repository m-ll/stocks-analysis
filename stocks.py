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

import argparse
from datetime import datetime
import glob
from pathlib import Path
import sys
import yaml

from colorama import init, Fore, Back, Style
init( autoreset=True )

from converter.converter import cConverter
from company.company import cCompany, cStockIndex
from downloader.options import cOptions
from downloader.browser import cBrowser
from downloader.downloader import cDownloader
from parser.parser import cParser
from renderer.renderer import cRenderer

# https://graphseobourse.fr/classement-des-entreprises-les-plus-innovantes-du-monde/

# https://www.suredividend.com/warren-buffett-stocks/

#---
		
parser = argparse.ArgumentParser( description='Process group(s).' )
parser.add_argument( 'groups', metavar='Group', nargs='*', help='One (or multiple) group(s) name (may also be company name)')
parser.add_argument( '--download', choices=['no', 'yes', 'force'], default='yes', help='Download source' )
parser.add_argument( '--suffix', help='Set suffix of output folder', required=True )
parser.add_argument( '--tmp', default='', help='Set the tmp folder' ) # MUST NOT be None for cOptions
args = parser.parse_args()

if not glob.glob( 'geckodriver' ) and not glob.glob( 'chromedriver*' ):
	print( Back.RED + 'You need to download "geckodriver/chromedriver" file and move it next to this file' )
	sys.exit( 5 )

#---

root_path = Path( '.' ).resolve()

# Create input (data) directory (_data/xxx)
data_path = root_path / '_data' / args.suffix
data_path.mkdir( parents=True, exist_ok=True )

# Create output directories (_output/xxx and _output/xxx/img)
output_path = root_path / '_output' / args.suffix
output_path.mkdir( parents=True, exist_ok=True )

image_name = 'img'
output_path_img = output_path / image_name
output_path_img.mkdir( parents=True, exist_ok=True )

#---

options = cOptions()
options.ForceDownload( args.download == 'force' )
error = {}
options.TempDirectory( args.tmp, error )
if error['id']:
	print( Back.RED + 'tmp folder: {}'.format( args.tmp ) )
	print( Back.RED + 'error: {} - {}'.format( error['id'], error['message'] ) )
	sys.exit( 10 )

print( '[TMP] {}'.format( options.TempDirectory() ) )

browser = cBrowser( options )

#---

config_path = root_path / 'config.yaml'
if not config_path.exists():
	print( Back.RED + 'The config file doesn\'t exist: config.yaml' )
	sys.exit( 15 )

config = yaml.safe_load( config_path.open( 'r' ) )

#---

if 'companies-path' not in config:
	print( Back.RED + 'The key "companies-path" doesn\'t exist in the config file' )
	sys.exit( 20 )

companies_pathfile = root_path / config['companies-path']
if not companies_pathfile.exists():
	print( Back.RED + 'The companies file doesn\'t exist: {}'.format( companies_pathfile ) )
	sys.exit( 25 )

data_groups = yaml.safe_load( companies_pathfile.open( 'r' ) )

#---

converter = cConverter( config )
converter.Build()
invest_pathfile = converter.Export()

data_owned_invests = []
if invest_pathfile is not None and invest_pathfile.exists():
	data_owned_invests = yaml.safe_load( invest_pathfile.open( 'r' ) )

#---

companies = []

# Create a list of all companies
for data_group_name in data_groups:
	for data in data_groups[data_group_name]:
		company = cCompany( data[0], data[1], data[2], data[3], 
							data[4], 
							data[5], 
							data[6], data[7], 
							data[8], data[9], data[10], data[11], 
							data[12], data[13] )
		company.Group( data_group_name )
		company.DataPath( data_path )
		company.OutputImgPathRelativeToHTMLFile( image_name )

		data_invest = next( ( c for c in data_owned_invests if c['isin'] == data[0] ), None )
		if data_invest:
			company.Invested( data_invest )

		companies.append( company )

#---

# If no group as argument, take them all
if not args.groups:
	for data_group_name in data_groups:
		args.groups.append( data_group_name )

#---

cac40 = cStockIndex( 'FR0003500008', 'CAC-40', 'eu', r'%5EFCHI' )
sp500 = cStockIndex( 'SP500', 'S-P-500', 'us', r'%5EGSPC' )
stock_indexes = [ cac40, sp500 ]

for stock_index in stock_indexes:
	stock_index.Group( 'index' )
	stock_index.DataPath( data_path )

if args.download in ['yes', 'force']:
	browser.Init()
	downloader = cDownloader()
	downloader.Download( browser, stock_indexes )
	
parser = cParser()
parser.Parse( stock_indexes )

#---

for group in args.groups:
	companies_of_current_group = list( filter( lambda v: v.mGroup == group, companies ) )
	if not companies_of_current_group:
		companies_of_current_group = list( filter( lambda v: v.mName == group, companies ) )
	if not companies_of_current_group:
		continue
	
	print( 'Group: {} ({})'.format( group, len( companies_of_current_group ) ) )
	
	if args.download in ['yes', 'force']:
		browser.Init()
		downloader = cDownloader()
		downloader.Download( browser, companies_of_current_group )
		
	parser = cParser()
	parser.Parse( companies_of_current_group )
	
	# companies_sorted_by_yield = sorted( companies_of_current_group, key=lambda company: company.mMorningstar.mYieldCurrent, reverse=True )
	# companies_sorted_by_note = sorted( companies_sorted_by_yield, key=lambda company: company.Notation().StarsCount(), reverse=True )
	companies_sorted_by_note_yield = sorted( companies_of_current_group, key=lambda company: ( company.Notation().StarsCount(), company.mMorningstar.mYieldCurrent ), reverse=True )

	renderer = cRenderer( companies_sorted_by_note_yield )
	renderer.Render()
	renderer.Export( output_path )
	
	print( '' )
	
#---

browser.Quit()
