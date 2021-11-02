/////////////////////////////////////////////////
// Plotly Line Graph
/////////////////////////////////////////////////

// Define a function that takes in a country_code, a dictionary structured
// like our response object, and an argument dictating whether to graph population
// or medals. Outputs x and y data for line graph plotting.

function xyData(countryCode, dictionary, yDataType) {

    // Define a variable for the data array for the specified country
    var country_data = dictionary[countryCode];

    // Define an x data array which holds the x-values (i.e., years) for the country's line graph
    var x = country_data.map(element => element.Year);

    // Define conditional to set the y data array based on the yDataType argument
    var y = country_data.map(element => element.Change in Temp (C)
    );
    
        
    

    // Return an array where the first element is the x-data and the second is the y-data. Each 
    // element is an array.
    return [x, y];
    console.log(xyData)
};

// Define a function that utilizes our response object from app.py AND the xyData() 
// function defined above to plot our line graph.
  
function lineGraph(country) {
    
    // Grab the json from that url and utilize it to build the line graph
    d3.json("/year_temp").then( function(response) {

        // Log the response to confirm it's in the same format I expect it to be in
        // console.log(response);
        
        // Define trace for the population line graph with AUT as the placeholder
        var temp_trace = {
            x: xyData(countryCode=country, dictionary=response, yDataType='Change in Temp (C)')[0],
            y: xyData(countryCode=country, dictionary=response, yDataType='Change in Temp (C)')[1],
            mode: 'line',
            name: 'Change in Temp (C)',
            line: {
                color: '#237BB8',
                width: 2
            }
        };
        
      

        // Define layout for the line graph
        var layout = {
            title:'Change in Temp over Time',
            yaxis: {
                tickformat: ',.2%'
            }
        };
        
        // Define the full trace for line graph
        var full_trace = [temp_trace];
        
        // Plot the line graph
        Plotly.newPlot('line', full_trace, layout);
    });
};
  
// Define a function that initializes the line graph on problem load, and provides
// users with the ability to toggle the country data that is shown.
  
function init() {

    // Grab a reference to the dropdown select element
    var selector = d3.select("#temp-line");
  
    // Use the list of sample names to populate the select options
    d3.json("/year_temp").then(function(response) {
      
      // Build a list of country codes from the keys of the response
      var countryCodes = Object.keys(response);
  
      // Loop through country codes and append each to the selector variable defined above
      countryCodes.forEach((countryCode) => {
        selector.append("option")
                .text(countryCode)
                .property("value", countryCode);
      });
  
      // Use the first country code from the list to build the initial line graph
      const firstCountry = countryCodes[1];
      lineGraph(firstCountry);
    });
};
  
// Define a function that fetches new data each time a new country is selected.
  
function optionChanged(newCountry) {
    lineGraph(newCountry);
};
  
// Call the init() function
init();