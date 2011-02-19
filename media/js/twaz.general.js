$(document).ready(function() {
  $(".geolocator").click(function(e){
    navigator.geolocation.getCurrentPosition(
      function(position) {
        $(e.currentTarget.form).children('#id_lat')[0].value = position.coords.latitude;
        $(e.currentTarget.form).children('#id_lon')[0].value = position.coords.longitude;
        $(e.currentTarget.form).submit();
      },
      function(error) {
      }
    );
  });
});
