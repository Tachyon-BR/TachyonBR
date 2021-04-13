var url = '' + window.location.href;


if(url.slice(-1) === "/"){
  url += "?pageNumber=1&pageSize=20";
}
else{
  if(url.indexOf("pageNumber=") == -1 && url.indexOf("pageSize=") == -1){
    url += "&pageNumber=1&pageSize=20";
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


$('#pag').pagination({
    className: "paginationjs-big",
    ulClassName: "pagination pagination-lg",
    dataSource: "/propiedades/",
    pageLink: url,
    totalNumber: 300,
    pageNumber: 1,
    pageSize: 30,
    pageRange: 2,
    autoHidePrevious: true,
    autoHideNext: true,
    callback: function(data, pagination) {
        // template method of yourself
        var html = simpleTemplating(data);
        $('#data-container').html(html);
    }
})
