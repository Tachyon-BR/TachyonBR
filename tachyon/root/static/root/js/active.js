$(".main_nav").on("click", function(){
   $(".main_nav").find(".active").removeClass("active");
   $(this).addClass("active");
});
