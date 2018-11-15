
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
