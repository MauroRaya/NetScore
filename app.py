from flask import Flask, request, render_template, redirect
from raspagem import buscar_partidas
import re

app = Flask(__name__)

COPA_ANO_INICIO = 2003
COPA_ANO_FIM    = 2015
PARTIDAS        = []
MENSAGEM_ERRO   = ''

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


def converter_texto_para_partida(texto):
    padrao  = re.compile(r'([^\W_]+(?:[\s-][^\W_]+)*)\s*(\d+)\s*x\s*(\d+)\s*([^\W_]+(?:[\s-][^\W_]+)*)')
    partida = padrao.search(texto)

    if not partida:
        return None

    resultado = {
        'nomeTimeA':   partida.group(1),
        'pontosTimeA': partida.group(2),
        'pontosTimeB': partida.group(3),
        'nomeTimeB':   partida.group(4)
    }

    return resultado


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/erro')
def erro():
    return render_template('erro.html', mensagem=MENSAGEM_ERRO)


@app.route('/raspar', methods=['POST'])
def raspar():
    global PARTIDAS, MENSAGEM_ERRO

    if request.method != 'POST':
        return render_template('index.html')
    
    ano_copa = request.form.get("ano_copa", None)
    
    if not validar_ano(ano_copa):
        MENSAGEM_ERRO = 'Número do ano da copa invalido.'
        return redirect('/erro')
        
    PARTIDAS = buscar_partidas(ano_copa)

    return redirect('/partidas') 
    

@app.route('/partidas', methods=['GET'])
def partidas():
    return render_template('partidas.html', partidas=PARTIDAS)


@app.route('/editar', methods=['POST'])
def editar():
    global PARTIDAS, MENSAGEM_ERRO

    if request.method != 'POST':
        return redirect('/partidas')

    index_partida = request.form.get('index', None)
    novo_texto    = request.form.get('texto', None)

    if index_partida is None or novo_texto is None:
        MENSAGEM_ERRO = 'Não foi possivel editar partida.'
        return redirect('/erro')
    
    try:
        index_partida = int(index_partida)
    except ValueError:
        MENSAGEM_ERRO = 'Índice de partida inválido.'
        return redirect('/erro')

    nova_partida = converter_texto_para_partida(novo_texto)

    if nova_partida is None:
        MENSAGEM_ERRO = 'Formato de partida inválido.'
        return redirect('/erro')

    try:
        PARTIDAS[index_partida] = nova_partida
    except IndexError:
        MENSAGEM_ERRO = 'Índice da partida inválido.'
        return redirect('/erro')

    return redirect('/partidas')


@app.route('/deletar', methods=['POST'])
def deletar():
    global PARTIDAS, MENSAGEM_ERRO

    if request.method != 'POST':
        return redirect('/partidas')

    index_partida = request.form.get('index', None)

    if index_partida is None:
        MENSAGEM_ERRO = 'Não foi possivel deletar partida.'
        return redirect('/erro')

    
    try:
        index_partida = int(index_partida)
        PARTIDAS.pop(index_partida)
    except IndexError:
        MENSAGEM_ERRO = 'Indice da partida inválido.'
        return redirect('/erro')


    return redirect('/partidas')


if __name__ == '__main__':
    app.run(debug=True)