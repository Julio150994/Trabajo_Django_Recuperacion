function eliminar(id) {
    Swal.fire({
        title: 'Mensaje de Salesin',
        text: "¿Desea eliminar este médico?",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#178ABC',
        cancelButtonColor: '#B91308',
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((medico) => {
        if (medico.isConfirmed) {
            window.location = '/eliminar_medico/' + id + '/';
        } else {
            window.location = '/medicos/';
        }
    });
}