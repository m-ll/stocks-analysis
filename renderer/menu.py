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

#---

def Sectors( iCompanies, iSoup ):
	root = iSoup.new_tag( 'ul' )
	root['class'] = 'sectors'
	
	sectors = {}
	sectors['All'] = { 'eu': [], 'us': [], 'all': [] }
	for company in iCompanies:
		sector = '{}-{}'.format( company.mMorningstar.mQuoteSector, company.mMorningstar.mQuoteIndustry )
		if sector not in sectors.keys():
			sectors[sector] = { 'eu': [], 'us': [], 'all': [] }

		sectors[sector]['all'].append( company.Name() )
		sectors['All']['all'].append( company.Name() )

		if company.Zone() == 'us':
			sectors[sector]['us'].append( company.Name() )
			sectors['All']['us'].append( company.Name() )
		else:
			sectors[sector]['eu'].append( company.Name() )
			sectors['All']['eu'].append( company.Name() )

	for sector, value in sorted( sectors.items(), key=lambda t: t[0] ):
		ssector = iSoup.new_tag( 'li' )
		ssector['class'] = 'sector'

		companies = value['all']
		sentry = iSoup.new_tag( 'a', href='#' + companies[0] if len( companies ) else '', title='<br>'.join( companies ) )
		sentry['data-toggle'] = 'tooltip'
		sentry['data-placement'] = 'bottom'
		sentry['data-html'] = 'true'
		sentry['data-companies'] = '[' + ', '.join( '"' + c + '"' for c in companies ) + ']'
		sentry['class'] = 'name'
		sentry.string = '{}'.format( sector )
		ssector.append( sentry )
		
		sentry = iSoup.new_tag( 'a', href='#' + companies[0] if len( companies ) else '', title='<br>'.join( companies ) )
		sentry['data-toggle'] = 'tooltip'
		sentry['data-placement'] = 'bottom'
		sentry['data-html'] = 'true'
		sentry['data-companies'] = '[' + ', '.join( '"' + c + '"' for c in companies ) + ']'
		sentry['class'] = 'count-all'
		sentry.string = '{}'.format( len( companies ) )
		ssector.append( sentry )
		
		companies = value['us']
		sentry = iSoup.new_tag( 'a', href='#' + companies[0] if len( companies ) else '', title='<br>'.join( companies ) )
		sentry['data-toggle'] = 'tooltip'
		sentry['data-placement'] = 'bottom'
		sentry['data-html'] = 'true'
		sentry['data-companies'] = '[' + ','.join( '"' + c + '"' for c in companies ) + ']'
		sentry['class'] = 'count-us'
		sentry.string = '{} $'.format( len( companies ) )
		ssector.append( sentry )
		
		companies = value['eu']
		sentry = iSoup.new_tag( 'a', href='#' + companies[0] if len( companies ) else '', title='<br>'.join( companies ) )
		sentry['data-toggle'] = 'tooltip'
		sentry['data-placement'] = 'bottom'
		sentry['data-html'] = 'true'
		sentry['data-companies'] = '[' + ','.join( '"' + c + '"' for c in companies ) + ']'
		sentry['class'] = 'count-eu'
		sentry.string = '{} €'.format( len( companies ) )
		ssector.append( sentry )

		root.append( ssector )

	return root
