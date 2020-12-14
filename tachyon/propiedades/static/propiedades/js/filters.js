

$( document ).ready(function() {

    //Cambiar los filtros si ya hay uno presente
    let searchParams = new URLSearchParams(window.location.search);
    //Campos select de hasta arriba
    $(`select option[value='${searchParams.get("tipo")}']`).attr("selected","selected");
    $(`select option[value='${searchParams.get("oferta")}']`).attr("selected","selected");
    $(`select option[value='${searchParams.get("estado")}']`).attr("selected","selected");

    let params = searchParams.keys();
    $(`.filter-click[data-name='tipo'][data-value='${searchParams.get("tipo")}'`).addClass("active-filter");
    $(`.filter-click[data-name='oferta'][data-value='${searchParams.get("oferta")}'`).addClass("active-filter");
    $(`.filter-click[data-name='estado'][data-value='${searchParams.get("estado")}'`).addClass("active-filter");
    $(`.filter-click[data-name='metros_terreno'][data-value='${searchParams.get("metros_terreno")}'`).addClass("active-filter");
    $(`.filter-click[data-name='metros_construccion'][data-value='${searchParams.get("metros_construccion")}'`).addClass("active-filter");
    
    

});


/* APILA LOS DIFERENTES FILTROS
obtiene los params del url
cacha los clicks del menu de filtros, 
dependiendo de cual filtro se hizo clik, lo agrega al stack de parametros de filtros
si se hace click a un filtro que ya existe, lo reemplaza
*/

$('.filter-click').on('click', function(){
    let name = $(this).attr("data-name");
    let value = $(this).attr("data-value");
    let searchParams = new URLSearchParams(window.location.search);

    if(name=="precio"){
        searchParams.set("precio_min", $("#precio_min").val());
        searchParams.set("precio_max", $("#precio_max").val());
    }else{
        searchParams.set(name, value);
    }
    
    let params = searchParams.keys();
    let url = "/propiedades/?";

    for(const param of params){
        url+=`&${param}=${searchParams.get(param)}`;
    }   
    window.location.href = url;
});

$(".clickToDeleteFilter").on("click", function(){
    let name = $(this).attr("data-filtername");
    let searchParams = new URLSearchParams(window.location.search);
    searchParams.delete(name);
    let url = "/propiedades/?";

    let params = searchParams.keys();
    for(const param of params){
        url+=`&${param}=${searchParams.get(param)}`;
    }   
    window.location.href = url;

});