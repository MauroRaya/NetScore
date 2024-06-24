async function editarPartida(elemento) {
    let span      = elemento.parentElement.querySelector('span');
    let texto     = span.textContent; 
    let novoTexto = prompt('Editar partida: ', texto);

    if (novoTexto !== null && novoTexto.trim() !== "") {
        let listaNaoOrdenada = elemento.closest('ul');
        let liElement        = elemento.closest('li');
        let indexPartida     = Array.from(listaNaoOrdenada.children).indexOf(liElement);

        try {
            fetch(`/partidas/?index=${indexPartida}&texto=${novoTexto}`, {
                method: 'PATCH'
            });
        }
        catch (erro) {
            console.log('Erro. ' + erro);
        }
    }
}