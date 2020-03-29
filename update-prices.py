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
import re
import requests
import sys

from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style
init( autoreset=True )

from downloader.options import cOptions # for UserAgent

#---
		
parser = argparse.ArgumentParser( description='Update prices.' )
parser.add_argument( 'directories', metavar='Directories', nargs='+', help='One (or multiple) directory(s) to update the price')
args = parser.parse_args()

#---

root_path = Path( '.' ).resolve()

for directory in args.directories:
    if directory == 'last':
        output_path = root_path / '_output'
        directory = [ element for element in output_path.glob( '*' ) if element.is_dir() ][-1]

    input_path = root_path / '_output' / directory
    if not input_path.exists():
        input_path = root_path / directory
        if not input_path.exists():
            print( Back.RED + f'Directory is not available: {directory}' )
            continue

    print( Fore.GREEN + f'Process: {input_path}' )

    input_files = [ element for element in input_path.glob( '*' ) if element.is_file() and element.suffix == '.html' and len( element.suffixes ) == 1 ]

    for input_file in input_files:
        soup = None
        with input_file.open( 'r' ) as fp:
            soup = BeautifulSoup( fp, 'html5lib' )
        
        if soup is None:
            continue
        
        #---
        
        srealtime_prices = soup.select( '.title .price.realtime .value' ) # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-by-css-class

        cached_requests = {}

        for srealtime_price in srealtime_prices:
            stitle = srealtime_price.find_parent( class_='title' )

            sprice = stitle.select( '.price.origin .value' )[0]

            ssociety = stitle.find( string=re.compile( '\[Societe\]' ) )
            link = ssociety.parent.get( 'href' )

            #---

            new_realtime_price = 0.0

            if link not in cached_requests:
                print( f'request realtime price ... ' + Style.DIM + link )
                options = cOptions()
                r = requests.get( link, headers={ 'User-Agent' : options.UserAgent() } )
                
                soup_zb = BeautifulSoup( r.text, 'html5lib' )
                snew_realtime_price = soup_zb.find( id='zbjsfv_dr' )
                
                new_realtime_price = float( snew_realtime_price.get_text( strip=True ) )
                cached_requests[link] = new_realtime_price
            else:
                new_realtime_price = cached_requests[link]

            srealtime_price.string = str( new_realtime_price )

            #---

            price = float( sprice.get_text( strip=True ) )

            if new_realtime_price > price:
                srealtime_price['class'].append( 'up' )
            elif new_realtime_price < price:
                srealtime_price['class'].append( 'down' )
            
            now = datetime.now()
            srealtime_price['title'] = now.strftime( '%d/%m/%Y - %H:%M:%S' )

        #---

        output_path = input_file.with_suffix( '.updated' + input_file.suffix )
        with output_path.open( 'w' ) as fp:
            fp.write( soup.prettify() )
            