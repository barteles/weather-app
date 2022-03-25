"""
PROJETO DE APLICATIVO DE TEMPO UTILIZANDO API

"""
import tkinter
from tkinter import *
from tkinter import ttk

from PIL import ImageTk,Image
import requests
from datetime import datetime,timezone
import json
import pytz
import pycountry_convert as pc


global imagem
##### Cores
cor1 = "#0a0a0a"     #cor preta
cor2 = "#feffff"     #cor branca
cor3 = "#6f9fbd"     #cor azul

fundo_dia = "#6cc4cc"
fundo_noite = "#484f60"
fundo_tarde = "#bfb86d"
fundo = fundo_dia

#criando a interface
janela = Tk()
janela.title('A Weather APP')
janela.geometry('320x350')
janela.configure(bg=fundo)
ttk.Separator(janela, orient= HORIZONTAL).grid(row=0, columnspan=1,ipadx=157)
img = PhotoImage(file ='Imagens/nuvem-dia1.png')
janela.iconphoto(False,img)

frame_superior= Frame(janela,width=320,height=50, bg=cor2, pady=0, padx=0)
frame_superior.grid(row=1, column =0)

frame_corpo= Frame(janela,width=320,height=300, bg=fundo, pady=12, padx=0)
frame_corpo.grid(row=2, column =0, sticky=NW)

estilo = ttk.Style()
estilo.theme_use('clam')


def informacao():

    chave = '387edf4a7d0c0133440ab024137eaaed'
    escolhe_cidade = local.get()
    api_link = f'https://api.openweathermap.org/data/2.5/weather?q={escolhe_cidade}&appid={chave}'

    #fazendo chamada da API usando request
    r = requests.get(api_link)
    #convertendo os dados
    dados = r.json()


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
    temperature = round(temperature - 273.15)

    if pais_codigo == 'GB':     #essa linha de código se faz necessária pois o pycountry_converter não consegue ler Britain(UK)
        pais = 'Great Britain'

    def pais_para_continente(i):
        pais_alpha = pc.country_name_to_country_alpha2(i)
        pais_continente_codigo = pc.country_alpha2_to_continent_code(pais_alpha)
        pais_continente_name = pc.convert_continent_code_to_continent_name(pais_continente_codigo)
        return pais_continente_name

    continente = pais_para_continente(pais)

    #passando as informações para as Labels
    cidade['text'] = escolhe_cidade + " - " + pais + " / " + continente
    data['text'] = zona_hora
    humidade_num['text'] = humidity
    humidade_simb['text'] = '%'
    humidade_nome['text'] = 'Humidade'
    pressao['text'] = 'Pressão : ' + str(pressure)
    vel_vento['text'] = 'Velocidade do vento : ' +  str(wind_speed)
    descricao['text'] = description
    temperatura['text'] = str(temperature) + ' °C'


    #logica da troca do fundo para cada horário
    zona_periodo = datetime.now(zona)
    zona_periodo = zona_periodo.strftime('%H')

    global imagem

    zona_periodo = int(zona_periodo)
    if 0< zona_periodo <= 5:
        if 'cloud' in description:
            imagem = Image.open('Imagens/nuvem-noite1.png')
            fundo = fundo_noite
        else:
            imagem = Image.open('Imagens/lua.png')
            fundo = fundo_noite

    elif zona_periodo <= 11:
        if 'cloud' in description:
            imagem = Image.open('Imagens/nuvem-dia1.png')
            fundo = fundo_dia
        else:
            imagem = Image.open('Imagens/sol-dia.png')
            fundo = fundo_dia

    elif zona_periodo <= 17:
        if 'cloud' in description:
            imagem = Image.open('Imagens/nuvem-dia1.png')
            fundo = fundo_tarde
        else:
            imagem = Image.open('Imagens/sol-tarde.png')
            fundo = fundo_tarde

    elif zona_periodo <= 24:
        if 'cloud' in description:
            imagem = Image.open('Imagens/nuvem-noite1.png')
            fundo = fundo_noite
        else:
            imagem = Image.open('Imagens/lua.png')
            fundo = fundo_noite

    else:
        pass

    imagem = imagem.resize((130, 130))
    imagem = ImageTk.PhotoImage(imagem)
    icone = Label(frame_corpo, image=imagem, bg=fundo)
    icone.place(x=180, y=70)

    janela.configure(bg=fundo)
    frame_corpo.configure(bg=fundo)
    frame_superior.configure(bg=fundo)

    cidade['bg'] = fundo
    data['bg'] = fundo
    humidade_num['bg'] = fundo
    humidade_simb['bg'] = fundo
    humidade_nome['bg'] = fundo
    pressao['bg'] = fundo
    vel_vento['bg'] = fundo
    descricao['bg'] = fundo
    temperatura['bg'] = fundo



#configurando frame_superior
local = Entry(frame_superior, width=20, justify='left', font=('',14), highlightthickness=1, relief='solid')
local.place(x=15, y=10)
#higlightthickness é a borda da Entry, deixando ela mais aparente ao clicar na mesma

botao_ver = Button(frame_superior, command = informacao, text='Ver clima',bg=cor2,fg=cor3, font=('Ivy 9 bold'),
                   relief= 'raised',  overrelief=RIDGE)
botao_ver.place(x=250, y=10)

#configurando frame corpo
cidade = Label(frame_corpo, text='',anchor='center',bg=fundo,fg=cor2, font=('Arial 14'))
cidade.place(x=10, y=4)

data = Label(frame_corpo, text='',anchor='center',bg=fundo,fg=cor2, font=('Arial 10'))
data.place(x=10, y=50)

humidade_num = Label(frame_corpo, text='',anchor='center',bg=fundo,fg=cor2, font=('Arial 45'))
humidade_num.place(x=10, y=90)
humidade_simb = Label(frame_corpo, text='',anchor='center',bg=fundo,fg=cor2, font=('Arial 10 bold'))
humidade_simb.place(x=90, y=100)
humidade_nome = Label(frame_corpo, text='',anchor='center',bg=fundo,fg=cor2, font=('Arial 8'))
humidade_nome.place(x=90, y=130)

pressao = Label(frame_corpo, text='',anchor='center',bg=fundo,fg=cor2, font=('Arial 10'))
pressao.place(x=10, y=220)

vel_vento = Label(frame_corpo, text='',anchor='center',bg=fundo,fg=cor2, font=('Arial 10'))
vel_vento.place(x=10, y=240)

descricao = Label(frame_corpo, text='',anchor='center',bg=fundo,fg=cor2, font=('Arial 10'))
descricao.place(x=210, y=230)

temperatura = Label(frame_corpo, text='',anchor='center',bg=fundo,fg=cor2, font=('Arial 25'))
temperatura.place(x=10, y=160)



janela.mainloop()

