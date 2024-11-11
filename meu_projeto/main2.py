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
enviar_para = ['eduardotestesvri@gmail.com']
username_email = os.getenv('EMAIL_USERNAME')
password_email = os.getenv('EMAIL_PASSWORD')
server_email = os.getenv('EMAIL_SERVER')
port_email = int(os.getenv('EMAIL_PORT'))


# TODO: funções globais
# Obter o mês e o ano do mês atual menos 1 ano
mes_atual = datetime.now().month - 0
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

#TODO: Acesso Participantes_visita
rota_visita_procedimentos = url_request+"/power_bi_participante_visita_procedimento"
df_visita_procedimentos = requests.get(rota_visita_procedimentos, headers = headers).json()
df_visita_procedimentos = pd.DataFrame(df_visita_procedimentos)

#TODO: Acesso Eventos Adversos
rota_evento_adverso = url_request+"/evento_adverso?nested=true"
df_evento_adverso = requests.get(rota_evento_adverso, headers = headers).json()
df_evento_adverso = pd.DataFrame(df_evento_adverso)  


#TODO  Relato de EA/EAS
dim_evento_adverso = df_evento_adverso.copy()

ultima_infomacao_ea = [
    'dados_participante',
    'dados_classificacao_evento',
    'dados_protocolo',
    'dados_centro',
    'dados_status',
    'dados_relacao_produto_investigacional',
    'dados_intensidade',
    'dados_classificacao',
    'dados_tipo',
    'dados_situacao_participante',
    'dados_evento_esperado',
    'dados_demanda_judicial',
    'dados_participante_descontinuado'
    
]
for coluna in ultima_infomacao_ea:
    dim_evento_adverso[coluna] = dim_evento_adverso[coluna].apply(extrair_ultima_informacao)
    
dim_evento_adverso.rename(columns={
    'dados_protocolo': 'Protocolo',
    'dados_centro': 'Centro',
    'dados_participante': 'Participante',
    'dados_classificacao_evento': 'Classificação',
    'dados_status': 'Status do EA',
    'dados_relacao_produto_investigacional': 'Causalidade com o produto investigacional',
    'dados_intensidade': 'Intensidade do Evento',
    'dados_classificacao': 'Gravidade',
    'dados_tipo':'Tipo',
    'dados_situacao_participante': 'Situação do Participante',
    'dados_evento_esperado': 'EA esperado?',
    'dados_demanda_judicial': 'Houve demanda judicial?',
    'dados_participante_descontinuado': 'Participante descontinuado?',
    'data_do_evento':'Data do evento',
    'data_de_report_farmacovigilancia': 'Data de report para farmacovigilância',
    'data_de_report_cep': 'Data de report ao CEP',
    'codigo': 'Código'
}, inplace = True)

dim_evento_adverso = dim_evento_adverso[[
    'Protocolo',
    'Centro',
    'Participante',
    'Código',
    'Gravidade',
    'Tipo',
    'Intensidade do Evento',
    'Causalidade com o produto investigacional',
    'Situação do Participante',
    'Participante descontinuado?',
    'EA esperado?',
    'Houve demanda judicial?',
    'Status do EA',
    'Data do evento',
    'Data de report para farmacovigilância',
    'Data de report ao CEP'
]]

colunas_data = [
    'Data do evento',
    'Data de report para farmacovigilância',
    'Data de report ao CEP'
]
dim_evento_adverso[colunas_data] = dim_evento_adverso[colunas_data].apply(pd.to_datetime)

dim_evento_adverso=dim_evento_adverso.dropna(subset=['Protocolo'])
dim_evento_adverso=dim_evento_adverso.dropna(subset=['Data do evento'])

# # Filtrar os EA/EAS que ocorreram nos últimos 7 dias
dim_evento_adverso = dim_evento_adverso[
    (dim_evento_adverso['Data do evento'] >= ultima_semana)
]

#-----#
nome_protocolo_ea = dim_evento_adverso['Protocolo'].tolist()
nome_protocolo_ea_reg = ', '.join(nome_protocolo_ea)


#----#
data_ea = dim_evento_adverso['Data do evento'].tolist()
data_ea_reg = ', '.join([data.strftime('%d/%m/%Y') for data in data_ea])

#-----#
if not dim_evento_adverso.empty:
    ea_info = f"<p> Relato de evento adverso: Protocolo {nome_protocolo_ea_reg}, Data: {data_ea_reg}"
else:
    ea_info = ""


def filtrar_dim_evento_adverso(dataframe, anos=3):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['Data do evento'].notna(), :]
# Verificar se o DataFrame filtrado está vazio
    if dim_evento_adverso.empty:
        return "Nenhum Evento Adverso notificado"
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_filtrado = dim_evento_adverso.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_filtrado.to_html(index=False)

# Chamando a função
dim_evento_adverso_html = filtrar_dim_evento_adverso(dim_evento_adverso) 



def enviar_email_evento_adverso():
    try:
        if dim_evento_adverso.empty:
            print("Nenhum Evento Adverso notificado")
            return

        msg = MIMEMultipart("alternative")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = f"Evento Adverso relatado no Protocolo {nome_protocolo_ea_reg}. Evento ocorrido em {data_ea_reg}"
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>Eventos adversos relatados </h2>
                
                <p>{dim_evento_adverso_html}</p>
                <p>Eu vim para te mandar mensagens, mua ha ha</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print("Evento adverso relatado")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_evento_adverso()
