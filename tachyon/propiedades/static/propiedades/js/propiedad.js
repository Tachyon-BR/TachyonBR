// A $( document ).ready() block.
$( document ).ready(function() {
  var str = $('#price').html().trim();
  str = formatter.format(str); /* $2,500.00 */
  $('#price').html(str.slice(0, str.length-3));
});

var formatter = new Intl.NumberFormat('es-MX', {
  style: 'currency',
  currency: 'MXN',
});
