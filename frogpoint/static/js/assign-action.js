$(function () {
    $('input:checkbox, input:radio').uniform();

    // $('select').select2();

    $('.input-datepicker').datetimepicker({
        format: 'YYYY-MM-DD H:mm',
    });

    $('select[name="type"]').on('change', function (event) {
        var type = $(this).val();
        $('.coupon-type').addClass('hidden');
        $('[data-type="' + type + '"]').removeClass('hidden');
    });
});
