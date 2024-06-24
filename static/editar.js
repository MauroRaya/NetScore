async function editarPartida(index, event) {
    event.preventDefault();
    
    let novoTexto = prompt('Editar partida:');
    
    if (novoTexto !== null && novoTexto.trim() !== "") {
        fetch('/editar', {
            method: 'POST',
            body: new URLSearchParams({
                index: index,
                texto: novoTexto
            })
        }).then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                alert('Erro ao editar a partida.');
            }
        });
    }
}
