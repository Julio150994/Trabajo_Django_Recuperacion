function eliminar(id) {
    Swal.fire({
        title: 'Mensaje de Salesin',
        text: "¿Desea eliminar este medicamento?",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#2384BB',
        cancelButtonColor: '#EA2323',
        confirmButtonText: 'Sí',
        cancelButtonText: 'No',
    }).then((medico) => {
        if (medico.isConfirmed) {
            window.location = '/eliminar_medicamento/' + id + '/';
        } else {
            window.location = '/medicamentos/';
        }
    });
}