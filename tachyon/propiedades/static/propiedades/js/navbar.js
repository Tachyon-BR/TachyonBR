$(document).ready(function() {
  $(".main_nav").find(".active").removeClass("active");

  var url = window.location.href;
  
  if(url.includes("propiedades/enRevision")){
    $("#en_revision").addClass("active");  
  }else if(url.includes("propiedades/mis-revisiones")){
    $("#mis_revisiones").addClass("active");  
  }else if(url.includes("propiedades/myProperties")){
    $("#my_pro").addClass("active");
  }else if(url.includes("propiedades/")){
    $("#properties").addClass("active");
  }
  
});
