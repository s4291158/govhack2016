document.onreadystatechange = () => {
  //let BASE_URL = 'https://qschools.online';
  let BASE_URL = 'http://45.32.247.22';
  
  let map;
  let markers = [];
  let savedSchools = [];
  let currentSchool = 0;
  
  let locationsRecieved = $.getJSON(BASE_URL + '/school_locations/?format=json');
  let mapInitialized = new Promise((resolve, reject) => {
    window.initMap = function() {
      let mapDiv = $('#map')[0];
      map = new google.maps.Map(mapDiv, {
        center: {lat: -27.4698, lng: 153.0251},
        zoom: 8
      });
      resolve();
    }
  });
  
  // promise to handle all setup
  Promise
    .all([locationsRecieved, mapInitialized])
    .then((data) => {
      let locations = data[0];
      console.log(data);
      for(let i in locations){
        let marker = new google.maps.Marker({
          position: {
            lat: locations[i].lat,
            lng: locations[i].lng
          },
          map: map,
          title: ("" + locations[i].id)
        });
        console.log(marker);
        markers.push(marker);
      }
    }).catch((err) => { console.log("Error: " + err); });
  
  // save for comparison button click handler
  $("#saveSchool").click((e) => {
    // if school already on list
    let indxOf = savedSchools.indexOf(currentSchool);
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
  
  
  
};