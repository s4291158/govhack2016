export class GoogleMap {
  constructor(config) {
    this.mapDivID = config.mapDivID;
    this.mapOpts = config.mapOpts;
    this.mapObj = {};
    this.markers = [];
  }

  // promise to initialize the google map
  loadGoogleMap() {
    return new Promise((resolve, reject) => {
      let mapDiv = $('#' + this.mapDivID)[0];
      window.initMap = () => {
        this.mapObj = new google.maps.Map(mapDiv, this.mapOpts);
        resolve();
      }
    });
  }

  removeAllMarkers() {
    for(let marker of this.markers){
      marker.setMap(null);
    }
    this.markers = [];
  }

  // generate markers on the map from data recieved from the server
  generateSchoolMarkers(schools, clickHandler) {
    // use javascript closure in order to retain the information of the 
    // id in the click-event function declaration
    let generateClickListener = (marker, id) => {
      marker.addListener('click', (e) => {
        clickHandler(id);
      })
    };

    // loop through school data
    for(let school of schools){
      let marker = new google.maps.Marker({
        position: {
          lat: school.lat,
          lng: school.lng
        },
        map: this.mapObj,
        title: fixNameFormat(school.name)
      });
      generateClickListener(marker, school.id);
      this.markers.push(marker);
    }
  }
}
