

function asignarseComoRevisor(id_prop){
    var token = csrftoken;
    $.ajax({
        url: "/propiedades/addRevisor/",
        // Seleccionar información que se mandara al controlador
        data: {
            id_prop:id_prop,
            'csrfmiddlewaretoken': token
        },
        type: "POST",
        success: function(){
            addRevisorTable(id_prop);
            showNotificationSuccess('top','right','Has sido agregado como revisor exitosamente.');
        },
        error: function(){

        }
    });
}

function quitarseComoRevisor(id_prop){
    var token = csrftoken;
    
    $.ajax({
        url: "/propiedades/removeRevisor/",
        // Seleccionar información que se mandara al controlador
        data: {
            id_prop:id_prop,
            'csrfmiddlewaretoken': token
        },
        type: "POST",
        success: function(){
            removeRevisorTable(id_prop)
            showNotificationSuccess('top','right','Has sido removido como revisor exitosamente.');
        },
        error: function(){

        }
    });
    
}

function addRevisorTable(id){
    let html_revisor = `
        <img src="${user_img_src}" alt="Ícono de usuario">
        <a href="#" class="user-link">${user_nombre_completo}</a> 
        <span class="user-subhead">${user_rol_nombre}</span>
    `;
    $('#row-'+id).find('#revisor').html(html_revisor);

    //agregar ícono de quitarse, como el revisor es el user loggeado
    var html_icons = `
    <!-- El revisor de la propiedad es el usuario logeado -->
    <a href="#" class="table-link danger" onclick="quitarseComoRevisor(${id})" >
        <span class="fa-stack">
        <i class="fa fa-square fa-stack-2x"></i>
        <i class="fas fa-minus fa-stack-1x fa-inverse"></i>
        </span>
    </a>
    `
    $('#row-'+id).find('#icons').html(html_icons);
}



function removeRevisorTable(id){
    let html_revisor = "Ningún revisor asignado"
    $('#row-'+id).find('#revisor').html(html_revisor);

    //agregar ícono de agregarse, como la propiedad ya no tiene revisor
    var html_icons = `
    <!-- La propiedad no tiene revisor asignado -->
    <a href="#" class="table-link success" onclick="asignarseComoRevisor(${id})" >
      <span class="fa-stack">
        <i class="fa fa-square fa-stack-2x"></i>
        <i class="fas fa-plus fa-stack-1x fa-inverse"></i>
      </span>
    </a>
    `
    $('#row-'+id).find('#icons').html(html_icons);
}

