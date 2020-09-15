function validar() {
    var contrasena = document.getElementById("contrasena").value;
    var conf_contrasena = document.getElementById("c_contrasena").value;

    if (contrasena != conf_contrasena) {
        alert("Las contraseñas no coinciden");
        return false;
    }
}