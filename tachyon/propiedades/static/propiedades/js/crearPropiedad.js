var min = -1;
var max = -1;

// A $( document ).ready() block.
$( document ).ready(function() {
  $('#id_portada').addClass('custom-file-input');
  $('#id_extra').addClass('custom-file-input');
});

// Example starter JavaScript for disabling form submissions if there are invalid fields
(function() {
  'use strict';
  window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();

$('#tipo').change(function() {
  var val = $(this).val();
  $('#tipo_prop').html('Fotos de la Propiedad     ('+ val +')');
  if(val == "Terreno"){
    min = 5;
    max = 7;
    $('#opcional').prop('hidden', true);
    quitar_required();
  }
  else{
    if(val == "Casa"){
      min = 10;
      max = 20;
    }
    else if(val == "Departamento"){
      min = 10;
      max = 15;
    }
    else if(val == "Edificio"){
      min = 10;
      max = 20;
    }
    else if(val == "Local"){
      min = 5;
      max = 7;
    }
    $('#opcional').prop('hidden', false);
    forzar_required();
  }
  $('#fotos_prop').html('Mínimo '+ min +' <=> Máximo '+ max);
});

function forzar_required(){
  $('#habs').prop('required', true);
  $('#banos').prop('required', true);
  $('#pisos').prop('required', true);
  $('#garaje').prop('required', true);
}

function quitar_required(){
  $('#habs').prop('required', false);
  $('#banos').prop('required', false);
  $('#pisos').prop('required', false);
  $('#garaje').prop('required', false);
}

function numero(id, val){
  if(isNaN($('#'+id).val())){
    $('#'+id).val('');
    showNotificationWarning('bottom', 'center', 'Número inválido. Por favor, ingrese sólo números.');
  }
}

function positivo(id, val){
  if($('#'+id).val() < 0){
    $('#'+id).val(0);
  }
}

function decimal(id, val){
  if(!Number.isInteger($('#'+id).val())){
    $('#'+id).val(Math.floor(val));
  }
}

$('#id_portada').change(function(){
  var len = $('#id_portada').get(0).files.length;
  if(len <= 0){
    $('#file-label-1').html('Selecciona tu archivo...');
  }
  else{
    $('#file-label-1').html($('#id_portada').get(0).files[0].name);
  }
});

$('#id_extra').change(function(){
  var len = $('#id_extra').get(0).files.length;
  if(len <= 0){
    $('#file-label-2').html('Selecciona tus archivos...');
  }
  else{
    $('#file-label-2').html(len +' archivos seleccionados');
  }
  // for(i = 0; i < len; i++){
  //   if(i == 0){
  //     $('#file-label-2').html($('#id_extra').get(0).files[i].name);
  //   }
  //   else{
  //     $('#file-label-2').html($('#file-label-2').html()+ ", " + $('#id_extra').get(0).files[i].name);
  //   }
  // }
  if((parseInt($('#id_extra').get(0).files.length) >= min) && (parseInt($('#id_extra').get(0).files.length) <= max)){
    $('#id_extra').removeClass('is-invalid').addClass('is-valid')
    $('#id_extra').next().prop('hidden', false)
    $('#safe').val('Qwerty')
  }
  else{
    $('#id_extra').removeClass('is-valid').addClass('is-invalid')
    $('#id_extra').next().prop('hidden', true)
    $('#safe').val('')
  }
});

function validate_files(){
  if((parseInt($('#id_extra').get(0).files.length) >= min) && (parseInt($('#id_extra').get(0).files.length) <= max)){
    $('#id_extra').removeClass('is-invalid').addClass('is-valid')
    $('#id_extra').next().prop('hidden', false)
    $('#safe').val('Qwerty')
  }
  else{
    $('#id_extra').removeClass('is-valid').addClass('is-invalid')
    $('#id_extra').next().prop('hidden', true)
    $('#safe').val('')
  }
}
