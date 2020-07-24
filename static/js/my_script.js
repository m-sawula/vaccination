$(document).ready(function () {
    $('#btn-1').on('click', function (event) {
        event.preventDefault();
        $('#div-1').hide();
    });


    $('#btn-2').on('click', function (event) {
        event.preventDefault();
        $('#div-1').show();
    });

    $('#btn-3').on('click', function (event) {
        event.preventDefault();
        $('#div-2').hide();
    });


    $('#btn-4').on('click', function (event) {
        event.preventDefault();
        $('#div-2').show();
    });

});
