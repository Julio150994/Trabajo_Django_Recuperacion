/** Habilitamos el botón de búsqueda cuando introducimos en la barra de búsqueda */
function habilitar_busqueda() {
    buscar_fecha = document.getElementById("fecha").value;
    longitud_cadena = 0;

    if (buscar_fecha == "") {
        longitud_cadena += 1;
    }

    if (longitud_cadena == 0) {
        document.getElementById("boton").disabled = false;
    } else {
        document.getElementById("boton").disabled = true;
    }
}

// Para el rellenado de datos
document.getElementById("fecha").addEventListener("keyup", habilitar_busqueda);