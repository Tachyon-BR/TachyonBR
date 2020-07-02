
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
    /*
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
    });*/
    removeRevisorTable(id_prop)
}

function addRevisorTable(id){
    let html_revisor = `
        <img src="{% static 'root/images/user.png' %}" alt="Ícono de usuario"> 
        <a href="#" class="user-link">{{ user.nombre }} {{ user.apellido_paterno }} {{ user.apellido_materno }}</a> 
        <span class="user-subhead">{{ user.rol.nombre }}</span>
    `;
    $('#row-'+id).find('#revisor').html(html_revisor);
}

function removeRevisorTable(id){
    let html_revisor = "Ningún revisor asignado"
    $('#row-'+id).find('#revisor').html(html_revisor);
}