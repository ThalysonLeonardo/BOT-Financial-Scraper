import time
import requests
import pandas as pd
from bs4 import BeautifulSoup, element
from selenium import webdriver
from webdriver_manager import driver
import webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager
import json

# Listas de Indicadores
valuation_list = []
debt_indicators_list = []
efficiency_list = []
profiability_list = []
growth_indicators_list = []

# Url base para consulta "Status Invest"
base_url = 'https://statusinvest.com.br/acoes/'

# input com o nome do papel(será substituido por uma planilha para consulta)
paper_name = input('Nome do ativo ou indice: ')
target_url = base_url + paper_name

# instala o drive do chrome evita incopatibilidade
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(target_url)
time.sleep(10)

# Verifica se existe pop up na página, se sim ele fecha
popup = driver.find_element_by_xpath(
    "//button[@class='btn-close']")
if popup:
    popup.click()

# Captura o html da tabela dos indicadores no site, facilitando a raspagem dos dados
element = driver.find_element_by_xpath(
    "//div[@id='indicators-section']//div[@class='indicator-today-container']")

indicators_table = element.get_attribute('outerHTML')

# Parseando conteúdo HTML da página
soup = BeautifulSoup(indicators_table, 'html.parser')

# Capturando conteúdo dos indicadores de valuation
valuation_table = soup.find("div", attrs={"data-group": "0"})
valuation_itens = valuation_table.findAll("div", attrs={"class": "item"})

# Capturando conteúdo dos indicadores de endividamento
debt_table = soup.find("div", attrs={"data-group": "2"})
debt_itens = debt_table.findAll("div", attrs={"class": "item"})

# Capturando conteúdo dos indicadores de eficiência
efficiency_table = soup.find("div", attrs={"data-group": "1"})
efficiency_itens = efficiency_table.findAll("div", attrs={"class": "item"})

# Capturando conteúdo dos indicadores de rentabilidade
profiability_table = soup.find("div", attrs={"data-group": "3"})
profiability_itens = profiability_table.findAll(
    "div", attrs={"class": "item"})

# Capturando conteúdo dos indicadores de crescimento
growth_table = soup.find("div", attrs={"data-group": "4"})
growth_itens = growth_table.findAll("div", attrs={"class": "item"})

# Cria uma lista com os indicadores de valuation capturados
for valuation_item in valuation_itens:
    title_vi = valuation_item.find("h3", attrs={"class": "title"})
    value_vi = valuation_item.find("strong", attrs={"class": "value"})

    valuation_list.append([title_vi.text, value_vi.text])

# Cria uma lista com os indicadores de endividamento
for debt_item in debt_itens:
    title_di = debt_item.find("h3", attrs={"class": "title"})
    value_di = debt_item.find("strong", attrs={"class": "value"})

    debt_indicators_list.append([title_di.text, value_di.text])

# Cria uma lista com os indicadores de eficiência
for efficiency_item in efficiency_itens:
    title_ei = efficiency_item.find("h3", attrs={"class": "title"})
    value_ei = efficiency_item.find("strong", attrs={"class": "value"})

    efficiency_list.append([title_ei.text, value_ei.text])

# Cria uma lista com os indicadores de rentabilidade
for profiability_item in profiability_itens:
    title_pi = profiability_item.find("h3", attrs={"class": "title"})
    value_pi = profiability_item.find("strong", attrs={"class": "value"})

    profiability_list.append([title_pi.text, value_pi.text])

# Cria uma lista com os indicadores de crescimento
for growth_item in growth_itens:
    title_gi = growth_item.find("h3", attrs={"class": "title"})
    value_gi = growth_item.find("strong", attrs={"class": "value"})

    growth_indicators_list.append([title_gi.text, value_gi.text])

# Cria o frame com os indicadores de Valuation e converte em json
vl_frame = pd.DataFrame(valuation_list, columns=[
    'Indicadores de Valuation', 'Valor'])

vl_frame.to_json('Valuation_Indicators.json')
print(vl_frame)

# Cria o frame com os indicadores de endividamento e converte em json
dl_frame = pd.DataFrame(debt_indicators_list, columns=[
    'Indicadores de Endividamento', 'Valor'])

dl_frame.to_json('Debt_Indicators.json')
print(dl_frame)

# Cria o frame com os indicadores de eficiência e converte em json
el_frame = pd.DataFrame(efficiency_list, columns=[
    'Indicadores de Eficiência', 'Valor'])

el_frame.to_json('Efficiency_Indicators.json')
print(el_frame)

# Cria o frame com os indicadores de Rentabilidade e converte em json
pl_frame = pd.DataFrame(profiability_list, columns=[
    'Indicadores de Rentabilidade', 'Valor'])

pl_frame.to_json('Profiability_Indicators.json')
print(pl_frame)

# Cria o frame com os indicadores de Crescimento e converte em json
gl_frame = pd.DataFrame(growth_indicators_list, columns=[
    'Indicadores de Crescimento', 'Valor'])

gl_frame.to_json('Growth_Indicators.json')
print(gl_frame)

driver.quit()
