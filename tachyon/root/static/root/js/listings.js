/* JS Document */

/******************************

[Table of Contents]

1. Vars and Inits
2. Set Header
3. Init Menu
4. Init Isotope


******************************/

$(document).ready(function()
{
	"use strict";

	/*

	1. Vars and Inits

	*/

	var header = $('.header');

	initMenu();
	initIsotope();

	setHeader();

	$(window).on('resize', function()
	{
		setHeader();

		setTimeout(function()
		{
			$(window).trigger('resize.px.parallax');
		}, 375);
	});

	$(document).on('scroll', function()
	{
		setHeader();
	});

	/*

	2. Set Header

	*/

	function setHeader()
	{
		if($(window).scrollTop() > 91)
		{
			header.addClass('scrolled');
		}
		else
		{
			header.removeClass('scrolled');
		}
	}

	/*

	3. Init Menu

	*/

	function initMenu()
	{
		if($('.menu').length && $('.hamburger').length)
		{
			var menu = $('.menu');
			var hamburger = $('.hamburger');
			var close = $('.menu_close');
			var superOverlay = $('.super_overlay');

			hamburger.on('click', function()
			{
				menu.toggleClass('active');
				superOverlay.toggleClass('active');
			});

			close.on('click', function()
			{
				menu.toggleClass('active');
				superOverlay.toggleClass('active');
			});

			superOverlay.on('click', function()
			{
				menu.toggleClass('active');
				superOverlay.toggleClass('active');
			});
		}
	}

	/*

	4. Init Isotope

	*/

	function initIsotope()
	{
		if($('.listings_container').length)
		{
			var grid = $('.listings_container');
			grid.isotope(
			{
				itemSelector:'.listing_box',
				layoutMode: 'fitRows',
				sortAscending: false,
				getSortData:
	            {
	            	price: function(itemElement)
	            	{
	            		var priceEle = $(itemElement).find('.listing_price').text().replace( '$', '' );
	            		priceEle = priceEle.replace(/\s/g, '');
									priceEle = priceEle.replace(/,/g, '');
	            		return parseFloat(priceEle);
	            	},
	            	area: function(itemElement)
	            	{
	            		var propertyArea = $(itemElement).find('.property_area span').text().replace(' m2', '');
	            		return parseFloat(propertyArea);
	            	},
								banos: function(itemElement)
	            	{
	            		var propertyBanos = $(itemElement).find('.property_banos span').text();
									if(propertyBanos == "" || propertyBanos == null){
										propertyBanos = 0;
									}
	            		return parseFloat(propertyBanos);
	            	},
								habs: function(itemElement)
	            	{
	            		var propertyHabs = $(itemElement).find('.property_habs span').text();
									if(propertyHabs == "" || propertyHabs == null){
										propertyHabs = 0;
									}
	            		return parseFloat(propertyHabs);
	            	},
								garaje: function(itemElement)
	            	{
	            		var propertyGaraje = $(itemElement).find('.property_garaje span').text();
									if(propertyGaraje == "" || propertyGaraje == null){
										propertyGaraje = 0;
									}
	            		return parseFloat(propertyGaraje);
	            	},
								date: function(itemElement)
	            	{
	            		var propertyDate = $(itemElement).find('.property_date').text();
									if(propertyDate == "" || propertyDate == null){
										propertyDate = 0;
									}
	            		return parseFloat(propertyDate);
	            	},
	            }
			});

			var sortingButtons = $('.sorting_button');

			sortingButtons.each(function()
	        {
	        	$(this).on('click', function()
	        	{
	        		var parent = $(this).parent().parent().find('span');
		        		parent.text($(this).text());
		        		var option = $(this).attr('data-isotope-option');
								if(sort == parent.text()){
									var temp = !bool;
									option = option.replace(bool.toString(), temp.toString());
									bool = !bool;
								}
								else{
									bool = false;
								}
								sort = parent.text();
		        		option = JSON.parse( option );
	    				grid.isotope( option );
	        	});
	        });
		}
	}

});
