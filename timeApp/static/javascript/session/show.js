$(document).ready(function() {
    var qr_string = $("#qrcode").attr("data");
    new QRCode($("#qrcode")[0], qr_string);
})
