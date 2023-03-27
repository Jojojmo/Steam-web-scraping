#Bibliotecas Utilizadas

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import re
import datetime

#Configurações do Web Driver
chrome_options = Options()
chrome_options.add_argument("--headless")
navegador = webdriver.Chrome(options=chrome_options)


url = 'https://store.steampowered.com/charts/mostplayed'

navegador.get(url)

sleep(8)

# COnvertendo para soup

conteudo = BeautifulSoup(navegador.page_source, 'html.parser')

#Encontrando e armazenando informações das linhas do site

rows_steam = conteudo.find_all('tr')
rows_steam = rows_steam[1:]

# Listas para armazenar as colunas de preço

preco_full = []
desconto_preco = []
preco_atual = []

# Laço que verifica descontos e adiciona os valores nas listas 

for p in range(len(rows_steam)):
    nome = rows_steam[p].find('div',{'class':re.compile("((salepreviewwidgets_Store)(.*))")})
    if nome is None:
        preco_full.append(nome)
        desconto_preco.append(None)
        preco_atual.append(None)
    else:
        quant_itens = nome.find_all('div')
        if len(quant_itens) > 3:
            desconto_preco.append(quant_itens[0].text)
            preco_full.append(quant_itens[2].text)
            preco_atual.append(quant_itens[3].text)
        else:
            desconto_preco.append(None)
            preco_full.append(quant_itens[0].text)
            preco_atual.append(None)

# Função para as demais colunas que não são preços

def rows_vals_unicos(html_tag,classe_div):
    lista_rows = []
    for p in range(len(rows_steam)):
        row_atual = rows_steam[p].find(html_tag,{'class':re.compile(classe_div)})
        if row_atual is None:
            lista_rows.append(row_atual)
        else:
            lista_rows.append(row_atual.text)
    return lista_rows


nomes_jogos = rows_vals_unicos("div","((weeklytopsellers_GameName)(.*))")
jogando_agora = rows_vals_unicos('td',"((weeklytopsellers_ConcurrentCell)(.*))")
pico_diario = rows_vals_unicos('td',"((weeklytopsellers_PeakInGameCell)(.*))")

# Criação do dataframe

dict_steam = {"Nome":nomes_jogos,"Preço inteiro":preco_full,"Desconto":desconto_preco,
              "Preço se desconto":preco_atual,"Jogadores atuais":jogando_agora,"Pico diario": pico_diario}

df_steam = pd.DataFrame(dict_steam)

# Exportando para .csv

data_do_export = datetime.datetime.now()
data_do_export = data_do_export.strftime("%d-%m-%Y")

df_steam.to_csv(f'{data_do_export} - Steam 100 mais jogados - v1.csv')