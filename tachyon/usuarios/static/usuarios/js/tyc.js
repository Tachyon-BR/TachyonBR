function changeSend(){
  if($('#submit').prop('disabled')){
    $('#submit').prop('disabled', false);
  }
  else{
    $('#submit').prop('disabled', true);
  }
}

function checkTyC(){
  if(!$('#tyc').prop('checked')){
    showNotificationInfo('top','right','Debe aceptar los términos y condiciones para continuar.');
  }
}
