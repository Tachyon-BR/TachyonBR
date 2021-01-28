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

function esconder_titulo(){
  $('#title').prop('hidden', true);
  $('#titulo').prop('required', true);
  $('#titulo').prop('hidden', false);
  $('#edit1').prop('hidden', true);
  $('#cancelar1').prop('hidden', false);
}

function mostrar_titulo(){
  $('#title').prop('hidden', false);
  $('#titulo').prop('required', false);
  $('#titulo').prop('hidden', true);
  $('#edit1').prop('hidden', false);
  $('#cancelar1').prop('hidden', true);
  $('#titulo').val(titulo);
}

function esconder_dif(){
  $('#dif').prop('hidden', true);
  $('#difer').prop('required', true);
  $('#difer').prop('hidden', false);
  $('#edit2').prop('hidden', true);
  $('#cancelar2').prop('hidden', false);
}

function mostrar_dif(){
  $('#dif').prop('hidden', false);
  $('#difer').prop('required', false);
  $('#difer').prop('hidden', true);
  $('#edit2').prop('hidden', false);
  $('#cancelar2').prop('hidden', true);
  $('#difer').val(diferenciador);
}

function esconder_desc(){
  $('#des').prop('hidden', true);
  $('#desc').prop('required', true);
  $('#desc').prop('hidden', false);
  $('#edit3').prop('hidden', true);
  $('#cancelar3').prop('hidden', false);
}

function mostrar_desc(){
  $('#des').prop('hidden', false);
  $('#desc').prop('required', false);
  $('#desc').prop('hidden', true);
  $('#edit3').prop('hidden', false);
  $('#cancelar3').prop('hidden', true);
  $('#desc').val(descripcion);
}
