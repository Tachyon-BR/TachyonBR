/* Funciones que se ejecutan al cargar la página */
$(document).ready(function() {
    // Cuando se cierra el modal para confirmar el borrado de la usuario, reajusta la variable global a 0
    $('#validate-property-revisor').on('hidden.bs.modal', function () {
       id_propiedad = 0;
       $("#propiedad-rev-comentarios").val('');
       console.log("ID Propiedad = 0")
    });
});

function validar_propiedad_revisor(id){
    console.log("VALIDANDO PROPIEDAD "+id);
    id_propiedad = id;
}

function validar_propiedad_revisor_send(decision){
    if (id_propiedad > 0){
        // Guardar variables globales en locales
        var id =  id_propiedad;
        var token = csrftoken;
        var coms = $("#propiedad-rev-comentarios").val();
    
        $.ajax({
            url: "/propiedades/validateAsRevisor/",
            // Seleccionar información que se mandara al controlador
            data: {
                id_prop:id,
                coms:coms,
                aor:decision,
                'csrfmiddlewaretoken': token
            },
            type: "POST",
            success: function(){
                if(decision == "aceptada"){
                    update_propiedad_revision_tabla(id, "publicada");
                }
                else if(decision == "rechazada"){
                    update_propiedad_revision_tabla(id, "no publicada");
                }
                showNotificationSuccess('top','right','La propiedad ha sido '+decision+" con éxito.");
                console.log("Validada propiedad "+id+" "+decision);
                id_propiedad = 0;
                $('#validate-property-revisor').modal('hide');
                $('.fade').remove();
                $('body').removeClass('modal-open');

                //redirect
                location.href = "/propiedades/mis-revisiones/";

            },
        }); //end ajax call
        
    }
}

function update_propiedad_revision_tabla(id, decision){
    if(decision=="publicada"){
        $('#row-'+id).find('#status').html('<span class="badge badge-pill badge-success">Publicada</span>');
    }
    if(decision=="no publicada"){
        $('#row-'+id).find('#status').html('<span class="badge badge-pill badge-danger">No Publicada</span>');
    }
    $('#row-'+id).find('#icons').find("#validar").remove();
}

