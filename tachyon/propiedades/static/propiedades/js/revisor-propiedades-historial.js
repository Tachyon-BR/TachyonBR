$(document).ready(function() {
    // Cuando se cierra el modal para confirmar el borrado de la usuario, reajusta la variable global a 0
    $('#historial-property-revisor').on('hidden.bs.modal', function () {
       id_prop_historial = 0;
       //$("#propiedad-rev-comentarios").val('');
       console.log("ID Propiedad Historial = 0")
    });
});


function historial_propiedad_revisor(id){
    console.log("VALIDANDO PROPIEDAD "+id);
    id_prop_historial = id;
    historial_property_request()
}

function historial_property_request(){
    if (id_prop_historial > 0){
        // Guardar variables globales en locales
        var id =  id_prop_historial;
        var token = csrftoken;

        $.ajax({
            url: "/propiedades/property-comment-history/",
            // Seleccionar información que se mandara al controlador
            data: {
                id:id,
                'csrfmiddlewaretoken': token
            },
            type: "GET",
            success: function(res){
                comms = res.info
                console.log("Consultando Historial de Propiedad # "+id);
                //id_prop_historial = 0;
                processComments(comms)
                
            },
        }); //end ajax call
        
    }
}

function processComments(comms){
    $('#historial-title').html("Historial de comentarios de la propiedad #"+id_prop_historial);
    let historial_modal_content = ""
    for (let c of comms){
        historial_modal_content += " <p>Revisor: "+ c.revisor+"</p>\
                                        <p>Fecha: " +c.fecha +"</p>\
                                        <p style='color:black'>"+c.comentario+"</p> <hr>"
    }
    $('#historial').html(historial_modal_content)
}
