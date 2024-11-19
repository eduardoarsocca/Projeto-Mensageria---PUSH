# TODO: Bibliotecas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
import requests
from urllib.parse import urljoin
from datetime import datetime, timedelta



#----------------------------------------------------------------------------------------------- 
# TODO: Carregar as variáveis de ambiente
load_dotenv()

api_username = os.getenv('API_USERNAME')
api_password = os.getenv('API_PASSWORD')
api_url = os.getenv("API_URL")

# Configurações do e-mail
enviar_para = ['eduardotestesvri@gmail.com', 'gleice.barros@svriglobal.com']
username_email = os.getenv('EMAIL_USERNAME')
password_email = os.getenv('EMAIL_PASSWORD')
server_email = os.getenv('EMAIL_SERVER')
port_email = int(os.getenv('EMAIL_PORT'))


# TODO: funções globais
# Obter o mês e o ano do mês atual menos 1 ano
mes_atual = datetime.now().month - 0
ano_atual = datetime.now().year
ano_anterior = datetime.now().year - 1
proximas_duas_semanas = (datetime.now()+timedelta(days=15)).strftime('%Y-%m-%d')
duas_ultimas_semanas = (datetime.now()-timedelta(days=15))
ultima_semana = (datetime.now() - timedelta(days=7))


# TODO: Configuração CSS
css_hover = """
<style>
    tr:hover {
        background-color: #EC0E73 !important;
    }
    div {
        margin: 40px 0px 40px 0 px;
    }
    h1 {
  font-size: 30px;
    }

    h2 {
    font-size: 20px;
    }

    p {
    font-size: 16px;
    }
    
    th {
        font-size: 12px;
        font-weight: bold;
    }
    td {
        font-size: 10px 
    }
</style>

"""     
## --------------------------EXTRAIR INFORMAÇÕES DE BIBLIOTECAS ---------------------------------
def extrair_ultima_informacao(x):
    if x is None:
        return None
    else:
        values_list = list(x.values())
        if len(values_list) == 0:
            return None
        else:
            return values_list[-1]
        
## -------------------------- VERIFICAR SE O DF ESTÁ COM VALORES ---------------------------------


## ----------------------------------VARIÁVEIS GLOBAIS -------------------------------------------


#------------------------------------------SEÇÃO--------------------------------------------------
# TODO: API 
# Corpo do login a ser utilizado no acesso
body = {
    "nome": api_username,
    "password":api_password
}

# Obtençao do token de acesso à polotrial
auth_url = urljoin(api_url, "/sessions")

response = requests.post(auth_url, json = body)

# # Verificar a resposta
# print(f"Status Code: {response.status_code}")
# print(f"Headers: {response.headers}")
# print(f"Content: {response.text}")

# Extraindo o token
token = response.json()["token"]

# Incorporando a string Bearer para inserir
if token:
    auth_token = "Bearer " + token
    # print(f"Auth Token: {auth_token}")
else:
    print("Falha ao obter o token.")
    
    
    
url_request = "https://api.polotrial.com"

headers = {"Authorization": auth_token}

# endregion
#------------------------------------------GENÉRICA-----------------------------------------------
# TODO: Generica

rota_generica = url_request+"/generica?nested=true"
df_generica = requests.get(rota_generica, headers = headers).json()
df_generica = pd.DataFrame(df_generica)
df_generica_limpo=df_generica[['id', 'ds_descricao']]
df_generica_limpo.head()

#------------------------------------------ROTAS---------------------------------------------- 
#TODO: Acesso Protocolos
rota_protocolo = url_request+"/protocolo?nested=true"
df_protocolo = requests.get(rota_protocolo, headers = headers).json()
df_protocolo = pd.DataFrame(df_protocolo)

#TODO: Acesso Participantes
rota_participantes = url_request+"/participantes?nested=true"
df_participantes = requests.get(rota_participantes, headers = headers).json()
df_participantes = pd.DataFrame(df_participantes)

#TODO: Acesso Participantes_visita (Agenda)
rota_participante_visita = url_request+"/participante_visita?nested=true"
df_participante_visita = requests.get(rota_participante_visita, headers=headers).json()
df_participante_visita = pd.DataFrame(df_participante_visita)

#TODO: Acesso Participantes_visita_procedimentos
rota_visita_procedimentos = url_request+"/power_bi_participante_visita_procedimento"
df_visita_procedimentos = requests.get(rota_visita_procedimentos, headers = headers).json()
df_visita_procedimentos = pd.DataFrame(df_visita_procedimentos)

