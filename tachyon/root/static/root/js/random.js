function getRandomProperty(){
	$.ajax({
        url: '/root/randomProperty',
        dataType: 'json',
        success : function(response){
              var data = JSON.parse(response.data[0]);
              showProperty(data);
        }
    });
}

function showProperty(property){
  $('#rp_image_link').attr('href', "/propiedades/property/" + property[0].pk);
  $('#rp_image').attr('src', "/media/" + property[0].fields.portada);
  $('#rp_tipo').html(property[0].fields.tipo);
  $('#rp_oferta').html(property[0].fields.oferta);
  $('#rp_tipo').attr('href', "/propiedades/property/" + property[0].pk);
  $('#rp_oferta').attr('href', "/propiedades/property/" + property[0].pk);
  $('#rp_price').html(property[0].fields.precio);
  $('#rp_address').html("" + property[0].fields.direccion + ", " + property[0].fields.estado + ", " + property[0].fields.codigo_postal);
  $('#rp_address').attr('href', "/propiedades/property/" + property[0].pk);
  $('#random_property').prop('hidden', false);
}
