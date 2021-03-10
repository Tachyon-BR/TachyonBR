$('.ml-auto').on("click",function(){
	$('.super-overlay').addClass("active");
	$('.text-right').addClass("active");
});
$('.menu_close').on("click",function(){
	$('.super-overlay').removeClass("active");
	$('.text-right').removeClass("active");
});