


var xArray = [50,60,70,80,90,100,110,120,130,140,150];
  var yArray = [7,8,8,9,9,9,10,11,14,14,15];
  
  // Define Data
  var data = [{
    x: xArray,
    y: yArray,
    mode:"lines"
  }];
  
  // Define Layout
  var layout = {
    xaxis: {range: [40, 160], title: "Square Meters"},
    yaxis: {range: [5, 16], title: "Price in Millions"},  
    title: "House Prices vs. Size"
  };
  
  // Display using Plotly
  Plotly.newPlot("myPlot", data, layout);



  var xArray = ["Italy","France","Spain","USA","Argentina"];
var yArray = [55, 49, 44, 24, 15];

var data = [{
  x: xArray,
  y: yArray,
  type: "bar"  }];
var layout = {title:"World Wide Wine Production"};

Plotly.newPlot("myPlot1", data, layout);


