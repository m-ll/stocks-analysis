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

import os
import sys
import json
import argparse
import glob
from datetime import datetime

from colorama import init, Fore, Back, Style
init( autoreset=True )

from company.company import cCompany
from downloader.options import cOptions
from downloader.browser import cBrowser
from downloader.downloader import cDownloader
from parser.parser import cParser
from renderer.renderer import cRenderer

# https://graphseobourse.fr/classement-des-entreprises-les-plus-innovantes-du-monde/

# https://www.suredividend.com/warren-buffett-stocks/

#---

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
parser.add_argument( 'groups', metavar='Group', nargs='*', help='One (or multiple) group(s) name (may also be company name)')
parser.add_argument( '--download', choices=['no', 'yes', 'force'], default='yes', help='Download source' )
parser.add_argument( '--suffix', help='Set suffix of output folder', required=True )
parser.add_argument( '--tmp', default='', help='Set the tmp folder' ) # MUST NOT be None for cOptions
args = parser.parse_args()

if not glob.glob( 'geckodriver*.exe' ) and not glob.glob( 'chromedriver*.exe' ):
	print( Back.RED + 'You need to download "geckodriver/chromedriver" file and move it next to this file' )
	sys.exit()

sys.exit()

#---

root_path = os.path.abspath( '.' )

# Create input (data) directory (_data/xxx)
data_path = os.path.join( root_path, '_data', args.suffix )
os.makedirs( data_path, exist_ok=True )

# Create output directories (_output/xxx and _output/xxx/img)
output_path = os.path.join( root_path, '_output', args.suffix )
os.makedirs( output_path, exist_ok=True )

image_name = 'img'
output_path_img = os.path.join( output_path, image_name )
os.makedirs( output_path_img, exist_ok=True )

#---

options = cOptions()
options.ForceDownload( args.download == 'force' )
previous = options.TempDirectory( args.tmp )
if isinstance( previous, tuple ):
	error, message = previous
	print( Back.RED + 'tmp folder: {}'.format( args.tmp ) )
	print( Back.RED + 'error: {} - {}'.format( error, message ) )
	sys.exit()

browser = cBrowser( options )

#---

companies = []

# Create a list of all companies
for data_group_name in data_groups:
	for data in data_groups[data_group_name]:
		company = cCompany( data[0], data[1], data[2], data[3], 
							data[4], 
							data[5], data[6], 
							data[7], data[8], data[9], data[10], 
							data[11], data[12] )
		company.Group( data_group_name )
		company.DataPath( data_path )
		company.OutputImgPathRelativeToHTMLFile( image_name )
		
		companies.append( company )
		
#---

# If no group as argument, take them all
if not args.groups:
	for data_group_name in data_groups:
		args.groups.append( data_group_name )

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
	
	companies_sorted_by_yield = sorted( companies_of_current_group, key=lambda company: company.mMorningstar.mYieldCurrent, reverse=True )

	renderer = cRenderer( companies_sorted_by_yield )
	renderer.Render()
	renderer.Export( output_path )
	
	print( '' )
	
#---

if browser is not None:
	browser.Quit()
