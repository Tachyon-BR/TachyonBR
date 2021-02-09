/* Funciones que se ejecutan al cargar la página */
$(document).ready(function() {
    // Cuando se cierra el modal para confirmar el borrado de la usuario, reajusta la variable global a 0
    $('#modal_validar_propiedad').on('hidden.bs.modal', function () {
       id_propiedad = 0;
    });
    // $('#modal_restaurar_usuario').on('hidden.bs.modal', function () {
    //    id_propiedad = 0;
    // });
});

function validar_propiedad(id){
    if (id > 0){
        id_propiedad = id;     // Carga el id de la cotización que se quiere borrar en la variable global
    }
}

function confirmar_validar_propiedad(){
    if (id_propiedad > 0){
        // Guardar variables globales en locales
        var id =  id_propiedad;
        var token = csrftoken;
        $.ajax({
            url: "/propiedades/validateProperty/"+id,
            // Seleccionar información que se mandara al controlador
            data: {
                id:id,
                'csrfmiddlewaretoken': token
            },
            type: "POST",
            success: function(){
                update_propiedad_tabla(id);
                showNotificationSuccess('top','right','Se ha mandado la solicitud de revisión.');
                id_propiedad = 0;
            },
        });

    }
 // Mostrar alerta de usuario borrada
}

function update_propiedad_tabla(id){
  $('#row-'+id).find('#status').html('<span class="badge badge-pill badge-info">En Revisión</span>');
  //$('#row-'+id).find('#icons').children().eq(0).remove();
  $('#row-'+id).find('#icons').children().remove();
  $('#row-'+id).find('#icons').append("Sin Acciones");
}


function despublicar_propiedad(id){
    if (id > 0){
        id_propiedad = id;     // Carga el id de la cotización que se quiere borrar en la variable global
    }
}



function confirmar_despublicar_propiedad(id){
    if (id_propiedad > 0){
        // Guardar variables globales en locales
        var id =  id_propiedad;
        var token = csrftoken;
        $.ajax({
            url: "/propiedades/unpublishProperty/",
            // Seleccionar información que se mandara al controlador
            data: {
                id:id,
                'csrfmiddlewaretoken': token
            },
            type: "POST",
            success: function(){
                //update_propiedad_tabla(id);
                showNotificationSuccess('top','right','Se ha despublicado la propiedad con éxito.');
                id_propiedad = 0;
            },
        });

    }
 // Mostrar alerta de usuario borrada

}