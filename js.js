
$('.image-holder img').on('mousemove', function(e)
{
	$h = $( this ).parent().children( '.horizontal' );
	//$v = $( this ).parent().children( '.vertical' );
	
	$h.css( 'top', e.offsetY==undefined ? e.originalEvent.layerY:e.offsetY );
	//$v.css( 'left', e.offsetX==undefined ? e.originalEvent.layerX:e.offsetX );
});

$('.image-holder').on('mouseenter', function(e)
{
	$h = $( this ).children( '.horizontal' );
	//$v = $( this ).children( '.vertical' );
	
	if( !$h.length )
	{
		$h = $( document.createElement( 'div' ) );
		$h.addClass( 'horizontal' );
		$h.prependTo( $( this ) );
	}
	/*
	if( !$v.length )
	{
		$v = $( document.createElement( 'div' ) );
		$v.addClass( 'vertical' );
		$v.prependTo( $( this ) );
	}
	*/
	
	$h.show();
	//$v.show();
}).on('mouseleave', function(e)
{
	$h = $( this ).children( '.horizontal' );
	//$v = $( this ).children( '.vertical' );
	
	$h.hide();
	//$v.hide();
});

//---

$('.dividend-chart .title a.toggle').click( function(e)
{
	$( this ).closest( '.dividend-chart' ).children( '.chart' ).toggle();
	
	return false;
});

//---

$('[data-toggle="tooltip"]').click( function(e)
{
	let companies = $( this ).attr( 'data-companies' );
	companies = JSON.parse( companies );
	
	$( 'article[id]' ).hide();
	companies.forEach( company => $( '#' + company ).show() );
	
	return true;
});

$(function ()
{
	$('[data-toggle="tooltip"]').tooltip()
});

//---

$('.summary .name').click( function( iEvent )
{
	let $article = $( this ).closest( 'article' ).find( 'article' );

	if( !iEvent.ctrlKey )
	{
		$article.toggle();
		return false;
	}
		
	if( $article.is( ':hidden' ) )
		$('article > article').show();
	else
		$('article > article').hide();
	
	return false;
});

$('.stock-index header').click( function( iEvent )
{
	let $article = $( this ).closest( 'article' ).find( 'article' );

	$article.toggle();
	return false;
});

$(function ()
{
	$('article > article').hide();
});
