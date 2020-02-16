
var correo_verificar = false;

var token = csrftoken;
$(document).ready(function () {
  $("#email").on("keyup",val_mail);
  $("#contrasena").on("keyup",val_passwords);
  $("#confirmar_contrasena").on("keyup",val_passwords);
});

function val_mail(e){   //Solo permite numeros en textbox
    $.ajax({
      url: '/usuarios/verificar_correo',
      type: 'POST',
      dataType: 'json',
      data: {
          'correo' : $('#email').val(),
          'csrfmiddlewaretoken': token
      },
      success : function (response) {
         if(response.num_mails>0){
             $("#submit").hide();
             if($('#email').val()!='') {

                 $(".invalid-mail").show();
                 correo_verificar = false;
             }
         }
         else{
             $("#submit").show();
             $(".invalid-mail").hide();
             correo_verificar = true;
         }
      }
    });
}

function val_passwords(e){
  if($("#contrasena").val()!=$("#confirmar_contrasena").val()){
      $("#submit").hide();
      $( ".invalid-password" ).show();
  }
  else{
      if(correo_verificar){
          $("#submit").hide();
      }
      $(".invalid-password").hide();
      $("#submit").show();
  }

  if ($("#contrasena").val().length < 6){
      $( ".invalid-password-len" ).show();
  }else {
      $( ".invalid-password-len" ).hide();
  }

}

// Funcion para ocultar los campos que no necesita en caso de crear un miembro que no sea propietario
$('#rol').change(function(){
    var role = $('#rol').val();
    if (role !== 'Propietario'){
        $('.ocultable').hide();
    }else{
        $('.ocultable').show();
    }
})
