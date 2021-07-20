var params = new URLSearchParams(location.search);
params.delete('pageNumber');

var url = window.location.pathname + "?" + params.toString();

$(document).ready(function() {
  let i = 0;

  $('#pagination').append('<li id="first" class="page-item"><a class="page-link" href="'+ url +'&pageNumber=1" tabindex="-1">&#x226A</a></li>');
  $('#pagination').append('<li id="prev" class="page-item"><a class="page-link" href="'+ url +'&pageNumber='+ parseInt(pageNumber - 1) +'">Anterior</a></li>');
  if(pageNumber <= 1){
    $('#first').addClass('disabled');
    $('#prev').addClass('disabled');
  }

  if(pageNumber > 3 && totalPages > 5 && pageNumber < totalPages - 2){
    $('#pagination').append('<li id="pag-'+ parseInt(pageNumber - 3) +'" class="page-item disabled"><a class="page-link" href="#">...</a></li>');
    for(i = pageNumber - 2; i <= pageNumber + 2; i++){
      $('#pagination').append('<li id="pag-'+ i +'" class="page-item"><a class="page-link" href="'+ url +'&pageNumber='+ i +'">'+ i +'</a></li>');
      if(i == pageNumber){
        $('#pag-'+pageNumber).addClass('active');
      }
    }
    $('#pagination').append('<li id="pag-'+ parseInt(pageNumber + 3) +'" class="page-item disabled"><a class="page-link" href="#">...</a></li>');
  }
  else if(pageNumber <= 3 || totalPages <= 5){
    let limit = totalPages;
    if(totalPages > 5){
      limit = 5;
    }
    for(i = 1; i <= limit; i++){
      $('#pagination').append('<li id="pag-'+ i +'" class="page-item"><a class="page-link" href="'+ url +'&pageNumber='+ i +'">'+ i +'</a></li>');
      if(i == pageNumber){
        $('#pag-'+pageNumber).addClass('active');
      }
    }
  }

  $('#pagination').append('<li id="next" class="page-item"><a class="page-link" href="'+ url +'&pageNumber='+ parseInt(pageNumber + 1) +'">Siguiente</a></li>');
  $('#pagination').append('<li id="last" class="page-item"><a class="page-link" href="'+ url +'&pageNumber='+ totalPages +'">&#x226B</a></li>');
  if(pageNumber >= totalPages){
    $('#next').addClass('disabled');
    $('#last').addClass('disabled');
  }
});
