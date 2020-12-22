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
	if(property[0].fields.tipo != "Terreno"){
		$('#rp_banos').html(property[0].fields.banos);
		$('#rp_habs').html(property[0].fields.habitaciones);
		$('#rp_gar').html(property[0].fields.garaje);
	}
	else{
		$('#rp_metros').html(property[0].fields.metros_terreno);
		$('#rp_tipo1').prop('hidden', true);
		$('#rp_tipo2').prop('hidden', false);
	}
  $('#random_property').prop('hidden', false);
}
