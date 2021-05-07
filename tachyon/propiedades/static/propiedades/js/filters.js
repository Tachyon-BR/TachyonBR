

$( document ).ready(function() {

    $('#filtros_avanzados').hide()
    //Cambiar los filtros si ya hay uno presente
    let searchParams = new URLSearchParams(window.location.search);

    //Campos select de hasta arriba
    $(`select option[value='${searchParams.get("tipo")}']`).attr("selected","selected");
    $(`select option[value='${searchParams.get("oferta")}']`).attr("selected","selected");
    $(`select option[value='${searchParams.get("estado")}']`).attr("selected","selected");

    let otros = searchParams.getAll("otros[]");
    otros.forEach(element => {
        $(`[value="${element}"]`).prop('checked', true);
    });
    let rest = searchParams.getAll("rest[]");
    rest.forEach(element => {
        $(`[value="${element}"]`).prop('checked', true);
    });

    $(`.filter-click[data-name='tipo'][data-value='${searchParams.get("tipo")}'`).addClass("active-filter");
    $(`.filter-click[data-name='oferta'][data-value='${searchParams.get("oferta")}'`).addClass("active-filter");
    $(`.filter-click[data-name='estado'][data-value='${searchParams.get("estado")}'`).addClass("active-filter");
    $(`.filter-click[data-name='metros_terreno'][data-value='${searchParams.get("metros_terreno")}'`).addClass("active-filter");
    $(`.filter-click[data-name='metros_construccion'][data-value='${searchParams.get("metros_construccion")}'`).addClass("active-filter");
    $(`.filter-click[data-name='banos'][data-value='${searchParams.get("banos")}'`).addClass("active-filter");
    $(`.filter-click[data-name='pisos'][data-value='${searchParams.get("pisos")}'`).addClass("active-filter");
    $(`.filter-click[data-name='garage'][data-value='${searchParams.get("garage")}'`).addClass("active-filter");
    //$(`.filter-click[data-name='garage'][data-value='${searchParams.get("garage")}'`).attr("checked", "");
});

$('#toggle_chk').on('click', function(){
    $('#filtros_avanzados2').hide();
    $('#filtros_avanzados').toggle();
});

$('#toggle_chk2').on('click', function(){
    $('#filtros_avanzados').hide();
    $('#filtros_avanzados2').toggle();
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

    let fo = true;
    let fr = true;

    for(const param of params){
        if (param === "otros[]" && fo ){
            let otros = searchParams.getAll("otros[]");
            otros.forEach(element => {
                url+=`&${param}=${element}`;
            });
            fo = !fo;
        }
        else if (param === "rest[]"  && fr){
            let rest = searchParams.getAll("rest[]");
            rest.forEach(element => {
                url+=`&${param}=${element}`;
            });
            fr = !fr;
        }else{
            if( param !== "otros[]" && param !== "rest[]" ){
                url+=`&${param}=${searchParams.get(param)}`;
            }
        }
    }
    window.location.href = url;
});

$(".clickToDeleteFilter").on("click", function(){
    let searchParams = new URLSearchParams(window.location.search);
    let url = "/propiedades/?";

    let name = $(this).attr("data-filtername");
    if(name === "otros[]" || name === "rest[]"){
        let val = $(this).attr("data-value");
        let or = searchParams.getAll(name);
        or = or.filter(item => item !== val)
        searchParams.delete(name);
        or.forEach(element => {
            url+=`&${name}=${element}`;
        });
    }

    searchParams.delete(name);
    let params = searchParams.keys();

    let fo = true;
    let fr = true;

    for(const param of params){
        if (param === "otros[]" && fo ){
            let otros = searchParams.getAll("otros[]");
            otros.forEach(element => {
                url+=`&${param}=${element}`;
            });
            fo = !fo;
        }
        else if (param === "rest[]"  && fr){
            let rest = searchParams.getAll("rest[]");
            rest.forEach(element => {
                url+=`&${param}=${element}`;
            });
            fr = !fr;
        }else{
            if( param !== "otros[]" && param !== "rest[]" ){
                url+=`&${param}=${searchParams.get(param)}`;
            }
        }
    }
    window.location.href = url;

});
