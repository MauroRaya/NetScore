from flask import Flask, render_template, request
from bs4 import BeautifulSoup
# from pymongo import MongoClient
from selenium import webdriver
import re


app = Flask(__name__)


COPA_ANO_INICIO = 2001
COPA_ANO_FIM = 2015


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ano_copa = request.form['ano_copa']

        if not validar_ano_copa(ano_copa):
            return render_template('index.html', error="Ano inválido.")
        
        navegador = abrir_site(ano_copa)

        if not navegador:
            return render_template('index.html', error="Erro ao abrir site copaBranqs.")

        partidas = buscar_partidas(navegador)

        if not partidas:
            return render_template('index.html', error="Partidas não encontradas.")
        
        return render_template('index.html', partidas=partidas)


def validar_ano_copa(_ano_copa):
    try:
        _ano_copa = int(_ano_copa)

    except ValueError:
        return False

    if not (COPA_ANO_INICIO <= _ano_copa >= COPA_ANO_FIM):
        return False
    
    return True


def abrir_site(_ano_copa):
    url_site = f'https://www.branqs.com.br/copaBranqs/copaBranqs{_ano_copa}/copabranqs{_ano_copa}.html'
    navegador = webdriver.Chrome() # Abrindo navegador
    navegador.get(url_site)        # Entrando na página

    return navegador


def buscar_partidas(_navegador):
    html = _navegador.page_source               # Pegando HTML puro
    soup = BeautifulSoup(html, 'html.parser')   # Gerando sopa do HTML (facilita d+ a vida)

    partidas = []

    elementos = soup.find_all('p')                                                                      # Pegando possiveis elementos HTML com a formatação de uma partida
    padrao = re.compile(r'([^\W_]+(?:[\s-][^\W_]+)*)\s*(\d+)\s*x\s*(\d+)\s*([^\W_]+(?:[\s-][^\W_]+)*)') # Gerando formatação de uma partida (TimeA x TimeB) 

    for elemento in elementos:
        texto = elemento.text
        partida = padrao.search(texto) # Verificando se texto do elemento HTML bate o padrão (TimeA x TimeB)

        if not partida:
            continue

        partidas.append({
            'nomeTimeA':    partida.group(1),
            'pontosTimeA':  partida.group(2),
            'pontosTimeB':  partida.group(3),
            'nomeTimeB':    partida.group(4)
        })

    _navegador.quit()
    return partidas


if __name__ == '__main__':
    app.run(debug=True)