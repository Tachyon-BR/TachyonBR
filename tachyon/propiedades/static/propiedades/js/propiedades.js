$(function () {
  $('.pop1').each(function() {
    $(this).popover({
        container: 'body',
        trigger: 'hover'
      })
  })
  $('.pop2').each(function() {
    $(this).popover({
        container: 'body',
        trigger: 'hover'
      })
  })
  $('.pop3').each(function() {
    $(this).popover({
        container: 'body',
        trigger: 'hover'
      })
  })
})


$( document ).ready(function() {
    $('.pagination').children().each(function() {
      $(this).click(function() {
        popovers();
      })
    })
});


function popovers(){
  $('.pop1').each(function() {
    $(this).popover({
        container: 'body',
        trigger: 'hover'
      })
  })
  $('.pop2').each(function() {
    $(this).popover({
        container: 'body',
        trigger: 'hover'
      })
  })
  $('.pop3').each(function() {
    $(this).popover({
        container: 'body',
        trigger: 'hover'
      })
  })
  $('.pagination').children().each(function() {
    $(this).click(function() {
      popovers();
    })
  })
}
