//EUTROPHIC MAP USING LEAFLET
// Create the tile layer that will be the background of our map
function createMap(classifcationStatus) {

    // Create the tile layer that will be the background of our map
    var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
      maxZoom: 18,
      id: "light-v10",
      accessToken: API_KEY
    });
  
    // Create a baseMaps object to hold the lightmap layer
    var baseMaps = {
      "Light Map": lightmap
    };
  
    // Create an overlayMaps object to hold the classification layer
    var overlayMaps = {
      "Classification": classificationStat
    };
  
    // Create the map object with options
    var map = L.map("map-id", {
      center: [40.73, -74.0059],
      zoom: 12,
      layers: [lightmap, classificationStat]
    });
  
    // Create a layer control, pass in the baseMaps and overlayMaps. Add the layer control to the map
    L.control.layers(baseMaps, overlayMaps, {
      collapsed: false
    }).addTo(map);
  }
  
  function createMarkers(response) {
  
    // Pull the "classificaiton" property off of response
    var classification = response;
  
    // Initialize an array to classification markers
    var classificationMarkers = [];
  
    // Loop through the classification array
    for (var index = 0; index < classification.length; index++) {
      var classificationStatus = classification[index];
  
      // For each classification, create a marker and bind a popup with the station's name
      var classificationMarker = L.marker([classificationStatus.Lat, classificationStatus.Long])
        .bindPopup("<h3>" + classificationStatus.classifcation + "<h3><h3>Country: " + classificationStatus.Country + "</h3>");
  
      // Add the marker to the bikeMarkers array
      classificationMarkers.push(classificationMarker);
    }
  
    // Create a layer group made from the bike markers array, pass it into the createMap function
    createMap(L.layerGroup(classificationMarkers));
  }
  
  
  // Perform an API call to the REgions API to get classification information. Call createMarkers when complete
  d3.json("/regions").then(createMarkers);