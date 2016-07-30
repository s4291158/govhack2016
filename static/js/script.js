document.onreadystatechange = () => {
  var BASE_URL = 'http://qschools.online';
  
  var map;
  var markers = [];
  var savedSchools = [];
  var currentSchool = 0;
  
  var locationsRecieved = $.getJSON(BASE_URL + '/school_locations/?format=json');
  var mapInitialized = new Promise((resolve, reject) => {
    window.initMap = function() {
      var mapDiv = $('#map')[0];
      map = new google.maps.Map(mapDiv, {
        center: {lat: -27.4698, lng: 153.0251},
        zoom: 8
      });
      resolve();
    }
  });

  function openInfoWindow(id) {
    console.log('ID: ', id);
    $('#info').removeClass('closed');

    $.post(BASE_URL + '/school', (school) => {
      currentSchool = school;
      console.log(school);
    });
  }

  function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
      markers[i].setMap(map);
    }
  }

  function deleteAllMarkers(){
    setMapOnAll(null);
    markers = [];
  }

  generateMarkers = (data) => {
    for(var i in data){
        locations = data;
        marker = new google.maps.Marker({
          position: {
            lat: locations[i].lat,
            lng: locations[i].lng
          },
          map: map,
          title: ("" + locations[i].name)
        });
        marker.addListener('click', (e) => {
            console.log('ID: ', locations[i].id);
            openInfoWindow(locations[i].id);
        });
    markers.push(marker);
  }};
  
  // promise to handle all setup
  Promise
    .all([locationsRecieved, mapInitialized])
    .then((data) => {
        var locations = data[0];
        generateMarkers(locations);
    }).catch((err) => { console.log("Error: " + err); });
  
  // save for comparison button click handler
  $("#saveSchool").click((e) => {
    // if school already on list
    var indxOf = savedSchools.indexOf(currentSchool);
    if(indxOf != -1){
      // remove it
      savedSchools.splice(indxOf, 1);
      
      // update graphics
      $(e.currentTarget).find('i').addClass('fa-check-square-o').removeClass('fa-square-o');
    } else {
      // update graphics
      $(e.currentTarget).find('i').addClass('fa-check-o').removeClass('fa-check-square-o');

      // update data
      savedSchools.push(currentSchool);
    }
  });

  // on query search
  $("#searchButton").click((e) => {
    queryText = $('#query').text();
    deleteAllMarkers();
    $.post('/', {"query": queryText}, (response) => {
        var locations = data[0];
        try{
            generateMarkers(locations);
        }catch(err){
        console.log(err);
        }
    })
  });
};
