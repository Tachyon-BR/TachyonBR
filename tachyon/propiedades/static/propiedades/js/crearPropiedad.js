var min = -1;
var max = -1;
var xtr = 0;
var f = [];

// A $( document ).ready() block.
$( document ).ready(function() {
  $('#id_portada').addClass('custom-file-input');
  $('#id_extra').addClass('custom-file-input');


  $('#id_portada').change(function() {
    img = document.getElementById('prtd');
    if($('#id_portada').prop('files').length >= 1){ //$('#id_portada').prop('files')[0];
      $('#prtd').prop('hidden', false);
      img.src = URL.createObjectURL(this.files[0]);
      img.onload = function() {
        URL.revokeObjectURL(this.src);
      }
    }
    else{
      $('#prtd').prop('hidden', true);
    }
    var len = $('#id_portada').get(0).files.length;
    if(len <= 0){
      $('#file-label-1').html('Selecciona tu archivo...');
    }
    else{
      $('#file-label-1').html($('#id_portada').get(0).files[0].name);
    }
  });
  $('#prtd').click(function() {
    $('#prtd').prop('hidden', true);
    $('#id_portada').val('');
    var len = $('#id_portada').get(0).files.length;
    if(len <= 0){
      $('#file-label-1').html('Selecciona tu archivo...');
    }
    else{
      $('#file-label-1').html($('#id_portada').get(0).files[0].name);
    }
  });


  $('#id_extra').change(function() {
    if($('#id_extra').prop('files').length >= 1){ //$('#id_portada').prop('files')[0];
      //$('#xtr').empty();
      //xtr = 0;
      var files = $('#id_extra').prop('files');
      var i;
      for(i = 0; i < files.length; i++){
        $('#xtr').append('<img id="xtr'+ xtr +'" alt="Extra'+ xtr +'" width="100" height="100" style="margin: 15px;" onclick="destroyImg(this.id);" />');
        img = document.getElementById('xtr'+xtr);
        xtr += 1;
        img.src = URL.createObjectURL(this.files[i]);
        img.onload = function() {
          URL.revokeObjectURL(this.src);
        }
        f.push(files[i]);
      }
    }
    else{
      //$('#xtr').empty();
      //xtr = 0;
    }
    var filtered = f.filter(function (el) {
      return el != null;
    });
    var len = filtered.length;
    if(len <= 0){
      $('#file-label-2').html('Selecciona tus archivos...');
    }
    else{
      $('#file-label-2').html(len +' archivos seleccionados');
    }
    if((parseInt(len) >= min) && (parseInt(len) <= max)){
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
  else{
    if(id === "codigo_postal"){
      if(val.length == 5){
        validar_cp();
      }
    }
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

function validar_cp(){
  var val = $('#codigo_postal').val();
  if(!(isNaN(val))){
    var temp;
    var bool = false;
    if(val[0] == "0"){
      temp = parseInt(val);
      temp = "0"+temp.toString();
      if(temp.length == 5){
        bool = true;
      }
    }
    else{
      temp = parseInt(val);
      if(temp.toString().length == 5){
        bool = true;
      }
    }
    if(bool){
      var token = csrftoken;
      $.ajax({
          url: "/propiedades/codigos/",
          dataType: 'json',
          // Seleccionar información que se mandara al controlador
          data: {
              'codigo': val,
              'csrfmiddlewaretoken': token
          },
          type: "POST",
          success: function (response) {
              // Obtener la info que se regresa del controlador
              $('#ubicacion').prop('hidden', false);
              $('#cp_safe').val('Qwerty')
              var data = JSON.parse(response.info);
              // Agregamos uno por uno los codigos seleccionados
              $('#colonia').empty();
              $('#colonia').append('<option disabled="disabled" value="" selected="selected">Seleccione una colonia...</option>');
              for (var i = 0; i < data.length; i++) {
                  var id = data[i].pk;
                  var estado = data[i].fields.estado;
                  var colonia = data[i].fields.asenta;
                  $('#estado').val(estado);
                  $('#colonia').append('<option>'+ colonia +'</option>');
              }
          },
          error: function (data) {
              showNotificationWarning('top', 'right', 'El código postal ingresado no existe.');
          }
      });
    }
    else{
      showNotificationWarning('top', 'right', 'El código postal ingresado no existe.');
    }
  }
  else{
    showNotificationWarning('top', 'right', 'El código postal ingresado no existe.');
  }
}

function cp_hidden(){
  $('#ubicacion').prop('hidden', true);
  $('#cp_safe').val('')
}

function val_video(val){
  var ban = val.includes("https://www.youtube.com/watch?v=");
  if(val == "" || ban){
    $("#safe_vid").val('Qwerty')
  }
  if(!ban && val != ""){
    $("#safe_vid").val('')
  }
}

function destroyImg(id){
  var val = id.slice(-1);
  $('#'+id).remove();
  f[val] = null;
  var filtered = f.filter(function (el) {
    return el != null;
  });
  var len = filtered.length;
  $('#file-label-2').html(len +' archivos seleccionados');
}
