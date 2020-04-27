// A $( document ).ready() block.
$( document ).ready(function() {

});

var formatter = new Intl.NumberFormat('es-MX', {
  style: 'currency',
  currency: 'MXN',
});

function precios(){
  $('.precios').each(function() {
    var str = $(this).html().trim();
    str = formatter.format(str); /* $2,500.00 */
    $(this).html(str.slice(0, str.length-3));
  });
}
