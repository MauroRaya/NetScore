from bs4 import BeautifulSoup
# from pymongo import MongoClient
from selenium import webdriver
import re

def buscar_partidas(_ano_copa):
    url_site = f'https://www.branqs.com.br/copaBranqs/copaBranqs{_ano_copa}/copabranqs{_ano_copa}.html'
    navegador = webdriver.Chrome()
    navegador.get(url_site)

    html = navegador.page_source
    soup = BeautifulSoup(html, 'html.parser')

    partidas = []

    elementos = soup.find_all('p') # Pegando todos os elementos HTML com a formatação que PODE ser uma partida
    padrao = re.compile(r'([^\W_]+(?:[\s-][^\W_]+)*)\s*(\d+)\s*x\s*(\d+)\s*([^\W_]+(?:[\s-][^\W_]+)*)') # Gerando formatação/padrão de uma partida -> (TimeA 0 x 0 TimeB) 

    for elemento in elementos:
        texto = elemento.text
        partida = padrao.search(texto) # Verificando se texto HTML bate o padrão de uma partida

        if not partida:
            continue

        partidas.append({
            'nomeTimeA':    partida.group(1),
            'pontosTimeA':  partida.group(2),
            'pontosTimeB':  partida.group(3),
            'nomeTimeB':    partida.group(4)
        })

    navegador.quit()
    return partidas