from pymongo import MongoClient
import re
from selenium import webdriver

# Validando input do usuario (ano da copa que ele deseja consultar)
while True:
    ano_copa = input('Digite o ano da copa que deseja buscar. (2001-2015): ')
    
    if ano_copa.isdigit():
        ano_copa = int(ano_copa)

        if 2001 <= ano_copa <= 2015:
            break

url_conexao_mongodb = input('Digite a url de conexão do MongoDB: ')

# Abrindo browser e site
url_site = f'https://www.branqs.com.br/copaBranqs/copaBranqs{ano_copa}/copabranqs{ano_copa}.html'
browser = webdriver.Chrome()
browser.get(url_site)

# Pegando elementos HTML
elementos = browser.find_elements('xpath', '//p[font[@size="5"]]|//i[font[@size="5"]]')
padrao = re.compile(r'([^\W_]+(?:[\s-][^\W_]+)*)\s*(\d+)\s*x\s*(\d+)\s*([^\W_]+(?:[\s-][^\W_]+)*)')

dados_partidas = []

# Iterando elementos webDriver encontrados
for elemento in elementos:
    informacoes_partida = elemento.text
    resultados = padrao.findall(informacoes_partida)
    
    # Iterando .text HTML dos elementos
    for resultado in resultados:
        time1, gols1, gols2, time2 = resultado
        # Criando objeto com os resultados
        dados_partida = {
            'nomeTimeA': time1.strip(),
            'pontosTimeA': gols1,
            'nomeTimeB': time2.strip(),
            'pontosTimeB': gols2
        }
        # Colocando no array de objetos
        dados_partidas.append(dados_partida)

# Fechando navegador
browser.quit()

# Mostrar dados encontrados no console
for i, dados in enumerate(dados_partidas):
    print(dados['nomeTimeA'], dados['pontosTimeA'], dados['nomeTimeB'], dados['pontosTimeB'])
print(f'{i+1} Jogos encontrados.')

# Tentando conectar com o MongoDB
try:
    client = MongoClient(url_conexao_mongodb)
    db = client['copaBranqs']
    collection = db[str(ano_copa)]
    collection.insert_many(dados_partidas)

    print("Dados inseridos com sucesso!")

except Exception as erro:
    print('Erro ao tentar conectar com o MongoDB. ', erro)