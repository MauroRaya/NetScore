async function editarPartida(elemento) {
    let span      = elemento.parentElement.querySelector('span');
    let texto     = span.textContent; 
    let novoTexto = prompt('Editar partida: ', texto);

    if (novoTexto !== null && novoTexto.trim() !== "") {
        let listaNaoOrdenada = elemento.closest('ul');
        let liElement = elemento.closest('li');
        let indexPartida = Array.from(listaNaoOrdenada.children).indexOf(liElement);

        try {
            let response = await fetch(`/?index=${indexPartida}&texto=${novoTexto}`, {
                method: 'PATCH'
            });

            if (!response.ok) {
                throw new Error('Erro ao tentar editar partida');
            }

            span.textContent = novoTexto;
        } catch (error) {
            console.error('Erro: ', error);
            alert('Um erro aconteceu ao tentar editar a partida');
        }
    }
}

async function removerPartida(elemento) {
    let resposta = confirm('Deseja remover essa partida?');

    if (resposta) {
        let listaNaoOrdenada = elemento.closest('ul');
        let liElement = elemento.closest('li');
        let indexPartida = Array.from(listaNaoOrdenada.children).indexOf(liElement);

        try {
            let response = await fetch(`/?index=${indexPartida}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Erro ao tentar deletar partida');
            }

            listaNaoOrdenada.removeChild(liElement);
        } catch (error) {
            console.error('Erro: ', error);
            alert('Um erro aconteceu ao tentar deletar a partida');
        }
    }
}
