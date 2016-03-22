var margin = {top: 30, right: 200, bottom: 70, left: 110},
        width = 1000 - margin.left - margin.right,
        height = 650 - margin.top - margin.bottom;


var x = d3.scale.linear()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .tickSize(-height);

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .tickSize(-width);




d3.csv("artist_cluster.csv", function(error, data){
	
    var svg = d3.select("#plot").append("svg")
    	.attr("width", width + margin.left + margin.right)
    	.attr("height", height + margin.top + margin.bottom)
  		.append("g")
    	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");


	var zoom = d3.behavior.zoom()
		.on("zoom",draw);

	svg.append("clipPath")
	    .attr("id", "clip")
	    .append("rect")
	    .attr("x", x(0))
	    .attr("y", y(1))
	    .attr("width", x(1) - x(0))
	    .attr("height", y(0) - y(1));

	svg.append("g")
		.attr("class","y axis")
		.append("text")
      	.classed("label", true)
      	.attr("transform", "rotate(-90)")
      	.attr("y", -margin.left + 30)
      	.attr("dy", ".71em")
      	.style("text-anchor", "end")
      	.style("font-size","20px")
      	.style("font-family","sans-serif")
      	.style("font-weight","bold")
      	.text("Hotness");

	svg.append("g")
		.attr("class","x axis")
		.attr("transform","translate(0," + height +")")
		.call(xAxis)
    	.append("text")
     	 .classed("label", true)
      	.attr("x", width)
      	.attr("y", margin.bottom - 20)
      	.style("text-anchor", "end")
      	.style("font-size","20px")
      	.style("font-family","sans-serif")
      	.style("font-weight","bold")
      	.text("Familiarity");


	svg.append("rect")
		.attr("class", "pane")
		.attr("width", width)
		.attr("height", height)
		.call(zoom);

	x.domain([0, 1]);
  	y.domain([0, 1]);
  	zoom.x(x);
  	zoom.y(y);
  	
  	draw();

  	svg.append("text")
            .attr("x", width + 25)  // space legend
            .attr("y", 15)
            .attr("class", "legend1")
            .style("fill", "#000000")
            .style("font-family", "sans-serif")
            .style("font-size","20px")
            .style("font-weight","bold")
            .text("Cluser 1");

    svg.append("text")
            .attr("x", width + 25)  // space legend
            .attr("y", 40)
            .attr("class", "legend2")
            .style("fill", "#ff0000")
            .style("font-family", "sans-serif")
            .style("font-size","16px")
            .text("Cluster 2");

    svg.append("text")
            .attr("x", width + 25)
            .attr("y",  65)  // space legend
            .attr("class", "legend3")
            .style("fill", "#0000ff")
            .style("font-family", "sans-serif")
            .style("font-size","20px")
            .style("font-weight","bold")
            .text("Cluster 3");

    svg.append("text")
            .attr("x", width + 25)
            .attr("y",  90)   // space legend
            .attr("class", "legend4")
            .style("fill", "#00ff00")
            .style("font-family", "sans-serif")
            .style("font-size","16px")
            .text("ENVIRONMENT");

    svg.append("text")
            .attr("x", width + 25)
            .attr("y",  115)  // space legend
            .attr("class", "legend5")
            .style("fill", "#ff00ff")
            .style("font-family", "sans-serif")
            .style("font-size","20px")
            .style("font-weight","bold")
            .text("FASHION");
    

	function draw() {
	  	svg.select("g.x.axis").call(xAxis);
	  	svg.select("g.y.axis").call(yAxis);

  }

});