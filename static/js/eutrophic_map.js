//EUTROPHIC MAP USING LEAFLET
// Create the tile layer that will be the background of our map
function createMap(classificationStatus) {

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
      "Classification": classificationStatus
    };
  
    // Initialize the layerGroups
    var layers = {
      Improved: new L.LayerGroup(),
      Eutrophic: new L.LayerGroup(),
      Hypoxic: new L.LayerGroup()
      
    };
    
    
    // Create the map object with layers
    var map = L.map("map-id", {
      center: [40.73, -74.0059],
      zoom: 4,
      layers: [
        layers.Improved,
        layers.Eutrophic,
        layers.Hypoxic
        ]
    });

    // Add our 'lightmap' tile layer to the map
    lightmap.addTo(map);

    // Create an overlays object to add to the layer control
    var overlays = {
      "Improved": layers.Improved,
      "Eutrophic": layers.Eutrophic,
      "Hypoxic": layers.Hypoxic,
    
    };


  
    // Create a layer control, pass in the baseMaps and overlayMaps. Add the layer control to the map
    L.control.layers(baseMaps, overlayMaps, {
      collapsed: false
    }).addTo(map);

    // Create a legend to display information about our map
    var info = L.control({
     position: "topright"
    });

    // When the layer control is added, insert a div with the class of "legend"
    info.onAdd = function() {
      var div = L.DomUtil.create("div", "legend");
      return div;
    };
    // Add the info legend to the map
    info.addTo(map);
     }

    // Initialize an object containing icons for each layer group
    /*
    var icons = {
      Improved: L.ExtraMarkers.icon({
        //icon: "ion-settings",
        iconColor: "white",
        markerColor: "yellow",
        shape: "circle"
      }),
      Eutrophic: L.ExtraMarkers.icon({
       // icon: "ion-android-bicycle",
        iconColor: "white",
        markerColor: "blue",
        shape: "circle"
      }),
      Hypoxic: L.ExtraMarkers.icon({
        //icon: "ion-minus-circled",
        iconColor: "white",
        markerColor: "red",
        shape: "circle"
      })
  
    };
    */
  
  function createMarkers(response) {
  
    // Pull the "classificaiton" property off of response
    var classification = response;
  
    // Initialize an array to classification markers
    var classificationMarkers = [];
  
    // Loop through the classification array
    for (var index = 0; index < classification.length; index++) {
      var classificationStatus = classification[index];
      console.log(classificationStatus)
      
      var color = "yellow";

      if(classificationStatus.Classification == "Improved")
        color = "blue";
        else if(classificationStatus.Classification == "Hypoxic")
            color = "red"
      // For each classification, create a marker and bind a popup 
      var classificationMarker = L.circle([classificationStatus.Lat, classificationStatus.Long], 
        {
            color: color, 
            fillColor: color,
            radius : 50
        })
        .bindPopup("<h3>" + classificationStatus.classifcation + "<h3><h3>Country: " + classificationStatus.Country + "</h3>");
  
      // Add the marker to the classificationMarkers array
      classificationMarkers.push(classificationMarker);
    }
  
    // Create a layer group made from the classification markers array, pass it into the createMap function
    createMap(L.layerGroup(classificationMarkers));
  }
  
  
  // Perform an API call to the Regions API to get classification information. Call createMarkers when complete
  d3.json("/regions").then(createMarkers);