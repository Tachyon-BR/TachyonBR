function getRandomProperty(){
	$.ajax({
        url: '/root/randomProperty',
        dataType: 'json',
        success : function(response){
							var error = JSON.parse(response.error);
							if(!error){
								var data = JSON.parse(response.data[0]);
	              showProperty(data);
							}
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
	var i = 0;
	if(property[0].fields.habitaciones != null){
		if(property[0].fields.habitaciones.toString() != ""){
			$('#rp_habs').html(property[0].fields.habitaciones);
			i++;
		}
	}
	else{
		$('#rp_tipo1').remove();
	}
	if(property[0].fields.banos != null){
		if(property[0].fields.banos.toString() != ""){
			$('#rp_banos').html(property[0].fields.banos);
			i++;
		}
	}
	else{
		$('#rp_tipo2').remove();
	}
	if(property[0].fields.garaje != null){
		if(property[0].fields.garaje.toString() != ""){
			$('#rp_gar').html(property[0].fields.garaje);
			i++;
		}
	}
	else{
		$('#rp_tipo3').remove();
	}
	if(i < 3){
		$('#rp_metros').html(property[0].fields.metros_terreno);
	}
	else{
		$('#rp_tipo4').remove();
	}
  $('#random_property').prop('hidden', false);
}
