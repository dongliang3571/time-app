$(document).ready(function() {
    $teamSelections = $('a.teams');
    $.each($teamSelections, function(index, team) {
        // console.log(team);
        team.click(function() {
            console.log('clicked');
        });
    });
});
