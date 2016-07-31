$(() => {
  let BASE_URL = 'http://qschools.online';
  
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
  
  function generateMarkers(data) {
    for(let i in data){
      let marker = new google.maps.Marker({
        position: {
          lat: data[i].lat,
          lng: data[i].lng
        },
        map: map,
        title: ("" + data[i].name)
      });
      marker.addListener('click', (e) => {
        openInfoWindow(data[i].id);
      })
      markers.push(marker);
    }
  }
  
  // promise to handle all setup
  Promise
    .all([locationsRecieved, mapInitialized])
    .then((data) => {
      generateMarkers(data[0]);
    }).catch((err) => { console.log("Error: ", err); });
  
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
      $(e.currentTarget).find('i').addClass('fa-square-o').removeClass('fa-check-square-o');

      // update data
      savedSchools.push(currentSchool);
    }
  });
  
  $("#info").click((e) => {
    $("#info").toggleClass("offscreen");
  });
  
  function clearAllMarkers() {
    for(let i in markers){
      markers[i].setMap(null);
    }
    markers = [];
  }
  
  function handleSearch() {
    let query = $("#srch-term").val();
    console.log(query);
    $.post(BASE_URL, {"query": query}, (data) => {
      console.log(data);
      clearAllMarkers();
      generateMarkers(data);
    });
  };
  
  $("#srch-term").keyup((e) => {
    if(e.keyCode == 13)
      handleSearch;
  });
  $("#searchButton").click(handleSearch);
  
  function openInfoWindow(id) {
    $.getJSON(BASE_URL + '/school/' + id,
              (school) => {
      currentSchool = school;
      $("#info").removeClass("offscreen");
      console.log(school);
     
      school.name = school.name
        .split('_').join(' ')
        .replace(/( ([a-z]))|(^[a-z])/g, (l) => {
          return l.toUpperCase();
        });
        
      $("#schoolName").text(school.name);

      if(school.naplan_set.length == 1){
        $("#schoolResultsLabel").text("NAPLAN results");
        let subjects = ["grammar", 'numeracy', 'reading', 'spelling', 'writing'];
        let napscores = [];
        for(let i in subjects){
          napscores.push({
            name: subjects[i].replace(/^([a-z])/, (l) => { return l.toUpperCase(); }),
            yr5: school.naplan_set[0]['year5_' + subjects[i] + 'mean'],
            yr9: school.naplan_set[0]['year9_' + subjects[i] + 'mean']
          })
        }

        let $naplanTable = $("#schoolResultsTable");
        $naplanTable.append("\
        <thead><tr>\
          <td>Subject</td>\
          <td>Year 5 Score</td>\
          <td>Year 9 Score</td>\
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
      }
    })
  }
});