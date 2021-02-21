/* Funciones que se ejecutan al cargar la página */
$(document).ready(function() {
    id_usuario = 0;
    $('#enviar').click(function() {
      $('#form').submit();
    });
});

function mostrar_rol(){
  $('#edit').prop('hidden', true);
  $('#accept').prop('hidden', false);
  $('#cancel').prop('hidden', false);
  $('#rol_name').prop('hidden', true);
  $('#rol_div').prop('hidden', false);
}

function esconder_rol(){
  $('#edit').prop('hidden', false);
  $('#accept').prop('hidden', true);
  $('#cancel').prop('hidden', true);
  $('#rol_name').prop('hidden', false);
  $('#rol_div').prop('hidden', true);
}
