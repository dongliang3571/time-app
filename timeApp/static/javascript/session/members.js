$(document).ready(function() {
    $('#delete').on('click', function() {
        var resp = confirm('Are you sure you want to delete this user?');
        if (resp == true) {
            return true;
        }
        else {
            return false;
        }
    });
});
