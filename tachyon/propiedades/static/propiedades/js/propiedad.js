$(function () {
  $('#pop1').popover({
    container: 'body',
    trigger: 'hover'
  })
})

function copy_link(){
  /* Get the text field */
  var copyText = document.getElementById("enlace");

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

  /* Copy the text inside the text field */
  document.execCommand("copy");

  /* Alert the copied text */
  $('#pop1').popover('show');
  var pop = $('#pop1').data('bs.popover').tip;
  $(pop).find('.popover-body').html("¡Copiado!");
  $('#pop1').data('bs.popover').update();
}

function show_tip(){
  $('#pop1').popover('hide');
}
