
var g_NumUnityDogs = 0;

var unityDog =
{
	Setup : function( element )
	{
		var webURL		= element.attr( "src" );
		var	defWidth	= element.attr( "width" );
		var defHeight	= element.attr( "height" );
	
		var unityelement = jQuery( "<div class=\"unitydog standard\"></div>" );
		
		// Add the controls
		var controls = jQuery( '<div class="controls"></div>' );
		
			var ctrl = jQuery( '<a class="make_fullscreen" ><img src="'+unitydogsettings.fullscreen+'"></a>' );
				ctrl.click( function(){ unityelement.addClass( 'fullscreen' ); unityelement.removeClass( 'standard' ); jQuery( 'BODY' ).addClass( 'unitydog_fullscreen' ); } );
			controls.append( ctrl );
		
			var ctrl = jQuery( '<a class="make_normal" ><img src="'+unitydogsettings.restore+'"></a>' );
				ctrl.click( function(){ unityelement.removeClass( 'fullscreen' ); unityelement.addClass( 'standard' ); jQuery( 'BODY' ).removeClass( 'unitydog_fullscreen' ); } );
			controls.append( ctrl );
			
		var playbutton = jQuery( '<div class="playbutton">&nbsp;</div>' );
		playbutton.click( function(){ unityDog.Play( unityelement, webURL ); } );
		
		unityelement.prepend( playbutton );
		unityelement.append( controls );
		
		element.replaceWith( unityelement );
	},
	
	Play : function( unityelement, webURL )
	{	
		var player = new UnityObject2( { width: "100%", height: "100%" } );
		
		// Stop all other instances
		unityDog.StopAll();
		
		// hide our play button
		unityelement.find( '.playbutton' ).hide();

		player.observeProgress( function ( progress ) 
		{
			switch( progress.pluginStatus ) 
			{
				case "broken":
					console.log( "Unity Player broken!" );
					return;
					break;
				case "missing":
					console.log( "Unity Player missing!" );
					return;
					break;
				case "installed":
					break;
				case "first":
					break;
			}

		});
		
		var plyelement = jQuery( '<div class="player"></div>' );
		unityelement.prepend( plyelement );

		player.initPlugin( plyelement[0], webURL );
	},
	
	StopAll : function()
	{
		jQuery( "DIV.unitydog .player" ).remove();
		jQuery( "DIV.unitydog .playbutton" ).show();
	}
}

jQuery(function()
{
	jQuery( 'unitydog' ).each( function( idx, element )
	{
		unityDog.Setup( jQuery( element ) );
	})
});