/* Funciones que se ejecutan al cargar la página */
$(document).ready(function() {
    // Cuando se cierra el modal para confirmar el borrado, reajusta la variable global a 0
    $('#delete-property-modal').on('hidden.bs.modal', function () {
       id_propiedad = 0;
    });

});

function borrar_propiedad(id){
    if (id > 0){
        id_propiedad = id;
    }
}

function confirmar_borrar_propiedad(){
  
    if (id_propiedad > 0){
        // Guardar variables globales en locales
        var id =  id_propiedad;
        var token = csrftoken;
        $.ajax({
            url: "/propiedades/deleteProperty/"+id,
            // Seleccionar información que se mandara al controlador
            data: {
                id:id,
                'csrfmiddlewaretoken': token
            },
            type: "POST",
            success: function(){
                remover_propiedad_de_lista(id);
                showNotificationSuccess('top','right','Se ha borrado la propiedad.');
                id_propiedad = 0;
            },
            error: function(data) { 
                showNotificationWarning('top','right', data.responseJSON.error);
            }  
        });

    }
  
        
 // Mostrar alerta de usuario borrada
}

function remover_propiedad_de_lista(id){
  $('#row-'+id).remove();
}
