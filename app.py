from flask import Flask, request, render_template
from raspagem import buscar_partidas


app = Flask(__name__)

COPA_ANO_INICIO = 2001
COPA_ANO_FIM = 2015

partidas = []


def validar_ano(_ano_copa):
    try:
        _ano_copa = int(_ano_copa)

    except ValueError:
        return False
    
    except Exception:
        return False
    
    if not (COPA_ANO_INICIO <= _ano_copa <= COPA_ANO_FIM):
        return False
    
    return True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/partidas', methods=['POST'])
def raspar():
    global partidas
    ano_copa = request.form.get("ano_copa", None)
    
    if not validar_ano(ano_copa):
        return render_template('erro.html', mensagem='Número do ano da copa invalido.')
        
    partidas = buscar_partidas(ano_copa)

    return render_template('partidas.html', partidas=partidas)


@app.route('/partidas', methods=['PATCH', 'GET'])
def editar_partidas():
    global partidas

    if request.method == 'PATCH':
        index_partida = int(request.args.get('index', None))
        novo_texto    = request.args.get('texto', None)

        if not index_partida:
            return render_template('erro.html', mensagem='Não foi possivel editar partida.')
        
        if not novo_texto:
            return render_template('erro.html', mensagem='Texto da nova partida invalido.')
        
        partidas[index_partida] = novo_texto

        return render_template('partidas.html', partidas=partidas)
    
    return render_template('erro.html', mensagem='Método HTTP invalido.')


@app.route('/partidas', methods=['POST', 'GET'])
def deletar_partida():
    global partidas

    if request.method == 'POST':
        index_partida = int(request.form['index'])

        if not index_partida:
            return render_template('erro.html', mensagem='Não foi possivel deletar partida.')

        partidas.pop(index_partida)

        return render_template('partidas.html', partidas=partidas)
    
    return render_template('erro.html', mensagem='Método HTTP invalido.')


if __name__ == '__main__':
    app.run(debug=True)