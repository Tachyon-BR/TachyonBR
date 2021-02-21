/* Funciones que se ejecutan al cargar la página */
$(document).ready(function() {
    // Cuando se cierra el modal para confirmar el borrado, reajusta la variable global a 0
    $('#edit-property-modal').on('hidden.bs.modal', function () {
       id_propiedad = 0;
    });

});

function editar_propiedad(id){
    if (id > 0){
        id_propiedad = id;
    }
}

function confirmar_editar_propiedad(){

    if (id_propiedad > 0){

      window.location.href = "/propiedades/editProperty/"+ id_propiedad;

    }


 // Mostrar alerta de usuario borrada
}
