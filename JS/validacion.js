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
		return true;
	}else{
		divErrores.html(errores);
		return false;
	}
}

$(document).ready(function()
    {	
    	$("#botonFunciona").click(function () {     
    	$("#ventanas").toggle('slow');
    });
});


