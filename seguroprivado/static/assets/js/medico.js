function eliminar() {
    Swal.fire({
        title: 'Mensaje de Salesin',
        text: "¿Desea eliminar este médico?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#076BCA',
        cancelButtonColor: '#C62D00',
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((medico) => {
        if (medico.isConfirmed) {
            // Al confimar la eliminación del médico
            window.location = '/eliminar_medico/' + id;
        } else {
            // Al cancelar dicha eliminación
            window.location = '/medicos/';
        }
    });
}