#!/usr/bin/python3

#---

def Extract( iCompany, iSoup ):
	div_graph = iSoup.new_tag( 'div' )
	div_graph['class'] = 'clear'
	
	img_10 = iSoup.new_tag( 'img' )
	img_10['src'] = iCompany.OutputImgPathFileRelativeToHTMLFile( iCompany.mZoneBourse.FileNamePricesSimple( 10 ) )
	div_graph.append( img_10 )
	
	img_5 = iSoup.new_tag( 'img' )
	img_5['src'] = iCompany.OutputImgPathFileRelativeToHTMLFile( iCompany.mZoneBourse.FileNamePricesSimple( 5 ) )
	div_graph.append( img_5 )
	
	img_2 = iSoup.new_tag( 'img' )
	img_2['src'] = iCompany.OutputImgPathFileRelativeToHTMLFile( iCompany.mZoneBourse.FileNamePricesSimple( 2 ) )
	div_graph.append( img_2 )
	
	return div_graph
	
