var url = '' + window.location.href;


var searchParams = new URLSearchParams(window.location.search);

if(`${searchParams.get("pageNumber")}` != "null"){
  pageNumber = `${searchParams.get("pageNumber")}`;
}

if(`${searchParams.get("pageSize")}` != "null"){
  pageSize = `${searchParams.get("pageSize")}`;
}

if(url.slice(-1) === "/"){
  url += "?pageNumber="+ pageNumber +"&pageSize="+ pageSize;
}
else{
  if(url.indexOf("pageNumber=") == -1 && url.indexOf("pageSize=") == -1){
    url += "&pageNumber="+ pageNumber +"&pageSize="+ pageSize;
  }
}


function simpleTemplating(data) {
    var html = '<ul>';
    $.each(data, function(index, item){
        html += '<li>'+ item +'</li>';
    });
    html += '</ul>';
    return html;
}


$(document).ready(function() {
  $('#pag').pagination({
      className: "paginationjs-big",
      ulClassName: "pagination pagination-lg",
      dataSource: "/propiedades/",
      pageLink: url,
      totalNumber: 300,
      pageNumber: pageNumber,
      pageSize: pageSize,
      pageRange: 2,
      autoHidePrevious: true,
      autoHideNext: true,
      callback: function(data, pagination) {
          // template method of yourself
          var html = simpleTemplating(data);
          $('#data-container').html(html);
      }
  });

  $('.paginationjs-page').each(function(){
    $(this).find('a').attr('href', '');
  });
});
