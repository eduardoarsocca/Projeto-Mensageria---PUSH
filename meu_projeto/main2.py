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


#TODO  Relato de 1ª visita
#TODO: Aprovação Regulatória

dim_regulatorio_aprovacao = df_protocolo.copy()
dim_regulatorio_aprovacao = dim_regulatorio_aprovacao[[
    'apelido_protocolo',
    'dados_patrocinador',
    'dados_co_centro',
    'status',
    'data_aprovacao_regulatorio',
    'status_regulatorio'
]]

filtro = dim_regulatorio_aprovacao['data_aprovacao_regulatorio'].notna()
dim_regulatorio_aprovacao = dim_regulatorio_aprovacao.loc[filtro,:] 

dim_regulatorio_aprovacao['data_aprovacao_regulatorio'] = pd.to_datetime(dim_regulatorio_aprovacao['data_aprovacao_regulatorio']).dt.normalize()

df_generica_limpo_regulatorio = df_generica_limpo.copy()

df_generica_limpo_regulatorio.rename(columns={'id': 'status_regulatorio', 'ds_descricao': 'regulatorio_status'}, inplace=True)



# Merge Regulatório-Generica
dim_regulatorio_aprovacao = dim_regulatorio_aprovacao.merge(df_generica_limpo_regulatorio, on='status_regulatorio', how='left')
dim_regulatorio_aprovacao.drop(columns=['status_regulatorio'], inplace = True)
status_interesse = ['Aguardando Ativação do Centro',
       'Qualificado', 'Fase Contratual',
       'Em apreciação Ética', 'Aprovado pelo CEP',
       'Aguardando o Pacote Regulatório']

dim_regulatorio_aprovacao = dim_regulatorio_aprovacao.query("status in @status_interesse")

# Filtrar contratos assinados no mesmo mês do ano anterior
dim_regulatorio_aprovacao = dim_regulatorio_aprovacao[
    (dim_regulatorio_aprovacao['data_aprovacao_regulatorio'].dt.month == mes_atual) 
]

apelidos_protocolo = dim_regulatorio_aprovacao['apelido_protocolo'].tolist()
apelidos_protocolo_aprovacao_reg = ', '.join(apelidos_protocolo)
data_protocolo = dim_regulatorio_aprovacao['data_aprovacao_regulatorio'].tolist()
data_protocolo_aprovacao_reg = ', '.join([data.strftime('%d/%m/%Y') for data in data_protocolo])

if apelidos_protocolo_aprovacao_reg:
    protocolo_info = f"<p> Protocolo {apelidos_protocolo_aprovacao_reg} aprovado na avaliação regulatória na data de {data_protocolo_aprovacao_reg}"
else:
    protocolo_info = ""


def filtrar_aprovacao_regulatorio(dataframe, anos=3):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['data_aprovacao_regulatorio'].notna(), :]
# Verificar se o DataFrame filtrado está vazio
    if dim_regulatorio_aprovacao.empty:
        return "Nenhum protocolo submetido para avaliação regulatória"
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_filtrado = dim_regulatorio_aprovacao.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_filtrado.to_html(index=False)

# Chamando a função
dim_regulatorio_aprovacao_html = filtrar_aprovacao_regulatorio(dim_regulatorio_aprovacao) 



def enviar_email_aprovacao_regulatorio():
    try:
        if not apelidos_protocolo_aprovacao_reg:
            print("Nenhum protocolo aprovado na regulatória no período.")
            return

        msg = MIMEMultipart("alternative")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = f"Protocolo {apelidos_protocolo_aprovacao_reg} aprovado na avaliação regulatória"
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>Protocolos aprovados pelo órgão regulatório </h2>
                {protocolo_info}
                <p>{dim_regulatorio_aprovacao_html}</p>
                <p>Eu vim para te mandar mensagens, mua ha ha</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print("E-mail de aprovacao regulaória enviado com sucesso!")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_aprovacao_regulatorio()
print(dim_regulatorio_aprovacao_html)
