function changeSend(){
  if($('#submit').prop('disabled')){
    $('#submit').prop('disabled', false);
  }
  else{
    $('#submit').prop('disabled', true);
  }
}
