"""
Esse arquivo serve somente para testar as lógicas gerais da construção do aplicativo
"""

from PIL import ImageTk,Image
import requests
from datetime import datetime,timezone
import json
import pytz
import pycountry_convert as pc
import config







escolhe_cidade = 'London'
api_link = f'https://api.openweathermap.org/data/2.5/weather?q={escolhe_cidade}&appid={config.chave}'

#fazendo chamada da API usando request
r = requests.get(api_link)
#convertendo os dados
dados = r.json()
print(dados)


#obtendo zona, país e hora
pais_codigo = dados['sys']['country']

# ----- zona de fuso horário -----
zona_fuso = pytz.country_timezones[pais_codigo]

# ----- país -----
pais = pytz.country_names[pais_codigo]

# ----- data -----
if pais == 'Brazil':    #colocando no fuso de Brasilia para todas as cidades do Brasil.
    zona = pytz.timezone(zona_fuso[7])
else:
    zona = pytz.timezone(zona_fuso[0])

zona_hora = datetime.now(zona)
zona_hora = zona_hora.strftime("%d %m %Y | %H:%M:%S %p")

# ----- tempo -----
weather = dados['main']['temp']
pressure = dados['main']['pressure']
humidity = dados['main']['humidity']
wind_speed = dados['wind']['speed']
description = dados['weather'][0]['description']
temperature = dados['main']['temp']
temperature -= 273.15
print(round(temperature))

if pais_codigo == 'GB':     #essa linha de código se faz necessária pois o pycountry_converter não consegue ler Britain(UK)
    pais = 'Great Britain'

def informacao():
    def pais_para_continente(i):
        pais_alpha = pc.country_name_to_country_alpha2(i)
        pais_continente_codigo = pc.country_alpha2_to_continent_code(pais_alpha)
        pais_continente_name = pc.convert_continent_code_to_continent_name(pais_continente_codigo)
        return pais_continente_name

    continente = pais_para_continente(pais)

