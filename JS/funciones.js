//Validacion del formulario
function validaForm(){
	//Errores
	errores = '';
	//Campos formulario
	var nombre = $("#nombre").val();
	var file = $("#file").val();
	var divErrores = $("#errores");
	//Nombre no puede estar vacío
	if (nombre == ""){
		errores = errores + 'Nombre del Pol\u00edgono est\u00e1 vac\u00edo.<br>';
	}
	//Comprobar la extensión
	if (file == ''){
		errores = errores + 'No se ha seleccionado ning\u00fan archivo.<br>';	
	}else{
		extensiones = new Array(".txt"); 
		extension = (file.substring(file.lastIndexOf("."))).toLowerCase();
		permitida = false;
	    for (var i = 0; i < extensiones.length; i++) {
	        if (extensiones[i] == extension) { 
	        permitida = true; 
	        break;   
	   		}
	   	}
	   if (permitida == false){
	   	errores = errores + "Extensi\u00f3n de archivo err\u00f3nea. Extensiones soportadas: "+extensiones+"<br>";
	   }
	}
	if(errores == ''){
		divErrores.html('');
		$("div.espera").show();
		return true;
	}else{
		divErrores.html(errores);
		return false;
	}
}
 

function aparecenAreas(){
    		var displayAr = $("polygon.ar").css("display");
    		if (displayAr == "none"){
    			$("polygon.ar").fadeIn('slow', function(){
    				$("polygon.ar").css("display","block");
    				$("polygon.inter").css("display","block");
    				$("p.mejorada").css("display","block");
    				$("hr.mejorada").css("display","block");
    			});
    		}else{
    			$("polygon.ar").fadeOut('slow', function(){
    				$("polygon.ar").css("display","none");
    				$("polygon.inter").css("display","none");
    				$("p.mejorada").css("display","none");
    				$("hr.mejorada").css("display","none");
    			});
    		}
    	}	

function exportarPNG(){
  var html = d3.select("svg")
        .attr("version", 1.1)
        .attr("xmlns", "http://www.w3.org/2000/svg")
        .node().parentNode.innerHTML;
 
  //console.log(html);
  var imgsrc = 'data:image/svg+xml;base64,'+ btoa(html);
 
  var canvas = document.querySelector("canvas"),
	  context = canvas.getContext("2d");
 
  var image = new Image;
  image.src = imgsrc;
  image.onload = function() {
	  context.drawImage(image,10,10,550,550);
 
	  var canvasdata = canvas.toDataURL("image/png");
 
	  var a = document.createElement("a");
	  a.download = $("#name").text()+".png";
	  a.href = canvasdata;
	  a.click();
  };
}

function exportPDF(){
	var doc = new jsPDF();
	doc.text(15, 20 , 'Posicionamiento topogr\xE1fico - 2014');
	doc.fromHTML($('#inf').get(0), 12, 30, {
        'width': 90
    });
    doc.fromHTML($('#infarea').get(0), 104, 30, {
        'width': 80
    });
  
	doc.save($("#name").text()+'.pdf');
}

