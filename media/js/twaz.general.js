$(document).ready(function() {
    $("a.geolocation").click(function(){
        navigator.geolocation.getCurrentPosition(
            function(position) {
                console.log(position);

            },
            function(error) {

            }
        );
    });
});
