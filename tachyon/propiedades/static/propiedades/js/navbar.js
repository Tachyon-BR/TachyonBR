$(document).ready(function() {
  $(".main_nav").find(".active").removeClass("active");

  var url = window.location.href;
  
  if(url.includes("propiedades/enRevision")){
    $("#en_revision").addClass("active");  
  }
  else{
    $("#my_pro").addClass("active");
  }
  
});