#TODO: Acesso Eventos Adversos
rota_evento_adverso = url_request+"/evento_adverso?nested=true"
df_evento_adverso = requests.get(rota_evento_adverso, headers = headers).json()
df_evento_adverso = pd.DataFrame(df_evento_adverso) 


proximas_visitas = df_participante_visita.copy()

# Tratamento dos dados 
## selecionando os campos de interesse da agenda do participante
proximas_visitas = proximas_visitas[[
    'id',
    'co_participante',
    'nome_tarefa',
    'data_realizada',
    'dados_status',
]]

## Renomeando as colunas para facil visualização no dataframe
proximas_visitas.rename(columns = {
    'id':'id_agenda',
    'co_participante':'id_participante',
    'nome_tarefa':'visita',
    'data_realizada':'Data da visita realizada',
    'dados_status': 'Status da visita'
}, inplace = True)

# Obtendo os dados do participante
dim_participantes = df_participantes.copy()
## selecionando os campos de interesse
dim_participantes=dim_participantes[[
    'id',
    'id_participante',
    'co_protocolo',
    'dados_protocolo',
    'dados_status',
]]
## Renomeando as colunas para facil visualização no dataframe

dim_participantes.rename(columns ={
    'id':'id_participante',
    'id_participante': 'Participante',
    'co_protocolo': 'id_protocolo',
    'dados_protocolo': 'Protocolo',
    'dados_status': 'Status do Participante'
    }, inplace = True)

# Obtenção dos centros
dim_protocolo = df_protocolo.copy()
centros = dim_protocolo.copy()
## selecionando os campos de interesse
centros = centros[[
    'id',
    'dados_co_centro'
]]
## Renomeando as colunas para facil visualização no dataframe
centros = centros.rename(columns={
    'id': 'id_protocolo',
    'dados_co_centro': 'Centro'
})

# Merge dos 3 datasets para criar o dataframe final
proximas_visitas = proximas_visitas.merge(dim_participantes, how = 'left', on='id_participante')
proximas_visitas = proximas_visitas.merge(centros, how = 'left', on='id_protocolo')

# Extraindo as informações dos dicionários
colunas_a_extrair = [
    'Status da visita',
    'Protocolo',
    'Status do Participante',
    'Centro'
   
]
for coluna in colunas_a_extrair:
    proximas_visitas[coluna] = proximas_visitas[coluna].apply(extrair_ultima_informacao)
    
# Tratamento da coluna de datas
proximas_visitas['Data da visita realizada']= pd.to_datetime(proximas_visitas['Data da visita realizada']).dt.tz_localize(None)

# tratando valores faltantes
proximas_visitas['Protocolo']=proximas_visitas['Protocolo'].fillna('Indefinido')
proximas_visitas['Centro']=proximas_visitas['Centro'].fillna('Indefinido')
proximas_visitas = proximas_visitas.dropna(subset=['Data da visita realizada'])

proximas_visitas = proximas_visitas[[
    'Protocolo',
    'Centro',
    'Participante',
    'Status do Participante',
    'visita',
    'Status da visita',
    'Data da visita realizada'
]]

# Selecionando o período a ser notificado
proximas_visitas = proximas_visitas[
    (proximas_visitas['Data da visita realizada'] >= ultima_semana)
]

# Primeira período para titulo do email
proximas_visitas_no_periodo_min = proximas_visitas['Data da visita realizada'].min().strftime('%d/%m/%Y')

proximas_visitas_no_periodo_max =proximas_visitas['Data da visita realizada'].max().strftime('%d/%m/%Y')

# Função para criar a tabela do corpo do email 
def filtrar_proximas_visitas(dataframe, anos=3):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['Data da visita realizada'].notna(), :]
# Verificar se o DataFrame filtrado está vazio
    if proximas_visitas.empty:
        return "Próximas visitas não notificadas"
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_filtrado = proximas_visitas.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_filtrado.to_html(index=False)

# Chamando a função
proximas_visitas_html = filtrar_proximas_visitas(proximas_visitas)

# Função de envio do e-mail
def enviar_email_proximas_visitas():
    try:
        if proximas_visitas.empty:
            print("Sem relato de visitas realizadas na semana")
            return

        msg = MIMEMultipart("alternative")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = f"Visitas realizadas entre {proximas_visitas_no_periodo_min} e {proximas_visitas_no_periodo_max}"
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>Visitas realizadas entre {proximas_visitas_no_periodo_min} e {proximas_visitas_no_periodo_max}</h2>
                <p>{proximas_visitas_html}</p>
                <p>Eu vim para te mandar mensagens, mua ha ha</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print(f"Visitas realizadas entre {proximas_visitas_no_periodo_min} e {proximas_visitas_no_periodo_max}")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_proximas_visitas()