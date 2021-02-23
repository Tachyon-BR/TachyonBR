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

function checkPass(id){
  var val = $('#'+id).val();
  if(val.length > 5){
    if($('#new').val() === $('#new2').val()){
      $('.word').hide();
      $('.pass').show();
      $('#safe').val('Hello World!');
    }
    else{
      $('.pass').hide();
      $('.word').text("Las contraseñas no coinciden.");
      $('.word').show();
      $('#safe').val('');
    }
  }
  else{
    $('.pass').hide();
    $('#'+id).next().next().text("Por favor, ingrese su nueva contraseña.");
    $('.word').show();
    $('#safe').val('');
  }
}
