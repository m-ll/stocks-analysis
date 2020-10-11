#!/usr/bin/env python3
#
# Copyright (c) 2019 m-ll. All Rights Reserved.
#
# Licensed under the MIT License.
# See LICENSE file in the project root for full license information.
#
# 2b13c8312f53d4b9202b6c8c0f0e790d10044f9a00d8bab3edf3cd287457c979
# 29c355784a3921aa290371da87bce9c1617b8584ca6ac6fb17fb37ba4a07d191
#

from datetime import date, datetime
from pathlib import Path
import platform
import pprint
import pyexcel_odsr as pe
import yaml

from colorama import init, Fore, Back, Style

class cConverter:
    def __init__( self, iConfig ):
        self.mConfig = iConfig

        self.mInputData = None
        self.mInputDataCTO = None
        self.mInputDataPEA = None

        self.mISINIndex = -1
        self.mNameIndex = -1
        self.mDateIndex = -1
        self.mTypeIndex = -1
        
        self.mOutputData = []

    def Build( self ):
        if 'buy-ods-path' not in self.mConfig:
            return

        buy_ods_path = self.mConfig['buy-ods-path']
        if platform.system().lower().startswith( 'cygwin' ):
            buy_ods_path = buy_ods_path.replace( '{DOCUMENTS}', '/cygdrive/d/Users/Mike/Documents' )
        elif platform.system().lower().startswith( 'linux' ):
            buy_ods_path = buy_ods_path.replace( '{DOCUMENTS}', '/mnt/d/Users/Mike/Documents' )
        elif platform.system().lower().startswith( 'windows' ):
            buy_ods_path = buy_ods_path.replace( '{DOCUMENTS}', 'D:/Users/Mike/Documents' )

        input_path = Path( buy_ods_path ).resolve()

        if not input_path.exists():
            print( Back.RED + f'[CONVERT] input path: {input_path}')
            return

        print( f'[CONVERT] input path: {input_path}')

        self.mInputData = pe.get_data( str(input_path) )
        self.mInputDataCTO = self.mInputData['cto data']
        self.mInputDataPEA = self.mInputData['pea data']

        self._FindIndexes()
        isins = self._FindISINs()
        self._BuildCompanies( isins )
    
    #---
    
    def _FindIndexes( self ):
        self.mISINIndex = self._FindIndex( 'ISIN' )
        self.mNameIndex = self._FindIndex( 'Company' )
        self.mDateIndex = self._FindIndex( 'Date' )
        self.mTypeIndex = self._FindIndex( 'Type' )
        
    def _FindIndex( self, iLabel ):
        for row in self.mInputDataCTO:
            for i, cell in enumerate( row ):
                if cell == iLabel:
                    return i
        
    #---
    
    def _FindISINs( self ):
        isins = set()
        for row in self.mInputDataCTO + self.mInputDataPEA:
            if not row:
                continue

            isin = row[self.mISINIndex]
            if len( isin ) == 12:
                isins.add( isin )

        return isins
    
    #---
    
    def _BuildCompanies( self, iISINs ):
        for isin in iISINs:
            for row in self.mInputDataCTO + self.mInputDataPEA:
                if not row:
                    continue
            
                cell_isin = row[self.mISINIndex]
                if cell_isin == isin and not any( data['isin'] == cell_isin for data in self.mOutputData ):
                    entry = {
                        'isin': cell_isin,
                        'name': row[self.mNameIndex],
                        'cto': [],
                        'pea': []
                    }

                    self.mOutputData.append( entry )

        for isin in iISINs:
            self._BuildCompany( isin, self.mInputDataCTO, 'cto' )
            self._BuildCompany( isin, self.mInputDataPEA, 'pea' )
        
    def _BuildCompany( self, iISIN, iInputData, iName ):
        state = 0
        for row in iInputData:
            if not row:
                continue
            
            if state == 0:
                cell_isin = row[self.mISINIndex]
                if cell_isin == iISIN:
                    state = 1

            elif state == 1:
                cell_isin = row[self.mISINIndex]
                if cell_isin == iISIN:
                    state = 0
                    continue
                
                try:
                    cell_type = row[self.mTypeIndex]
                except IndexError:
                    cell_type = ''
                if not cell_type or cell_type == 'div':
                    continue

                cell_date = row[self.mDateIndex]

                entry_buy = {
                    'date': cell_date, # is a <class 'datetime.date'>
                    # 'date': cell_date.strftime( '%d/%m/%Y' ),
                    'count': row[self.mTypeIndex+1],
                    'unit-price': float(row[self.mTypeIndex+2].split()[0])
                }

                entry = next( data for data in self.mOutputData if data['isin'] == iISIN )
                entry[iName].append( entry_buy )

    #---
    
    def Export( self ):
        if 'invest-path' not in self.mConfig:
            return None

        output_path = Path( self.mConfig['invest-path'] ).resolve()
        print( f'[CONVERT] output path: {output_path}')

        yaml.safe_dump( self.mOutputData, output_path.open( 'w' ) )
        
        return output_path
	