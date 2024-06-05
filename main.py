from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
import re


COPA_ANO_INICIO = 2001
COPA_ANO_FIM = 2015


# -------------------------------------------------------------------------------------
while True:
    ano_copa = input(f'Digite o ano da copa que deseja buscar. ({COPA_ANO_INICIO}-{COPA_ANO_FIM}): ')

    if not ano_copa.isdigit():
        continue

    if COPA_ANO_INICIO <= int(ano_copa) <= COPA_ANO_FIM:
        break

# -------------------------------------------------------------------------------------
while True:
    conectar_db = input('Deseja armazenar dados automaticamente no MongoDB? (s/n): ').lower()

    if conectar_db == 's' or conectar_db == 'n':
        break

if conectar_db == 's':
    url_conexao_mongodb = input('Digite a url de conexão do MongoDB: ')

# -------------------------------------------------------------------------------------
url_site = f'https://www.branqs.com.br/copaBranqs/copaBranqs{ano_copa}/copabranqs{ano_copa}.html'
navegador = webdriver.Chrome()
navegador.get(url_site)

html = navegador.page_source
soup = BeautifulSoup(html, 'html.parser')

partidas = []

elementos = soup.find_all('p') # Pegando partidas com essa formatação HTML
padrao = re.compile(r'([^\W_]+(?:[\s-][^\W_]+)*)\s*(\d+)\s*x\s*(\d+)\s*([^\W_]+(?:[\s-][^\W_]+)*)')

for elemento in elementos:
    texto = elemento.text
    partida = padrao.search(texto)

    if not partida:
        continue

    partidas.append({
        'nomeTimeA':    partida.group(1),
        'pontosTimeA':  partida.group(2),
        'pontosTimeB':  partida.group(3),
        'nomeTimeB':    partida.group(4)
    })

if not partidas:
    print('Não foi possivel encontrar uma partida.')
    quit()

for i, partida in enumerate(partidas):
    print(f"{partida['nomeTimeA']} {partida['pontosTimeA']} x {partida['pontosTimeB']} {partida['nomeTimeB']}")
print(f'{i+1} partidas encontradas.')

# -------------------------------------------------------------------------------------
if conectar_db == 'n':
    quit()

try:
    client = MongoClient(url_conexao_mongodb)
    db = client['copaBranqs']
    collection = db[ano_copa]
    collection.insert_many(partidas)

    print("Dados inseridos com sucesso!")

except Exception as erro:
    print('Erro ao tentar conectar com o MongoDB. ', erro)
