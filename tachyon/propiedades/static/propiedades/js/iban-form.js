$("#amount_minus").click(function(event) {
    zoom("out");
});

$("#amount_plus").click(function(event) {
    zoom("in");
});

$("#amount").on('input change', function(event) {
    $('#amount_output').text($(event.currentTarget).val());
});

function zoom(direction) {
    var slider = $("#amount");
    var step = parseInt(slider.attr('step'), 10);
    var currentSliderValue = parseInt(slider.val(), 10);
    var newStepValue = currentSliderValue + step;

    if (direction === "out") {
        newStepValue = currentSliderValue - step;
    } else {
        newStepValue = currentSliderValue + step;
    }
    slider.val(newStepValue).change();
};
