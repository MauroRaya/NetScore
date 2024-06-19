function editarPartida(elemento) {
    let li = elemento.parentElement;
    let span = li.querySelector('span');
    let texto = span.textContent;
    let novoTexto = prompt('Editar partida: ', texto);

    if (novoTexto !== null && novoTexto.trim() !== null) {
        span.textContent = novoTexto;
    }
}

function removerPartida(elemento) {
    let resposta = confirm('Deseja remover essa partida?');

    if (resposta) {
        let li = elemento.parentElement;
        li.parentElement.removeChild(li)
    }
}