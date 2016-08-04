// when document is ready
$(() => {
  // import modules
  import {BackendAPI} from 'backendAPI.js';
  import {GoogleMap} from 'googleMap.js';
  import {InfoWindow} from 'infoWindow.js';
  import {Utils} from 'utils.js';
  import {UserInterface} from 'userInterface.js';

  // configuration
  const BACKEND_CONFIG = {
    base_url: 'http://qschools.online',
    school_locations_endpoint: '/school_locations/?format=json',
    school_info_endpoint: '/school/'
  };

  const MAP_CONFIG = {
    mapDivSel: "#map",
    mapOpts: {
      center: {
        lat: -27.4698,
        lng: 153.0251
      },
      zoom: 12
    }
  };

  const INFO_WINDOW_CONFIG = {
    infoDivSel: "#info",
    
  }
  
  // handle back-end comms through this object
  let backend = new BackendAPI(BACKEND_CONFIG);
  // handle local browser memory and cookie storage
  let storage = new Storage();
  // handle map functions with this object
  let map = new GoogleMap(MAP_CONFIG);
  // handle information shown in the info window
  let infoWindow = new InfoWindow(storage, INFO_WINDOW_CONFIG);

  const UI_SELS = {
    searchBar: '',
    watchlistButton: '',
    compareSchoolsButton: ''
  };
  // callbacks for User Interface
  let UI_CBS = {
    searchBarInput: (query) => {
      backend.handleSearch(query)
        .then((schools) => {
          map.removeAllMarkers();
          map.generateSchoolMarkers(schools, infoWindow.openInfoWindow);
        });
    },
    watchlistPress: () => { console.log('opened Watchlist'); },
    compareSchoolsPress: () => { console.log('opened school compare'); }
  }

  // user interface
  let ui = new UserInterface(UI_SELS, UI_CBS);
  
  // promise to get location data and load google map
  Promise
    .all([
      backend.getAllSchoolLocations(),
      map.loadGoogleMap()
    ])
    .then((data) => {
      let schools = data[0]; // result from first promise
      map.generateSchoolMarkers(schools);
    }).catch((err) => { console.log("Error: ", err); });
  
  function openInfoWindow(id) {
    $.getJSON(BASE_URL + '/school/' + id,
              (school) => {
      currentSchool = school;
      $("#info").removeClass("offscreen");
      console.log(school);
     
      school.name = Utils.nounify(school.name);
        
      $("#schoolName").text(school.name);

      if(school.naplan_set.length != 0){
        $("#schoolResultsLabel").text("NAPLAN results");
        let subjects = ["grammar", 'numeracy', 'reading', 'spelling', 'writing'];
        let napscores = [];
        for(let i in subjects){
          let napscore = {
            name: subjects[i].replace(/^([a-z])/, (l) => { return l.toUpperCase(); }),
            yr5: school.naplan_set[0]['year5_' + subjects[i] + 'mean'],
            yr9: school.naplan_set[0]['year9_' + subjects[i] + 'mean']
          };
          if(napscore.yr5 == 0){
            napscore.yr5 = 'N/A';
            $("#schoolType").text("High School");
          } 
          if(napscore.yr9 == 0){
            napscore.yr9 = 'N/A';
            $("#schoolType").text("Primary School");
          }
          napscores.push(napscore);
        }

        let $naplanTable = $("#schoolResultsTable");
        $naplanTable.html(""); // clear the table
        $naplanTable.append("\
        <thead><tr>\
          <td>Subject</td>\
          <td>Year 5 Result</td>\
          <td>Year 9 Result</td>\
        </tr></thead>")
        $tbody = $('<tbody></tbody>');
        for(let i in napscores){
          $row = $("<tr></tr>")
            .append("<td>" + napscores[i].name + "</td>")
            .append("<td>" + napscores[i].yr5 + '</td>')
            .append("<td>" + napscores[i].yr9 + '</td>')
          $tbody.append($row);
        }
        $naplanTable.append($tbody);

        console.log(savedSchools);

        if(savedSchools.indexOf(school) != -1){
          $("#saveSchoolButton").find('i').addClass('fa-check-square-o').removeClass('fa-square-o');
        } else {
          $("#saveSchoolButton").find('i').addClass('fa-square-o').removeClass('fa-check-square-o');
        }
      }

      // ATTENDANCES
      if(attendenceChart.clear){
        $('#attendenceChart').html('<canvas></canvas>'); // make new canvas
      }

      if(school.attendence_set.length > 0){
        let attendenceLabels = school.attendence_set.map((p) => {
          return '' + p.year;
        });
        let attendenceRates = school.attendence_set.map((p) => {
          return p.attendence_rate;
        });
        attendenceChart = new Chart($('#attendenceChart').find('canvas'), {
          type: 'bar',
          data: {
            labels: attendenceLabels,
            datasets: [{
              label: school.name + " Attendence Rates",
              data: attendenceRates,
              backgroundColor: '#4caf50'
            }]
          }
        });
      } else {
        $('#attendenceChart').text('No attendence data available');
      }

      $("#schoolLanguages").html('');
      school.secondlanguage_set.forEach(function(p) {
        $("#schoolLanguages").append("<li>" + p.second_language + "</li>")
      }, this);
    });
  }
});