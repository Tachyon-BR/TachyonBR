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
                update_usuario_tabla(id);
                // borrar_usuario_tabla('.act-row',id);
                id_usuario = 0;
            },
        });

    }
 // Mostrar alerta de usuario borrada
}

function update_usuario_tabla(id){
  if ($('#row-'+id).find('#status').children().hasClass('badge-secondary')){
    if ($('#row-'+id).find('#icons').children().hasClass("danger")){
      $('#row-'+id).find('#icons').find(".danger").attr("data-target", "#restore-user");
      $('#row-'+id).find('#icons').children(".danger").removeClass("danger").addClass("success").html('<span class="fa-stack"><i class="fa fa-square fa-stack-2x"></i><i class="fas fa-trash-restore fa-stack-1x fa-inverse"></i></span>');
      showNotificationSuccess('top','right','Se ha eliminado el usuario exitosamente.');
    }
    else if ($('#row-'+id).find('#icons').children().hasClass("success")) {
      $('#row-'+id).find('#icons').find(".success").attr("data-target", "#delete-user");
      $('#row-'+id).find('#icons').children(".success").removeClass("success").addClass("danger").html('<span class="fa-stack"><i class="fa fa-square fa-stack-2x"></i><i class="fas fa-trash fa-stack-1x fa-inverse"></i></span>');
      showNotificationSuccess('top','right','Se ha restaurado el usuario exitosamente.');
    }
  }
  else if ($('#row-'+id).find('#status').children().hasClass('badge-success')){
    $('#row-'+id).find('#status').html('<span class="badge badge-pill badge-danger">Eliminado</span>');
    $('#row-'+id).find('#icons').find(".danger").attr("data-target", "#restore-user");
    $('#row-'+id).find('#icons').children(".danger").removeClass("danger").addClass("success").html('<span class="fa-stack"><i class="fa fa-square fa-stack-2x"></i><i class="fas fa-trash-restore fa-stack-1x fa-inverse"></i></span>');
    showNotificationSuccess('top','right','Se ha eliminado el usuario exitosamente.');
  }
  else if ($('#row-'+id).find('#status').children().hasClass('badge-danger')){
    $('#row-'+id).find('#status').html('<span class="badge badge-pill badge-success">Activo</span>');
    $('#row-'+id).find('#icons').find(".success").attr("data-target", "#delete-user");
    $('#row-'+id).find('#icons').children(".success").removeClass("success").addClass("danger").html('<span class="fa-stack"><i class="fa fa-square fa-stack-2x"></i><i class="fas fa-trash fa-stack-1x fa-inverse"></i></span>');
    showNotificationSuccess('top','right','Se ha restaurado el usuario exitosamente.');
  }
}