//Al cargar.
$(document).ready(function()
    {	//Botones Info y Faqs.
    	$("div.espera").hide();
    	$("#botonFunciona").click(function () {
    		displayingFaqs = $("#faqs").css("display");
    		displayingInfo = $("#informacion").css("display");
    		if (displayingFaqs == "none"){
    			$("#faqs").slideDown();
    			$("#faqs").fadeIn('slow',function() {
    				$("#faqs").css("display","block");
    			});
    			$("#informacion").css("display","none");
    		}else{
    			$("#faqs").fadeOut('slow',function() {
    				$("#faqs").css("display","none");
    			});
    		}
    	});
    	$("#info").click(function () {
    		displayingFaqs = $("#faqs").css("display");
    		displayingInfo = $("#informacion").css("display");
    		if (displayingInfo == "none"){
    			$("#informacion").slideDown();
    			$("#informacion").fadeIn('slow',function() {
    				$("#informacion").css("display","block");
    			});
    			$("#faqs").css("display","none");
    		}else{
    			$("#informacion").fadeOut('slow',function() {
    				$("#informacion").css("display","none");
    			});
    		}
    	});
    	
    	//Boton volver.
    	$('#atras').click(function(){
    		var r = confirm("¿Seguro que quieres volver?");
			if (r == true)
  			{
 				window.location = "http://localhost:8888";
    			return false;
  			}
		});
		
		//Dibuja Polígono con D3
		
		//Datos del servidor
        var poly = jQuery.parseJSON(pol);
        var escalaJSON = jQuery.parseJSON(escala);
        var areasJSON = jQuery.parseJSON(visioness);
        var interJSON = jQuery.parseJSON(interss);
           
        var width = 500;
		var height = 500;
		
		var xmin = escalaJSON[0];
		var xmax = escalaJSON[1];
		var ymin = escalaJSON[2];
		var ymax = escalaJSON[3];
		
		//Creación de un contenedor
		var svgContainer = d3.select("#poligono")
			.append("svg")
			.attr("id", "contenedor")
			.attr("width", width)
			.attr("height", height)
			.attr("border", 1)
			.attr("class", "svg");
		
		svgContainer.append("rect")
			.attr("width", "100%")
    		.attr("height", "100%")
    		.attr("fill", "black");
		
		
		//Definición de escala.
		var xScale = d3.scale.linear()
			.domain([xmin, xmax])
			.range([0, width]);
		
		var yScale = d3.scale.linear()
			.domain([ymin, ymax])
			.range([height, 0]);
		
		//Dibujado de las áreas de visión.
   		var areas = svgContainer.selectAll("area")
   			.data(areasJSON)
   			.enter()
   			.append("polygon")
   			.attr("class", "ar");
	
   		var vision = areas
   			.attr("points", function(d){
				return d.map(function(d) { return [xScale(d.x),yScale(d.y)].join(","); }).join(" ");})
			.attr("stroke","white")
   		    .attr("stroke-width",1.5)
   		    .attr("fill", "#2EFE2E");
   		    
   		//Dibujado de las intersecciones
   		var intersecciones = svgContainer.selectAll("interseccion")
   			.data(interJSON)
   			.enter()
   			.append("polygon")
   			.attr("class", "inter");
   		
   		var interseccion = intersecciones
   			.attr("points", function(d){
				return d.map(function(d) { return [xScale(d.x),yScale(d.y)].join(","); }).join(" ");})
   		    .attr("fill", "yellow");
   		    
		//Dibujado de polígono.
		var polygon = svgContainer.selectAll("poligono")
			.data([poly])
			.enter()
			.append("polygon")
			.attr("points", function(d){
				return d.map(function(d) { return [xScale(d.x),yScale(d.y)].join(","); }).join(" ");})
			.attr("stroke","grey")
   		    .attr("stroke-width",0.5)
   		    .attr("fill", "#FF7F50");
   		    
   		//Creación de etiquetas para los vértices del edificio.
   		var texts = svgContainer.selectAll("text")
   			.data(poly) 
   			.enter() 
	        .append("text");
	        
        var textLabels = texts
       		.attr("x", function(d) { return xScale(d.x);})
       		.attr("y", function(d) { return yScale(d.y);})
        	.text(function (d) { return "( " + d.x + ", " + d.y +" )";})
            .attr("font-family", "Arial")
            .attr("font-size", "11px")
            .attr("fill", "red");
		
		//Creación del border del contenedor.
		var borderPath = svgContainer.append("rect")
       			.attr("height", height)
       			.attr("width", width)
       			.style("stroke", "black")
       			.style("fill", "none")
       			.style("stroke-width", 2);
       	
       	//Creación del botón exportarSVG
        var html = d3.select("svg")
	        .attr("version", 1.1)
	        .attr("xmlns", "http://www.w3.org/2000/svg")
	        .node().parentNode.innerHTML;
 
	    //console.log(html);
	    var imgsrc = 'data:image/svg+xml;base64,'+ btoa(html);
	    var img = '<a href="'+imgsrc+'"download="'+$("#name").text()+'".svg class="svgIcon" style="text-decoration: none;"><span>Export to SVG</span></a>'; 
	    d3.select("#botonesSVG").html(img);
});









