/* Funciones que se ejecutan al cargar la página */
$(document).ready(function() {
    // Cuando se cierra el modal para confirmar el borrado de la usuario, reajusta la variable global a 0
    $('#modal_borrar_usuario').on('hidden.bs.modal', function () {
       id_usuario = 0;
    });
    // $('#modal_restaurar_usuario').on('hidden.bs.modal', function () {
    //    id_usuario = 0;
    // });
});

function borrar_usuario(id){
    if (id > 0){
        id_usuario = id;     // Carga el id de la cotización que se quiere borrar en la variable global
    }
}

function confirmar_borrar_usuario(){
    if (id_usuario > 0){
        // Guardar variables globales en locales
        var id =  id_usuario;
        var token = csrftoken;
        $.ajax({
            url: "/usuarios/deleteUser/"+id,
            // Seleccionar información que se mandara al controlador
            data: {
                id:id,
                'csrfmiddlewaretoken': token
            },
            type: "POST",
            success: function(){
                // update_usuario_tabla('.user-row',id);
                // borrar_usuario_tabla('.act-row',id);
                id_usuario = 0;
                $('#modal_borrar_usuario').modal('toggle');                                        // Cerrar el modal de borrar usuario
                showNotificationSuccess('top','right','Se ha borrado el usuario exitosamente.');
            },
        });

    }
 // Mostrar alerta de usuario borrada
}
