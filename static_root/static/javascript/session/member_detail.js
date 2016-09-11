$(document).ready(function() {
    var qr_string = $("#qrcode").attr("data");
    new QRCode($("#qrcode")[0], qr_string);

    $('button.print').click(function() {
        var prtContent = document.getElementById("qrcode");
        var WinPrint = window.open('', '', 'left=0,top=0,width=800,height=900,toolbar=0,scrollbars=0,status=0');
        WinPrint.document.write(prtContent.innerHTML);
        WinPrint.document.close();
        WinPrint.focus();
        WinPrint.print();
        WinPrint.close();
    });
});
