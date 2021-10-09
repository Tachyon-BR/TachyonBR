    //Link handler
    $('.iban-link').click(function(){
        var token = csrftoken;
        $.ajax({
            url: "/propiedades/registerClickIbanOnline/",
            data: {
                'csrfmiddlewaretoken': token
            },
            type: "POST",
            success: function(msg){
                //console.log(msg);
            }
        });
    });

    //Amount handler
    $('.amount_minus').click(function(){
        var value = parseInt($('#amount').val());
       value = value === 100000 ? value : value -50000;
       $('#amount').val(value);
       $('#amount').trigger('change');
   });


   $('.amount_plus').click(function(){
        var value = parseInt($('#amount').val());
       value = value === 25000000 ? value : value +50000;
       $('#amount').val(value);
       $('#amount').trigger('change');
   });

   $('#amount').change(function(e){
       e.preventDefault();
       var current_value = parseInt($('#amount').val());
       //Format currency
       let dollarUSLocale = Intl.NumberFormat('en-US');
       current_value = dollarUSLocale.format(current_value);
       $('#HowDoYouNeedForLoanLabel').html("MXN $" + current_value); 
   })


   //Duration handler
   $('.duration_minus').click(function(){
       var value = parseInt($('#loanDurationInMonths').val());
       //console.log("0 " + value);
       value = value === 6 ? value : value -1;
       //console.log("01 " + value);
       $('#loanDurationInMonths').val(value);
       $('#loanDurationInMonths').trigger('change');
   });


   $('.duration_plus').click(function(){
        var value = parseInt($('#loanDurationInMonths').val());
       //console.log("1 " + value);
       value = value === 240 ? value : value +1;
       //console.log("2 " + value);
       $('#loanDurationInMonths').val(value);
       $('#loanDurationInMonths').trigger('change');
   });

   $('#loanDurationInMonths').change(function(e){
       e.preventDefault();
       var current_value = parseInt($('#loanDurationInMonths').val());
       //console.log("3 " + current_value);
       $('#ForWhatTimeLabel').html(current_value + " Meses"); 
       $('#duration_output').html(current_value + " Meses"); 
   })