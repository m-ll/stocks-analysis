#!/usr/bin/python3

#---

def Extract( iCompany, iSoup ):
	div_graph = iSoup.new_tag( 'div' )
	div_graph['class'] = ['clear', 'image-holder']
	
	filenames = iCompany.mZoneBourse.FileNamesPricesIchimoku()
	
	img = iSoup.new_tag( 'img' )
	img['src'] = iCompany.OutputImgPathFileRelativeToHTMLFile( filenames[0] )
	div_graph.append( img )
	img = iSoup.new_tag( 'img' )
	img['src'] = iCompany.OutputImgPathFileRelativeToHTMLFile( filenames[1] )
	div_graph.append( img )
	
	br = iSoup.new_tag( 'br' )
	div_graph.append( br )
	
	img = iSoup.new_tag( 'img' )
	img['src'] = iCompany.OutputImgPathFileRelativeToHTMLFile( filenames[2] )
	div_graph.append( img )
	
	return div_graph
	
