
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


function removeRevisorTable(id){
    let html_revisor = "Ningún revisor asignado"
    //$('#row-'+id).find('#revisor').html(html_revisor);
    $('#row-'+id).remove();
}

