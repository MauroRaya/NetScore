from flask import Flask, request, render_template, redirect, url_for
from scraper import buscar_partidas


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
    return render_template('index.html', partidas=partidas)


@app.route('/', methods=['POST'])
def scrape():
    global partidas
    ano_copa = request.form.get("ano_copa", None)
    
    if validar_ano(ano_copa):
        partidas = buscar_partidas(ano_copa)
        
    return render_template('index.html', partidas=partidas)


@app.route('/', methods=['PATCH'])
def editar_partidas():
    global partidas
    index_partida = int(request.args.get('index', None))
    novo_texto    = request.args.get('texto', None)
    partidas[index_partida] = novo_texto
    return render_template('index.html', partidas=partidas)


@app.route('/', methods=['DELETE'])
def deletar_partidas():
    global partidas
    index_partida = int(request.args.get('index', None))
    partidas.pop(index_partida)
    return render_template('index.html', partidas=partidas)


if __name__ == '__main__':
    app.run(debug=True)