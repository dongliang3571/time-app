$(document).ready(function() {

    $('#delete').on('click', function() {
        var resp = confirm('Are you sure you want to delete this employee?');
        if (resp == true) {
            return true;
        }
        else {
            return false;
        }
    });

    $('#delete-department').on('click', function() {
        var resp = confirm('Are you sure you want to delete this department?');
        if (resp == true) {
            return true;
        }
        else {
            return false;
        }
    });

    $('.logout').on('click', function() {
        var resp = confirm('Are you sure you want to log out this employee?');
        if (resp == true) {
            var time_now = new Date();
            var year = time_now.getFullYear();
            var month = time_now.getMonth() + 1;
            var day = time_now.getDate();
            var hour = time_now.getHours();
            var minute = time_now.getMinutes();
            var second = time_now.getSeconds();
            var string_time_now = year + '-' + month + '-' + day + ' ' +
                                  hour + ':' + minute + ':' + second;
            $('.time-now').attr('value', string_time_now);
            return true;
        }
        else {
            return false;
        }
    });

    $('#add-icon').on('click', function(event) {
        event.preventDefault();
        $(this).before('<div class="form-group"><input type="text" class="form-control" name="department"></div>');
    });

});
