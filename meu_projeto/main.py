# TODO: Bibliotecas

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
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
import io
from io import BytesIO
import base64
from email.mime.image import MIMEImage
import openpyxl


#----------------------------------------------------------------------------------------------- 
# TODO: Carregar as variáveis de ambiente
load_dotenv()

api_username = os.getenv('API_USERNAME')
api_password = os.getenv('API_PASSWORD')
api_url = os.getenv("API_URL")

# TODO: Configurações do e-mail
enviar_para = os.getenv('DESTINATARIO')
print(f"Valor original do DESTINATARIO: {enviar_para}")
if enviar_para:
    enviar_para = [email.strip() for email in enviar_para.split(',')]
else:
    enviar_para = []
username_email = os.getenv('EMAIL_USERNAME')
password_email = os.getenv('EMAIL_PASSWORD')
server_email = os.getenv('EMAIL_SERVER')
port_email = int(os.getenv('EMAIL_PORT'))


# TODO: variáveis de período
mes_atual = datetime.now().month - 0 
ano_atual = datetime.now().year
ano_anterior = datetime.now().year - 1
proximas_duas_semanas = (datetime.now()+timedelta(days=15)).strftime('%Y-%m-%d')
duas_ultimas_semanas = (datetime.now()-timedelta(days=15))
ultima_semana = (datetime.now() - timedelta(days=7))
proxima_semana = (datetime.now()+timedelta(days=7))
amanha = (datetime.now()+timedelta(days=0))
ontem = (datetime.now()-timedelta(days=1))

# TODO: Configuração CSS
css_hover = """
<style>
    tr:hover {
        background-color: #EC0E73 !important;
        color: #FFFFFF;
    }
    div {
        margin: 40px 0px 40px 0 px;
        overflow-x:auto;
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
        font-size: 16px;
        font-weight: bold;
        background-color: #041266;
        color: #FFFFFF;
        white-space: nowrap;
    }
    td {
        font-size: 14px 
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


def extrair_segunda_informacao(x):
    if x is None:
        return None
    else:
        values_list = list(x.values())
        if len(values_list) == 0:
            return None
        else:
            return values_list[1]
        
def extrair_terceira_informacao(x):
    if x is None:
        return None
    else:
        values_list = list(x.values())
        if len(values_list) == 0:
            return None
        else:
            return values_list[2] if len(values_list) > 2 else None

        
def extrair_apelido_protocolo(x):
    if x is None:
        return None
    elif 'apelido_protocolo' in x:
        return x['apelido_protocolo']
    else:
        return None
    
    
def extrair_campo(x, *chaves):
# """
# Extrai um campo aninhado de um dicionário dado um conjunto de chaves.
# :param x: O dicionário de entrada.
# :param chaves: Chaves para navegar no dicionário.
# :return: O valor extraído ou None se a navegação falhar.
# """
    if isinstance(x, dict):
        for chave in chaves:
            x = x.get(chave)
            if x is None:
                return None
        return x
    return None

#------------------------------------------SEÇÃO--------------------------------------
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
    
    
    


headers = {"Authorization": auth_token}

# endregion
#------------------------------------------GENÉRICA-----------------------------------------------
# TODO: Generica

rota_generica = api_url+"/generica?nested=true"
df_generica = requests.get(rota_generica, headers = headers).json()
df_generica = pd.DataFrame(df_generica)
df_generica_limpo=df_generica[['id', 'ds_descricao']]
df_generica_limpo.head()

#------------------------------------------ROTAS---------------------------------------------- 
#TODO: Acesso Protocolos
rota_protocolo = api_url+"/protocolo?nested=true"
df_protocolo = requests.get(rota_protocolo, headers = headers).json()
df_protocolo = pd.DataFrame(df_protocolo)

#TODO: Acesso Participantes
rota_participantes = api_url+"/participantes?nested=true"
df_participantes = requests.get(rota_participantes, headers = headers).json()
df_participantes = pd.DataFrame(df_participantes)

#TODO: Acesso Participantes_visita (Agenda)
rota_participante_visita = api_url+"/participante_visita?nested=true"
df_participante_visita = requests.get(rota_participante_visita, headers=headers).json()
df_participante_visita = pd.DataFrame(df_participante_visita)

#TODO: Acesso Participantes_visita_procedimentos
rota_visita_procedimentos = api_url+"/power_bi_participante_visita_procedimento"
df_visita_procedimentos = requests.get(rota_visita_procedimentos, headers = headers).json()
df_visita_procedimentos = pd.DataFrame(df_visita_procedimentos)

#TODO: Acesso Eventos Adversos
rota_evento_adverso = api_url+"/evento_adverso?nested=true"
df_evento_adverso = requests.get(rota_evento_adverso, headers = headers).json()
df_evento_adverso = pd.DataFrame(df_evento_adverso)  

# TODO: Flowchart
rota_flowchart = api_url +"/protocolo_flowchart"
df_flowchart = requests.get(rota_flowchart, headers = headers).json()
df_flowchart = pd.DataFrame(df_flowchart)

# TODO: Pessoas
rota_pessoas = api_url + "/pessoas?nested=true"
df_pessoas = requests.get(rota_pessoas, headers = headers).json()
df_pessoas = pd.DataFrame(df_pessoas)

# TODO: Protocolo Financeiro
rota_protocolo_financeiro = api_url+"/protocolo_financeiro?nested=true"
df_protocolo_financeiro = requests.get(rota_protocolo_financeiro, headers = headers).json()
df_protocolo_financeiro = pd.DataFrame(df_protocolo_financeiro)

# TODO: Recebimentos
rota_recebimento = api_url + "/recebimento?nested=true"
df_recebimento = requests.get(rota_recebimento, headers = headers).json()
df_recebimento = pd.DataFrame(df_recebimento)
#--------------------------------------TRATAMENTOS-----------------------------------------------
#TODO: Tratamento Protocolos
dim_protocolo = df_protocolo[[
    'id',
    'apelido_protocolo',
    'data_cadastro',
    'data_visita_selecao',
    'data_estimada_inicio',
    'data_finalizacao_esperada',
    'data_inicio_recrutamento',
    'data_fim_recrutamento',
    'aprovacao_anvisa_data',
    'aprovacao_conep_data',
    'aprovacao_cep_data',
    'data_ativacao_centro',
    'data_recebimento_contrato',
    'data_resposta_contrato',
    'data_aprovacao_contrato',
    'data_assinatura_contrato',
    'data_recebimento_orcamento',
    'data_resposta_orcamento',
    'data_aprovacao_orcamento',
    'data_submissao_regulatorio',
    'data_aprovacao_regulatorio',
    'data_primeira_inclusao',
    'data_ultima_atualizacao',
    'data_siv',
    'data_close_out',
    'meta_inclusao',
    'nu_meta_inclusao',
    'dados_co_centro',
    'status',
    'tipo_iniciativa',
    'nome_patrocinador',
    'status_contrato',
    'status_orcamento',
    'status_regulatorio',
    'dados_patrocinador',
    'dados_cro_responsavel',
    'dados_aprovacao_anvisa',
    'dados_aprovacao_conep',
    'dados_aprovacao_cep'
]]

extrair_ultima_info = [
    'dados_co_centro',
    'status',
    'tipo_iniciativa',
    'nome_patrocinador',
    'dados_patrocinador',
    'dados_cro_responsavel',
    'dados_aprovacao_anvisa',
    'dados_aprovacao_conep',
    'dados_aprovacao_cep',
]

for coluna in extrair_ultima_info:
    if coluna in dim_protocolo.columns:
        dim_protocolo.loc[:, coluna] = dim_protocolo[coluna].apply(extrair_ultima_informacao)
    else:
        print(f"A coluna '{coluna}' não existe no DataFrame.")
    
df_generica_limpo_contrato = df_generica_limpo.copy()
df_generica_limpo_orcamento = df_generica_limpo.copy()
df_generica_limpo_contrato.rename(columns={'id': 'status_contrato', 'ds_descricao': 'contrato_status'}, inplace=True)
df_generica_limpo_orcamento.rename(columns={'id': 'status_orcamento', 'ds_descricao': 'orcamento_status'}, inplace=True)
# print(df_generica_limpo_contrato.head())
# print(df_generica_limpo_orcamento.head())

# TODO: Merge Protocolo-Generica
dim_protocolo = dim_protocolo.merge(df_generica_limpo_contrato, on='status_contrato', how='left')
dim_protocolo = dim_protocolo.merge(df_generica_limpo_orcamento, on='status_orcamento', how='left')    

status_interesse = ['Visita de seguimento', 'Recrutamento aberto','Recrutamento Finalizado','Aguardando Ativação do Centro','Qualificado', 'Fase Contratual','Em apreciação Ética','Aprovado pelo CEP','Aguardando o Pacote Regulatório','Em qualificação']

dim_protocolo = dim_protocolo.query("status in @status_interesse")

colunas_data = ['data_cadastro',
    'data_visita_selecao',
    'data_estimada_inicio',
    'data_finalizacao_esperada',
    'data_inicio_recrutamento',
    'data_fim_recrutamento',
    'aprovacao_anvisa_data',
    'aprovacao_conep_data',
    'aprovacao_cep_data',
    'data_ativacao_centro',
    'data_recebimento_contrato',
    'data_resposta_contrato',
    'data_aprovacao_contrato',
    'data_assinatura_contrato',
    'data_recebimento_orcamento',
    'data_resposta_orcamento',
    'data_aprovacao_orcamento',
    'data_submissao_regulatorio',
    'data_aprovacao_regulatorio',
    'data_primeira_inclusao',
    'data_ultima_atualizacao',
    'data_siv',
    'data_close_out'
    ]

# Converte cada coluna de data separadamente para melhorar o desempenho
for coluna in colunas_data:
    dim_protocolo[coluna] = pd.to_datetime(dim_protocolo[coluna], errors='coerce').dt.tz_localize(None).dt.date
    
#----------------------------------------CONTRATOS-----------------------------------------------

#--------------------------CONTRATOS SEM DATA DE ASSINATURA---------------------------------------
# TODO: Contratos sem data de assinatura
contrato = dim_protocolo.copy()
contrato = contrato[['apelido_protocolo',
                     'dados_co_centro',
                     'nome_patrocinador',
                     'status',
                     'data_assinatura_contrato',
                     'contrato_status'
                     ]]

# filtro = contrato['data_assinatura_contrato'].isna() # Filtrando somente os contratos sem data de assinatura
# contrato_sem_data = contrato.loc[filtro,:] # Exibindo somente os contratos sem data de assinatura

# contratostatus = ['Assinado']
# contrato_sem_data = contrato_sem_data.query("contrato_status in @contratostatus")

contrato_sem_data = contrato[
    contrato['data_assinatura_contrato'].isna() &
    contrato['contrato_status'].isin(['Assinado'])
]

# contrato_sem_data_html = contrato_sem_data.to_html(index=False)

def filtrar_contratos_sem_data(dataframe):
    # Verificar se o DataFrame filtrado está vazio
    if dataframe.empty:
        return "Não há datas de contrato a serem inseridas."
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_formatado = dataframe.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_formatado.to_html(index=False)
    
# Usando a função
contrato_sem_data_html = filtrar_contratos_sem_data(contrato_sem_data)


def enviar_email():
    try:
        if "Não há datas de contrato" in contrato_sem_data_html:
            print("Nenhum contrato pendente para enviar.")
            return

        msg = MIMEMultipart("alternative")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = "Contratos assinados sem data de assinatura"
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>Contratos assinados sem data de assinatura</h2>
                {contrato_sem_data_html}
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print("E-mail de datas de contrato enviado com sucesso!")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email()


#--------------------------CONTRATOS FAZENDO ANIVERSÁRIO---------------------------------------
# TODO: Aniversário de contrato
contrato_assinado = dim_protocolo.copy()
contrato_assinado = contrato_assinado[['apelido_protocolo',
                     'dados_co_centro',
                     'nome_patrocinador',
                     'status',
                     'data_assinatura_contrato',
                     'contrato_status'
                     ]]

filtro = contrato_assinado['data_assinatura_contrato'].notna()
contrato_assinado = contrato_assinado.loc[filtro,:] 

contrato_assinado['data_assinatura_contrato'] = pd.to_datetime(contrato_assinado['data_assinatura_contrato']).dt.normalize()

# Definir o intervalo de anos para a comparação (por exemplo, últimos 3 anos)
anos_interesse = [datetime.now().year - i for i in range(0, 4)]


# Filtrar contratos assinados no mesmo mês do ano anterior
contrato_assinado_aniversario = contrato_assinado[
    (contrato_assinado['data_assinatura_contrato'].dt.month == mes_atual) & 
    (contrato_assinado['data_assinatura_contrato'].dt.year.isin(anos_interesse))
]

def filtrar_contratos_aniversario(dataframe, anos=3):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['data_assinatura_contrato'].notna(), :]
# Verificar se o DataFrame filtrado está vazio
    if contrato_assinado_aniversario.empty:
        return "Não há contratos que completam aniversário no mês atual nos anos especificados."
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_filtrado = contrato_assinado_aniversario.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_filtrado.to_html(index=False)

# Chamando a função
contrato_assinado_html = filtrar_contratos_aniversario(contrato_assinado, anos=3) 

def enviar_email_aniversario():
    try:
        if "Não há contratos que completam aniversário" in contrato_assinado_html:
            print("Nenhum contrato completando aniversário este mês.")
            return

        msg = MIMEMultipart("alternative")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = "Aniversário de contratos"
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>Contratos completando aniversário neste mês</h2>
                {contrato_assinado_html}
                <p>Eu vim para te mandar mensagens, mua ha ha</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print("E-mail de aniversário enviado com sucesso!")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_aniversario()


#--------------------------------------REGULATÓRIO-----------------------------------------------
#TODO: Submissão Regulatório
dim_regulatorio = dim_protocolo.copy()
dim_regulatorio = dim_regulatorio[[
    'apelido_protocolo',
    'dados_patrocinador',
    'dados_co_centro',
    'status',
    'data_submissao_regulatorio',
    'status_regulatorio'
]]

filtro = dim_regulatorio['data_submissao_regulatorio'].notna()
dim_regulatorio = dim_regulatorio.loc[filtro,:] 

dim_regulatorio['data_submissao_regulatorio'] = pd.to_datetime(dim_regulatorio['data_submissao_regulatorio']).dt.normalize()

df_generica_limpo_regulatorio = df_generica_limpo.copy()

df_generica_limpo_regulatorio.rename(columns={'id': 'status_regulatorio', 'ds_descricao': 'regulatorio_status'}, inplace=True)



# Merge Regulatório-Generica
dim_regulatorio = dim_regulatorio.merge(df_generica_limpo_regulatorio, on='status_regulatorio', how='left')
dim_regulatorio.drop(columns=['status_regulatorio'], inplace = True)
status_interesse = ['Aguardando Ativação do Centro',
       'Qualificado', 'Fase Contratual',
       'Em apreciação Ética', 'Aprovado pelo CEP',
       'Aguardando o Pacote Regulatório']

dim_regulatorio = dim_regulatorio.query("status in @status_interesse")

# Filtrar contratos assinados no mesmo mês do ano anterior
dim_regulatorio_aniversario = dim_regulatorio[
    (dim_regulatorio['data_submissao_regulatorio'].dt.month == mes_atual) 
]

apelidos_protocolo = dim_regulatorio_aniversario['apelido_protocolo'].tolist()
apelidos_protocolo_submissao_reg = ', '.join(apelidos_protocolo)
data_protocolo = dim_regulatorio_aniversario['data_submissao_regulatorio'].tolist()
data_protocolo_submissao_reg = ', '.join([data.strftime('%d/%m/%Y') for data in data_protocolo])


def filtrar_submissao_regulatorio(dataframe, anos=3):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['data_submissao_regulatorio'].notna(), :]
# Verificar se o DataFrame filtrado está vazio
    if dim_regulatorio_aniversario.empty:
        return "Nenhum protocolo submetido para avaliação regulatória"
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_filtrado = dim_regulatorio_aniversario.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_filtrado.to_html(index=False)

# Chamando a função
dim_regulatorio_aniversario_html = filtrar_submissao_regulatorio(dim_regulatorio_aniversario) 



def enviar_email_submissao_regulatorio():
    try:
        if "Nenhum protocolo submetido para avaliação regulatória" in dim_regulatorio_aniversario_html:
            print("Nenhum protocolo submetido para avaliação regulatória no período.")
            return

        msg = MIMEMultipart("alternative")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = f"Protocolo {apelidos_protocolo_submissao_reg} submetido para avaliação regulatória"
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>Protocolos Submetidos para avaliação regulatória </h2>
                <p> O protocolo {apelidos_protocolo_submissao_reg} foi submetido para avaliação regulatória na data {data_protocolo_submissao_reg} </p>
                <p>{dim_regulatorio_aniversario_html}</p>
                <p>Eu vim para te mandar mensagens, mua ha ha</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print("E-mail de submissao regulaória enviado com sucesso!")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_submissao_regulatorio()

#--------------------------------------REGULATÓRIO-----------------------------------------------
#TODO: Aprovação Regulatória

dim_regulatorio_aprovacao = dim_protocolo.copy()
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
    (dim_regulatorio_aprovacao['data_aprovacao_regulatorio'].dt.year == ano_atual) & 
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

#---------------------------VISITA DE ATIVAÇÃO DE CENTRO------------------------------------------
# TODO: Site Initiation Visit (SIV)

# Selecionando os dados
siv = df_protocolo.copy()
siv = siv[[
    'data_siv',
    'apelido_protocolo',
    'dados_co_centro',
    'dados_pi',
    'dados_coordenador',
    'dados_patrocinador',
    'dados_cro_responsavel',
    'dados_especialidade',
    'dados_status_protocolo'    
]]

# Tratamento das datas
siv['data_siv']= pd.to_datetime(siv['data_siv']).dt.tz_localize(None)
# Eliminando linhas vazia
siv = siv.dropna(subset=['data_siv'])

# Extraindo as informações dos dicionários 
colunas_a_extrair=[
    'dados_co_centro',
    'dados_pi',
    'dados_coordenador',
    'dados_patrocinador',
    'dados_cro_responsavel',
    'dados_especialidade',
    'dados_status_protocolo'
]

for coluna in colunas_a_extrair:
    siv[coluna] = siv[coluna].apply(extrair_ultima_informacao)
    
# Renomeando as colunas para composição da tabela final
siv.rename(columns={
    'data_siv': 'Data da SIV',
    'apelido_protocolo': 'Protocolo',
    'dados_co_centro':'Centro',
    'dados_pi': 'Investigador Principal',
    'dados_coordenador': 'Coordenador',
    'dados_patrocinador':'Patrocinador',
    'dados_cro_responsavel': 'CRO',
    'dados_especialidade': 'Especialidade',
    'dados_status_protocolo': 'Status do Protocolo',
    }, inplace=True)

# Aplicando filtro de período dos dados exibidos
siv = siv[
    (siv['Data da SIV'] > amanha) &
    (siv['Data da SIV'] <= proximas_duas_semanas)
].sort_values(by='Data da SIV', ascending = True)

# Período para titulo do email
if not siv.empty:
    siv_no_periodo_min = siv['Data da SIV'].min().strftime('%d/%m/%Y')
    siv_no_periodo_max = siv['Data da SIV'].max().strftime('%d/%m/%Y')
else:
    siv_no_periodo_min = None
    siv_no_periodo_max = None
    
subject_email =(
   f'SiV agendada na data {siv_no_periodo_min}'
   if siv_no_periodo_min == siv_no_periodo_max
   else f'SiVs agendadas nas datas {siv_no_periodo_min} e {siv_no_periodo_max}'
)

# Função para criar a tabela do corpo do email 
def filtrar_siv(dataframe, anos=3):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['Data da SIV'].notna(), :]
# Verificar se o DataFrame filtrado está vazio
    if siv.empty:
        return "Nenhum participante finalizou o estudo ou o tratamento"
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_filtrado = siv.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_filtrado.to_html(index=False)

# Chamando a função
siv_html = filtrar_siv(siv)

# Função de envio do e-mail
def enviar_email_siv():
    try:
        if siv.empty:
            print("Nada a declarar sobre alteração de status de participantes")
            return

        msg = MIMEMultipart("alternative")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = subject_email
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>No período entre {siv_no_periodo_min} e {siv_no_periodo_max} foram agendadas as seguintes SIVs</h2>
                <p>{siv_html}</p>
                <p>Eu vim para te mandar mensagens, mua ha ha</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print(f"SIVs agendadas entre {siv_no_periodo_min} e {siv_no_periodo_max}")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_siv()



#------------------------------VISITA DE ENCERRAMENTO----------------------------------------------
#TODO  Close-Out Visit (COV)
# SELECIONANDO OS DADOS
cov = df_protocolo.copy()
cov = cov[[
    'data_close_out',
    'apelido_protocolo',
    'dados_co_centro',
    'dados_pi',
    'dados_coordenador',
    'dados_patrocinador',
    'dados_cro_responsavel',
    'dados_especialidade',
    'dados_status_protocolo'    
]]

# TRATAMENTO DA COLUNA DATAS
cov['data_close_out']= pd.to_datetime(cov['data_close_out']).dt.tz_localize(None)

#ELIMINANDO LINHAS NULAS
cov = cov.dropna(subset=['data_close_out'])

# EXTRAINDO DADOS DOS DICIONÁRIOS
colunas_a_extrair=[
    'dados_co_centro',
    'dados_pi',
    'dados_coordenador',
    'dados_patrocinador',
    'dados_cro_responsavel',
    'dados_especialidade',
    'dados_status_protocolo'
]

for coluna in colunas_a_extrair:
    cov[coluna] = cov[coluna].apply(extrair_ultima_informacao)

# RENOMEANDO AS COLUNAS PARA A TABELA FINAL
cov.rename(columns={
    'data_close_out': 'Data da COV',
    'apelido_protocolo': 'Protocolo',
    'dados_co_centro':'Centro',
    'dados_pi': 'Investigador Principal',
    'dados_coordenador': 'Coordenador',
    'dados_patrocinador':'Patrocinador',
    'dados_cro_responsavel': 'CRO',
    'dados_especialidade': 'Especialidade',
    'dados_status_protocolo': 'Status do Protocolo',
    }, inplace=True)

# SELECIONANDO O PERÍODO
cov = cov[
    (cov['Data da COV'] > amanha) &
    (cov['Data da COV'] <= proximas_duas_semanas)
].sort_values(by='Data da COV', ascending = True)

# SELECIONANDO A PRIMEIRA E ULTIMA DATA DO PERÍODO
# Primeira período para titulo do email
if not cov.empty:
    cov_no_periodo_min = cov['Data da COV'].min().strftime('%d/%m/%Y')
    cov_no_periodo_max = cov['Data da COV'].max().strftime('%d/%m/%Y')
else:
    cov_no_periodo_min = None
    cov_no_periodo_max = None

# CONFIGURANDO O TÍTULO DO E-MAIL
subject_email =(
   f'COV agendada na data {cov_no_periodo_min}'
   if cov_no_periodo_min == cov_no_periodo_max
   else f'covs agendadas nas datas {cov_no_periodo_min} e {cov_no_periodo_max}'
)

# Função para criar a tabela do corpo do email 
def filtrar_cov(dataframe, anos=3):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['Data da COV'].notna(), :]
# Verificar se o DataFrame filtrado está vazio
    if cov.empty:
        return "Nenhum participante finalizou o estudo ou o tratamento"
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_filtrado = cov.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_filtrado.to_html(index=False)

# Chamando a função
cov_html = filtrar_cov(cov)

# Função de envio do e-mail
def enviar_email_cov():
    try:
        if cov.empty:
            print("NENHUMA COV AGENDADA PARA AS PROXIMAS SEMANAS")
            return

        msg = MIMEMultipart("alternative")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = subject_email
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>No período entre {cov_no_periodo_min} e {cov_no_periodo_max} foram agendadas as seguintes COVs</h2>
                <p>{cov_html}</p>
                <p>Eu vim para te mandar mensagens, mua ha ha</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print(f"covs agendadas entre {cov_no_periodo_min} e {cov_no_periodo_max}")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_cov()


#-----------------------------Assinatura do primeiro TCLE------------------------------------------
#TODO  Assinatura do primeiro TCLE
# PARTE 1 - CENTROS
centros = dim_protocolo.copy()

centros = centros[[
    'id',
    'dados_co_centro'
]]
centros = centros.rename(columns={
    'id': 'id_protocolo',
    'dados_co_centro': 'Centro'
})
# PARTE 2 - PARTICIPANTES
dim_participantes = df_participantes.copy()
dim_participantes = dim_participantes[[
    'id',
    'numero_de_randomizacao',
    'Status',
    'co_protocolo',
    'dados_protocolo']]
dim_participantes.rename(columns={
    'id': 'id_participante',
    'numero_de_randomizacao':'Participante',
    'Status':'Status',
    'co_protocolo':'id_protocolo',
    'dados_protocolo': 'Protocolo'
}, inplace=True)


ultima_infomacao_pct = [
    'Status',
    'Protocolo'
]
for coluna in ultima_infomacao_pct:
    dim_participantes[coluna] = dim_participantes[coluna].apply(extrair_ultima_informacao)
    
# PARTE 3 - PROCEDIMENTOS
dim_visita_procedimentos = df_visita_procedimentos.copy()
dim_visita_procedimentos=dim_visita_procedimentos[[
                                                 'dados_participante_visita.co_participante',
                                                 'dados_protocolo_procedimento.nome_procedimento_estudo',
                                                 'data_executada'
                                                 ]]
dim_visita_procedimentos.rename(columns={
    'dados_participante_visita.co_participante': 'id_participante',
    'dados_protocolo_procedimento.nome_procedimento_estudo': 'Procedimento',
    'data_executada': 'Data Executada'
}, inplace = True)

dim_visita_procedimentos['Data Executada']= pd.to_datetime(dim_visita_procedimentos['Data Executada'])

dim_participantes = dim_participantes.merge(dim_visita_procedimentos, how = 'left', on='id_participante')
dim_participantes = dim_participantes.merge(centros, how = 'left', on='id_protocolo')

colunas_data = [
    'Data Executada'
]

dim_participantes[colunas_data]=dim_participantes[colunas_data].apply(lambda x: pd.to_datetime(x, errors = 'coerce').dt.tz_localize(None).dt.date)
dim_participantes['Data Executada']= pd.to_datetime(dim_participantes['Data Executada'])

termos = [
    'tcle', 
    'Termo e Consentimento' ,
    'Termo de Consentimento',
    'Consentimento',
    'Assentimento'
    ]
expressao = '|'.join(termos)

dim_participantes = dim_participantes[dim_participantes['Procedimento'].str.contains(expressao, regex=True, na=False, case=False)]
# Encontrando o primeiro indivíduo que realizou cada procedimento por protocolo
primeiro_tcle_assinado = dim_participantes.loc[dim_participantes.groupby(['Protocolo', 'Procedimento'])['Data Executada'].idxmin()]
    
# # Filtrar para o primeiro TCLE de cada protocolo assinado nas duas ultimas semanas
primeiro_tcle_assinado = primeiro_tcle_assinado[
    (primeiro_tcle_assinado['Data Executada'] >= duas_ultimas_semanas)
]

nome_protocolo_primeiro_tcle_assinado = primeiro_tcle_assinado['Protocolo'].tolist()
primeiro_tcle_assinado_reg = ', '.join(nome_protocolo_primeiro_tcle_assinado)
data_primeiro_tcle_assinado = primeiro_tcle_assinado['Data Executada'].tolist()
data_protocolo_aprovacao_reg = ', '.join([data.strftime('%d/%m/%Y') for data in data_primeiro_tcle_assinado])

if not primeiro_tcle_assinado.empty:
    tcle_info = f"<p> Protocolo {primeiro_tcle_assinado} aprovado na avaliação regulatória na data de {data_protocolo_aprovacao_reg}"
else:
    tcle_info = ""


def filtrar_primeiro_tcle_assinado(dataframe, anos=3):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['Data Executada'].notna(), :]
# Verificar se o DataFrame filtrado está vazio
    if primeiro_tcle_assinado.empty:
        return "Nenhum TCLE assinado até o presente momento"
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_filtrado = primeiro_tcle_assinado.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_filtrado.to_html(index=False)

# Chamando a função
primeiro_tcle_assinadoo_html = filtrar_primeiro_tcle_assinado(primeiro_tcle_assinado) 



def enviar_email_primeiro_tcle_assinado():
    try:
        if primeiro_tcle_assinado.empty:
            print("Nenhum estudo com seu primeiro TCLE assinado no período")
            return

        msg = MIMEMultipart("alternative")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = f"Protocolo {primeiro_tcle_assinado_reg} teve seu primeiro TCLE Assinado na data {data_protocolo_aprovacao_reg}"
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>Protocolos aprovados pelo órgão regulatório </h2>
                
                <p>{primeiro_tcle_assinadoo_html}</p>
                <p>Eu vim para te mandar mensagens, mua ha ha</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print("Encontrados estudos com o primeiro TCLE Assinado")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_primeiro_tcle_assinado()

#------------------------Relato de Evento Adverso/ Evento Adverso Sério---------------------------
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
                {ea_info}
                <p style="overflow-x:auto;">{dim_evento_adverso_html}</p>
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

#------------------------Primeira visita do estudo---------------------------
#TODO: Primeira Visita do Primeiro Paciente realizada (FPFV)
# Obtendo os dados da agenda dos participantes
fato_agenda = df_participante_visita.copy()

# Tratamento dos dados 
## selecionando os campos de interesse da agenda do participante
fato_agenda = fato_agenda[[
    'id',
    'co_participante',
    'nome_tarefa',
    'data_realizada',
    'dados_status',
]]

## Renomeando as colunas para facil visualização no dataframe
fato_agenda.rename(columns = {
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
fato_agenda = fato_agenda.merge(dim_participantes, how = 'left', on='id_participante')
fato_agenda = fato_agenda.merge(centros, how = 'left', on='id_protocolo')

# Extraindo as informações dos dicionários
colunas_a_extrair = [
    'Status da visita',
    'Protocolo',
    'Status do Participante',
    'Centro'
   
]
for coluna in colunas_a_extrair:
    fato_agenda[coluna] = fato_agenda[coluna].apply(extrair_ultima_informacao)
    
# Tratamento da coluna de datas
fato_agenda['Data da visita realizada']= pd.to_datetime(fato_agenda['Data da visita realizada']).dt.tz_localize(None)

# tratando valores faltantes
fato_agenda['Protocolo']=fato_agenda['Protocolo'].fillna('Indefinido')
fato_agenda['Centro']=fato_agenda['Centro'].fillna('Indefinido')
fato_agenda = fato_agenda.dropna(subset=['Data da visita realizada'])

fato_agenda = fato_agenda[[
    'Protocolo',
    'Centro',
    'Participante',
    'Status do Participante',
    'visita',
    'Status da visita',
    'Data da visita realizada'
]]

# Primeira visita do estudo
primeira_visita = fato_agenda.loc[fato_agenda.groupby(['Protocolo', 'Centro'])['Data da visita realizada'].idxmin()]


# Selecionando o período a ser notificado
primeira_visita = primeira_visita[
    (primeira_visita['Data da visita realizada'] >= ultima_semana)
]

#Configurações para o E-MAIL
# Filtrando os nomes de estudos que irão compor o titulo do e-mail
protocolo_primeira_visita = primeira_visita['Protocolo'].tolist()
protocolo_primeira_visita_reg = ', '.join(protocolo_primeira_visita)

# Filtrando as datas das visitas que irão compor o titulo do e-mail
data_primeira_visita = primeira_visita['Data da visita realizada'].tolist()
data_primeira_visita_reg = ', '.join([data.strftime('%d/%m/%Y') for data in data_primeira_visita])

# Texto do corpo do e-mail
if not primeira_visita.empty:
    primeira_visita_info = f"<p> Relato de evento adverso: Protocolo {protocolo_primeira_visita_reg}, Data: {data_primeira_visita_reg}"
else:
    primeira_visita_info = ""

# Função para criar a tabela do corpo do email 
def filtrar_primeira_visita(dataframe, anos=3):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['Data da visita realizada'].notna(), :]
# Verificar se o DataFrame filtrado está vazio
    if primeira_visita.empty:
        return "Visitas não notificadas"
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_filtrado = primeira_visita.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_filtrado.to_html(index=False)

# Chamando a função
primeira_visita_html = filtrar_primeira_visita(primeira_visita)

# Função de envio do e-mail
def enviar_email_primeira_visita():
    try:
        if primeira_visita.empty:
            print("Sem relato de primeira visita")
            return

        msg = MIMEMultipart("alternative")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = f"O Estudo {protocolo_primeira_visita_reg} teve sua primeira visita em {data_primeira_visita_reg}"
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>Eventos adversos relatados </h2>
                {primeira_visita_info}
                <p>{primeira_visita_html}</p>
                <p>Eu vim para te mandar mensagens, mua ha ha</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print("Relatos de primeira visita")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_primeira_visita()

#------------------------Visitas realizadas na semana---------------------------
#TODO: Visitas realizadas na semana
visitas_realizadas = df_participante_visita.copy()

# Tratamento dos dados 
## selecionando os campos de interesse da agenda do participante
visitas_realizadas = visitas_realizadas[[
    'id',
    'co_participante',
    'nome_tarefa',
    'data_realizada',
    'dados_status',
]]

## Renomeando as colunas para facil visualização no dataframe
visitas_realizadas.rename(columns = {
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
visitas_realizadas = visitas_realizadas.merge(dim_participantes, how = 'left', on='id_participante')
visitas_realizadas = visitas_realizadas.merge(centros, how = 'left', on='id_protocolo')

# Extraindo as informações dos dicionários
colunas_a_extrair = [
    'Status da visita',
    'Protocolo',
    'Status do Participante',
    'Centro'
   
]
for coluna in colunas_a_extrair:
    visitas_realizadas[coluna] = visitas_realizadas[coluna].apply(extrair_ultima_informacao)
    
# Tratamento da coluna de datas
visitas_realizadas['Data da visita realizada']= pd.to_datetime(visitas_realizadas['Data da visita realizada']).dt.tz_localize(None)

# tratando valores faltantes
visitas_realizadas['Protocolo']=visitas_realizadas['Protocolo'].fillna('Indefinido')
visitas_realizadas['Centro']=visitas_realizadas['Centro'].fillna('Indefinido')
visitas_realizadas = visitas_realizadas.dropna(subset=['Data da visita realizada'])

visitas_realizadas = visitas_realizadas[[
    'Protocolo',
    'Centro',
    'Participante',
    'Status do Participante',
    'visita',
    'Status da visita',
    'Data da visita realizada'
]]

# Selecionando o período a ser notificado
visitas_realizadas = visitas_realizadas[
    (visitas_realizadas['Data da visita realizada'] >= ultima_semana)
]

# Primeira período para titulo do email
visitas_realizadas_no_periodo_min = visitas_realizadas['Data da visita realizada'].min().strftime('%d/%m/%Y')

visitas_realizadas_no_periodo_max =visitas_realizadas['Data da visita realizada'].max().strftime('%d/%m/%Y')

# Função para criar a tabela do corpo do email 
def filtrar_visitas_realizadas(dataframe, anos=3):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['Data da visita realizada'].notna(), :]
# Verificar se o DataFrame filtrado está vazio
    if visitas_realizadas.empty:
        return "Visitas não notificadas"
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_filtrado = visitas_realizadas.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_filtrado.to_html(index=False)

# Chamando a função
visitas_realizadas_html = filtrar_visitas_realizadas(visitas_realizadas)

# Função de envio do e-mail
def enviar_email_visitas_realizadas():
    try:
        if visitas_realizadas.empty:
            print("Sem relato de visitas realizadas na semana")
            return

        msg = MIMEMultipart("alternative")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = f"Visitas realizadas entre {visitas_realizadas_no_periodo_min} e {visitas_realizadas_no_periodo_max}"
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>Visitas realizadas entre {visitas_realizadas_no_periodo_min} e {visitas_realizadas_no_periodo_max}</h2>
                <p>{visitas_realizadas_html}</p>
                <p>Eu vim para te mandar mensagens, mua ha ha</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print(f"Visitas realizadas entre {visitas_realizadas_no_periodo_min} e {visitas_realizadas_no_periodo_max}")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_visitas_realizadas()

#------------------------Visitas previstas para os próximos dias---------------------------
#TODO: Próximas visitas
proximas_visitas = df_participante_visita.copy()

# Tratamento dos dados 
## selecionando os campos de interesse da agenda do participante
proximas_visitas = proximas_visitas[[
    'id',
    'co_participante',
    'nome_tarefa',
    'data_estimada',
    'dados_status',
]]

## Renomeando as colunas para facil visualização no dataframe
proximas_visitas.rename(columns = {
    'id':'id_agenda',
    'co_participante':'id_participante',
    'nome_tarefa':'visita',
    'data_estimada':'Data Prevista',
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
proximas_visitas['Data Prevista']= pd.to_datetime(proximas_visitas['Data Prevista']).dt.tz_localize(None)

# tratando valores faltantes
proximas_visitas['Protocolo']=proximas_visitas['Protocolo'].fillna('Indefinido')
proximas_visitas['Centro']=proximas_visitas['Centro'].fillna('Indefinido')
proximas_visitas = proximas_visitas.dropna(subset=['Data Prevista'])

proximas_visitas = proximas_visitas[[
    'Protocolo',
    'Centro',
    'Participante',
    'Status do Participante',
    'visita',
    'Status da visita',
    'Data Prevista'
]]

# Selecionando o período a ser notificado
proximas_visitas = proximas_visitas[
    (proximas_visitas['Data Prevista'] > amanha) & 
    (proximas_visitas['Data Prevista']<= proxima_semana)
].sort_values(by='Data Prevista', ascending = True)

proximas_visitas_no_periodo_min = proximas_visitas['Data Prevista'].min().strftime('%d/%m/%Y')

proximas_visitas_no_periodo_max =proximas_visitas['Data Prevista'].max().strftime('%d/%m/%Y')

# Função para criar a tabela do corpo do email 
def filtrar_proximas_visitas(dataframe):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['Data Prevista'].notna(), :]
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
        msg['Subject'] = f"Agenda Polotrial - Proximas visitas. Período: {proximas_visitas_no_periodo_min} - {proximas_visitas_no_periodo_max}"
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>Visitas a serem realizadas entre {proximas_visitas_no_periodo_min} e {proximas_visitas_no_periodo_max}</h2>
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
        print(f"Visitas a serem realizadas entre {proximas_visitas_no_periodo_min} e {proximas_visitas_no_periodo_max}")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_proximas_visitas()

#-------------------------------Ultima visita do estudo---------------------------------------
#TODO: EOS ou EOT realizado

eos_eot = df_participante_visita.copy()

# Tratamento dos dados 
## selecionando os campos de interesse da agenda do participante
eos_eot = eos_eot[[
    'id',
    'co_participante',
    'nome_tarefa',
    'data_realizada',
    'dados_status',
]]

## Renomeando as colunas para facil visualização no dataframe
eos_eot.rename(columns = {
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
eos_eot = eos_eot.merge(dim_participantes, how = 'left', on='id_participante')
eos_eot = eos_eot.merge(centros, how = 'left', on='id_protocolo')

# Extraindo as informações dos dicionários
colunas_a_extrair = [
    'Status da visita',
    'Protocolo',
    'Status do Participante',
    'Centro'
   
]
for coluna in colunas_a_extrair:
    eos_eot[coluna] = eos_eot[coluna].apply(extrair_ultima_informacao)
    
# Tratamento da coluna de datas
eos_eot['Data da visita realizada']= pd.to_datetime(eos_eot['Data da visita realizada']).dt.tz_localize(None)

# tratando valores faltantes
eos_eot['Protocolo']=eos_eot['Protocolo'].fillna('Indefinido')
eos_eot['Centro']=eos_eot['Centro'].fillna('Indefinido')
eos_eot = eos_eot.dropna(subset=['Data da visita realizada'])

eos_eot = eos_eot[[
    'Protocolo',
    'Centro',
    'Participante',
    'Status do Participante',
    'visita',
    'Status da visita',
    'Data da visita realizada'
]]

filtros = ['EOS', 'EOT']

eos_eot = eos_eot[
    (eos_eot['Status do Participante'].isin(filtros)) &
    (eos_eot['Data da visita realizada'] >= duas_ultimas_semanas)
]

eos_eot = eos_eot.sort_values(
    by=[
        'Protocolo',
        'Centro',
        'Participante',
        'Data da visita realizada'
    ], ascending=False
)

eos_eot=eos_eot.groupby(
    [
        'Protocolo',
        'Centro',
        'Participante'
     ]
).first().reset_index()

# Primeira período para titulo do email
if not eos_eot.empty:
    eos_eot_no_periodo_min = eos_eot['Data da visita realizada'].min().strftime('%d/%m/%Y')
    eos_eot_no_periodo_max = eos_eot['Data da visita realizada'].max().strftime('%d/%m/%Y')
else:
    eos_eot_no_periodo_min = None
    eos_eot_no_periodo_max = None

# Função para criar a tabela do corpo do email 
def filtrar_eos_eot(dataframe, anos=3):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['Data da visita realizada'].notna(), :]
# Verificar se o DataFrame filtrado está vazio
    if eos_eot.empty:
        return "Nenhum participante finalizou o estudo ou o tratamento"
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_filtrado = eos_eot.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_filtrado.to_html(index=False)

# Chamando a função
eos_eot_html = filtrar_eos_eot(eos_eot)

# Função de envio do e-mail
def enviar_email_eos_eot():
    try:
        if eos_eot.empty:
            print("Nada a declarar sobre alteração de status de participantes")
            return

        msg = MIMEMultipart("alternative")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = f"Participantes que finalizaram o tratamento ou o Estudo entre {eos_eot_no_periodo_min} e {eos_eot_no_periodo_max}"
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>No período entre {eos_eot_no_periodo_min} e {eos_eot_no_periodo_max} os seguintes participantes finalizaram o tratamento ou o estudo</h2>
                <p>{eos_eot_html}</p>
                <p>Eu vim para te mandar mensagens, mua ha ha</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print(f"EOS/EOT entre {eos_eot_no_periodo_min} e {eos_eot_no_periodo_max}")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_eos_eot()

# TODO: Alteração de protocolos
#Acessando as bases de dados
flowchart = df_flowchart.copy()

#Protocolo
dim_protocolo_flowchart = df_protocolo[[
    'id',
    'apelido_protocolo',
    'dados_co_centro',
    'nome_patrocinador',
    'PessoaPI',
    'status'
    
    ]].copy()

colunas_a_extrair=[
    'dados_co_centro',
    'PessoaPI',
    'status',
    'nome_patrocinador'
]

for coluna in colunas_a_extrair:
    dim_protocolo_flowchart[coluna] = dim_protocolo_flowchart[coluna].apply(extrair_ultima_informacao)

dim_protocolo_flowchart.rename(columns={
    'id':'co_protocolo',
    'apelido_protocolo': 'Protocolo',
    'dados_co_centro': 'Centro',
    'nome_patrocinador': 'Patrocinador',
    'PessoaPI': 'Investigador Principal',
    'status': 'Status'
    
    }, inplace=True)

dim_pessoas = df_pessoas[[
    'id',
    'ds_nome',
    'dados_co_tipo_gn'
    ]].copy()

colunas_a_extrair=[
    'dados_co_tipo_gn'
]

for coluna in colunas_a_extrair:
    dim_pessoas[coluna] = dim_pessoas[coluna].apply(extrair_ultima_informacao)

dim_pessoas.rename(columns={
    'id':'aprovador',
    'ds_nome':'Nome aprovador',
    'dados_co_tipo_gn':'Função'
    
    }, inplace=True)

# MERGE
flowchart = flowchart.merge(dim_protocolo_flowchart, on='co_protocolo', how='left')
flowchart = flowchart.merge(dim_pessoas, on='aprovador', how='left')

# Tratamento
flowchart.rename(columns={
    'data_aprovacao': 'Data de aprovação do Flowchart'
    
    }, inplace=True)

flowchart=flowchart[[
    'Data de aprovação do Flowchart',
    'Protocolo',
    'Centro',
    'Patrocinador',
    'Investigador Principal',
    'Status',
    'Nome aprovador',
    'Função'
]]

flowchart=flowchart.dropna(subset=['Data de aprovação do Flowchart', 'Protocolo'])
flowchart['Data de aprovação do Flowchart']= pd.to_datetime(flowchart['Data de aprovação do Flowchart']).dt.tz_localize(None)

flowchart = flowchart[
    flowchart['Data de aprovação do Flowchart'] > ontem
].sort_values(by='Data de aprovação do Flowchart', ascending = True)

# Primeira período para titulo do email
if not flowchart.empty:
    flowchart_no_periodo_min = flowchart['Data de aprovação do Flowchart'].min().strftime('%d/%m/%Y')
    flowchart_no_periodo_max = flowchart['Data de aprovação do Flowchart'].max().strftime('%d/%m/%Y')
else:
    flowchart_no_periodo_min = None
    flowchart_no_periodo_max = None

subject_email =(
   f'Flowchart aprovado em {flowchart_no_periodo_min}'
   if flowchart_no_periodo_min == flowchart_no_periodo_max
   else f'Flowcharts aprovados em: {flowchart_no_periodo_min} e {flowchart_no_periodo_max}'
)

# Função para criar a tabela do corpo do email 
def filtrar_flowchart(dataframe):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['Data de aprovação do Flowchart'].notna(), :]
# Verificar se o DataFrame filtrado está vazio
    if flowchart.empty:
        return "Nenhum participante finalizou o estudo ou o tratamento"
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_filtrado = flowchart.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_filtrado.to_html(index=False)

# Chamando a função
flowchart_html = filtrar_flowchart(flowchart)

# Função de envio do e-mail
def enviar_email_flowchart():
    try:
        if flowchart.empty:
            print("NENHUMA FLOWCHART APROVADO NO PERÍODO")
            return

        msg = MIMEMultipart("alternative")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = subject_email
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>No período entre {flowchart_no_periodo_min} e {flowchart_no_periodo_max} foram aprovados os flowcharts</h2>
                <p>{flowchart_html}</p>
                <p>Eu vim para te mandar mensagens, mua ha ha</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print(f"flowcharts aprovados entre {flowchart_no_periodo_min} e {flowchart_no_periodo_max}")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_flowchart()



# TODO: Protocolos sem moeda

dim_protocolo_financeiro = df_protocolo_financeiro[[
    'id',
    'co_protocolo',
    'dados_protocolo',
    'dados_moeda']].copy()

colunas_a_extrair=[
    'dados_protocolo',
    'dados_moeda'
]

for coluna in colunas_a_extrair:
    dim_protocolo_financeiro[coluna] = dim_protocolo_financeiro[coluna].apply(extrair_ultima_informacao)

dim_protocolo_financeiro.rename(columns={
    'id':'id_protocolo_financeiro',
    'dados_protocolo': 'Protocolo',
    'dados_moeda': 'Moeda'
}, inplace=True)

dim_protocolo = df_protocolo[[
    'id',
    'dados_co_centro',
    'nome_patrocinador',
    'PessoaPI',
    'status',
    'data_cadastro'
    
    ]].copy()

colunas_a_extrair=[
    'dados_co_centro',
    'PessoaPI',
    'status',
    'nome_patrocinador'
]

for coluna in colunas_a_extrair:
    dim_protocolo[coluna] = dim_protocolo[coluna].apply(extrair_ultima_informacao)

dim_protocolo.rename(columns={
    'id':'co_protocolo',
    'dados_co_centro': 'Centro',
    'nome_patrocinador': 'Patrocinador',
    'PessoaPI': 'Investigador Principal',
    'status': 'Status',
    'data_cadastro': 'Data de Cadastro'
    
    }, inplace=True)

dim_protocolo_financeiro = dim_protocolo_financeiro.merge(dim_protocolo, on='co_protocolo', how='left')
dim_protocolo_financeiro=dim_protocolo_financeiro.drop(columns = ['id_protocolo_financeiro','co_protocolo'])

status  = [
    'Concluído',
    'Visita de seguimento',
    'Recrutamento aberto',
    'Recrutamento Finalizado', 
    'Aguardando Ativação do Centro',
    'Qualificado',
    'Aprovado pelo CEP',
    'Fase Contratual',
    ]


dim_protocolo_financeiro=dim_protocolo_financeiro[dim_protocolo_financeiro['Status'].isin(status)].sort_values(by='Data de Cadastro', ascending = True)
dim_protocolo_financeiro['Data de Cadastro']= pd.to_datetime(dim_protocolo_financeiro['Data de Cadastro']).dt.tz_localize(None)
dim_protocolo_financeiro=dim_protocolo_financeiro[dim_protocolo_financeiro['Moeda'].isnull()]
contagem = dim_protocolo_financeiro['Protocolo'].value_counts()
def figura_barra_sem_moeda():
    fig, ax = plt.subplots()

    # Criar gráfico de barra horizontal com os dados da variável 'contagem'
    ax.barh(contagem.index, contagem.values)
    
    # Salva a figura em um buffer em memória
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Fecha a figura para liberar memória
    plt.close(fig)

    return buf

# Primeira período para titulo do email
if not dim_protocolo_financeiro.empty:
    dim_protocolo_financeiro_min = dim_protocolo_financeiro['Data de Cadastro'].min().strftime('%d/%m/%Y')
    dim_protocolo_financeiro_max = dim_protocolo_financeiro['Data de Cadastro'].max().strftime('%d/%m/%Y')
else:
    dim_protocolo_financeiro_min = None
    dim_protocolo_financeiro_max = None
    
subject_email =(
   f'Protocolos cadastrado em {dim_protocolo_financeiro_min} não contem moeda cadastrada'
   if dim_protocolo_financeiro_min == dim_protocolo_financeiro_max
   else f'Os protocolos cadastrados entre {dim_protocolo_financeiro_min} e {dim_protocolo_financeiro_max} não apresentam moeda cadastrada'
)
subject_email
# Função para criar a tabela do corpo do email 
def filtrar_protocolo_financeiro(dataframe, anos=3):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['Data de Cadastro'].notna(), :]
# Verificar se o DataFrame filtrado está vazio
    if dim_protocolo_financeiro.empty:
        return "Nenhum estudos cadastrado está sem a moeda"
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_filtrado = dim_protocolo_financeiro.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_filtrado.to_html(index=False)

# Chamando a função
dim_protocolo_financeiro_html = filtrar_protocolo_financeiro(dim_protocolo_financeiro)

# Função de envio do e-mail
def enviar_email_protocolos_sem_moeda():
    try:
        if dim_protocolo_financeiro.empty:
            print("Todos os protocolos estão com moeda cadastrada")
            return
        
        # Gerar o gráfico e obter o buffer da imagem
        imagem_buffer = figura_barra_sem_moeda()

        msg = MIMEMultipart("related")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = subject_email
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>Os protocolos cadastrados entre {dim_protocolo_financeiro_min} e {dim_protocolo_financeiro_max} não apresentam moeda cadastrada</h2>
                <p>{dim_protocolo_financeiro_html}</p>
                <img src="cid:imagem1">
                <p>Eu vim para te mandar mensagens, mua ha ha</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))
        
        # Anexar a imagem ao e-mail
        imagem_anexo = MIMEImage(imagem_buffer.read(), subtype='png')
        imagem_anexo.add_header('Content-ID', '<imagem1>')
        msg.attach(imagem_anexo)
        
        # Enviar o e-mail
        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print(f"Os protocolos cadastrados entre {dim_protocolo_financeiro_min} e {dim_protocolo_financeiro_max} não apresentam moeda cadastrada")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_protocolos_sem_moeda()

# TODO: Protocolos sem centro
sem_centro = df_protocolo[[
    'apelido_protocolo',
    'dados_co_centro',
    'nome_patrocinador',
    'PessoaPI',
    'status',
    'data_cadastro'
    
    ]].copy()

colunas_a_extrair=[
    'dados_co_centro',
    'PessoaPI',
    'status',
    'nome_patrocinador'
]

for coluna in colunas_a_extrair:
    sem_centro[coluna] = sem_centro[coluna].apply(extrair_ultima_informacao)

sem_centro.rename(columns={
    'apelido_protocolo':'Protocolo',
    'dados_co_centro': 'Centro',
    'nome_patrocinador': 'Patrocinador',
    'PessoaPI': 'Investigador Principal',
    'status': 'Status',
    'data_cadastro': 'Data de Cadastro'
    
    }, inplace=True)
status  = [
    'Concluído',
    'Visita de seguimento',
    'Recrutamento aberto',
    'Recrutamento Finalizado', 
    'Aguardando Ativação do Centro',
    'Qualificado',
    'Aprovado pelo CEP',
    'Fase Contratual',
    ]


sem_centro=sem_centro[sem_centro['Status'].isin(status)].sort_values(by='Data de Cadastro', ascending = True)


sem_centro['Data de Cadastro']= pd.to_datetime(sem_centro['Data de Cadastro']).dt.tz_localize(None)

sem_centro=sem_centro[sem_centro['Centro'].isnull()]

# Primeira período para titulo do email
if not sem_centro.empty:
    sem_centro_min = sem_centro['Data de Cadastro'].min().strftime('%d/%m/%Y')
    sem_centro_max = sem_centro['Data de Cadastro'].max().strftime('%d/%m/%Y')
else:
    sem_centro_min = None
    sem_centro_max = None
    
subject_email =(
   f'Todos os protocolos cadastrados tem o campo "Centro" preenchido'
   if sem_centro_min==None
   else f'Protocolos cadastrado em {sem_centro_min} não contem o centro cadastrado'
      if sem_centro_min == sem_centro_max
      else f'Os protocolos cadastrados entre {sem_centro_min} e {sem_centro_max} não apresentam centro cadastrado'
)
# Função para criar a tabela do corpo do email 
def filtrar_protocolo_sem_centro(dataframe, anos=3):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['Data de Cadastro'].notna(), :]
# Verificar se o DataFrame filtrado está vazio
    if sem_centro.empty:
        return "Nenhum estudos cadastrado está sem a moeda"
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_filtrado = sem_centro.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_filtrado.to_html(index=False)

# Chamando a função
sem_centro_html = filtrar_protocolo_sem_centro(sem_centro)

# Função de envio do e-mail
def enviar_email_protocolos_sem_centro():
    try:
        if sem_centro.empty:
            print("Todos os protocolos estão com centro cadastrada")
            return
        
        

        msg = MIMEMultipart("related")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = subject_email
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>Os protocolos cadastrados entre {sem_centro_min} e {sem_centro_max} não apresentam centro cadastrado</h2>
                <p>{sem_centro_html}</p>
                <p>Eu vim para te mandar mensagens, mua ha ha</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))
        

        
        # Enviar o e-mail
        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print(f"Os protocolos cadastrados entre {sem_centro_min} e {sem_centro_max} não apresentam centro cadastrado")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_protocolos_sem_centro()


# TODO: Invoices/NFs duplicadas

#acesso à base de dados
dim_recebimentos = df_recebimento.copy()

# Extraindo informações de dicionários
colunas_a_extrair_recebimento=[
    'dados_protocolo',
    'dados_status_invoice',
    'dados_moeda'
]

for coluna in colunas_a_extrair_recebimento:
    dim_recebimentos[coluna] = dim_recebimentos[coluna].apply(extrair_ultima_informacao)

# dados de interesse    
dim_recebimentos=dim_recebimentos[[
    'id',
    'codigo_nota_fiscal',
    'data_emissao',
    'valor_enviado',
    'data_prevista_pagamento',
    'valor_recebido',
    'data_recebimento',
    'impostos_retidos_valor',
    'dados_protocolo',
    'dados_status_invoice',
    'dados_moeda'
]]

# endereçando o dataframe
dataframe_recebimento = "Recebimentos"
dim_recebimentos['Origem'] = dataframe_recebimento

# Primeiro Filtro
filtro = ['A emitir']
dim_recebimentos=dim_recebimentos[~dim_recebimentos['codigo_nota_fiscal'].isin(filtro)]

# Segundo Filtro
filtro = ['Cancelada']
dim_recebimentos=dim_recebimentos[~dim_recebimentos['dados_status_invoice'].isin(filtro)]

# Selecionando valores duplicados
valore_duplicados=dim_recebimentos['codigo_nota_fiscal'].duplicated(keep=False)
invoices_duplicadas=dim_recebimentos[valore_duplicados]

# Tratameto da coluna de datas
invoices_duplicadas['data_emissao']= pd.to_datetime(invoices_duplicadas['data_emissao']).dt.tz_localize(None)

# Classificando os dados em ordem crescente
invoices_duplicadas=invoices_duplicadas.sort_values(by='codigo_nota_fiscal', ascending = True)

# Períodos para titulo do email
if not invoices_duplicadas.empty:
    invoices_duplicadas_min = invoices_duplicadas['data_emissao'].min().strftime('%d/%m/%Y')
    invoices_duplicadas_max = invoices_duplicadas['data_emissao'].max().strftime('%d/%m/%Y')
else:
    invoices_duplicadas_min = None
    invoices_duplicadas_max = None

# Texto personalizado  
subject_email =(
   f'Não existem invoices duplicadas'
   if invoices_duplicadas_min==None
   else f'A Invoice ou NF cadastrada em {invoices_duplicadas_min} possui duplicata'
      if invoices_duplicadas_min == invoices_duplicadas_max
      else f'As invoices ou Notas fiscais cadastradas entre {invoices_duplicadas_min} e {invoices_duplicadas_max} possuem duplicatas'
)

# Salvando o DataFrame em um arquivo Excel
def salvar_dataframe_como_excel(dataframe, filename='invoices_duplicadas.xlsx'):
    buffer = BytesIO()
    dataframe.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)
    return buffer

# Função para criar a tabela do corpo do email 
def filtrar_protocolo_invoices_duplicadas(dataframe, anos=3):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['data_emissao'].notna(), :]
# Verificar se o DataFrame filtrado está vazio
    if invoices_duplicadas.empty:
        return "Nenhum estudos cadastrado está sem a moeda"
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_filtrado = invoices_duplicadas.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_filtrado.to_html(index=False)

# Chamando a função
invoices_duplicadas_html = filtrar_protocolo_invoices_duplicadas(invoices_duplicadas)

# Função de envio do e-mail
def enviar_email_protocolos_invoices_duplicadas():
    try:
        if invoices_duplicadas.empty:
            print("Notas Fiscais e Invoices sem duplicatas")
            return
        
        # Criação do arquivo Excel em memória
        excel_file = salvar_dataframe_como_excel(invoices_duplicadas)

        msg = MIMEMultipart("related")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = subject_email
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>{subject_email}</h2>
                <p>{invoices_duplicadas_html}</p>
                <p>Eu vim para te mandar mensagens, mua ha ha</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))
        
        # Anexando o arquivo Excel
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(excel_file.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename="invoices_duplicadas.xlsx"'
        )
        msg.attach(part)
        
        # Enviar o e-mail
        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print(f"{subject_email}")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_protocolos_invoices_duplicadas()

# TODO: Visitas realizadas e se elas estão vinculadas a alguma Invoice ou NF
fato_visitas_nf = df_participante_visita[[
    'id',
    'dados_participante',
    'dados_visita',
    'data_realizada',
    'dados_status',
    'dados_nota_fiscal'
    ]].copy()

# Extrair 'co_protocolo'
fato_visitas_nf['co_protocolo'] = fato_visitas_nf['dados_participante'].apply(
    lambda x: extrair_campo(x, 'co_protocolo')
)

# Extrair 'id_participante'
fato_visitas_nf['id_participante'] = fato_visitas_nf['dados_participante'].apply(
    lambda x: extrair_campo(x, 'id_participante')
)

# Extrair 'apelido_protocolo'
fato_visitas_nf['apelido_protocolo'] = fato_visitas_nf['dados_participante'].apply(
    lambda x: extrair_campo(x, 'dados_protocolo', 'apelido_protocolo')
)

participante = ['dados_visita']

for coluna in participante:
    if coluna in fato_visitas_nf.columns:
        fato_visitas_nf[coluna] = fato_visitas_nf[coluna].apply(
            lambda x: extrair_segunda_informacao(x) if isinstance(x, dict) else None
        )
    else:
        print(f"A coluna '{coluna}' não existe no DataFrame.")
        
ultima_info=['dados_status','dados_nota_fiscal']

for coluna in ultima_info:
    if coluna in fato_visitas_nf.columns:
        fato_visitas_nf.loc[:,coluna] = fato_visitas_nf[coluna].apply(extrair_ultima_informacao)
    else:
        print(f"A coluna '{coluna}' não existe no Dataframe")
fato_visitas_nf=fato_visitas_nf.drop('dados_participante', axis = 1)
colunas_data = ['data_realizada']

# Converte cada coluna de data separadamente para melhorar o desempenho
for coluna in colunas_data:
    fato_visitas_nf[coluna] = pd.to_datetime(fato_visitas_nf[coluna], errors='coerce').dt.tz_localize(None).dt.date
fato_visitas_nf.rename(columns={
    'id':'id_visita_nf',
    'apelido_protocolo': 'Protocolo',
    'dados_participante':'Participante',
    'dados_visita':'Visita',
    'data_realizada':'Data Realizada',
    'dados_status':'Status da visita',
    'dados_nota_fiscal':'Nota Fiscal'
    }, inplace=True)
filtros = ['Realizada', 'Realizada parcialmente']

fato_visitas_nf = fato_visitas_nf[
    fato_visitas_nf['Status da visita'].isin(filtros)
]
fato_visitas_nf = fato_visitas_nf[fato_visitas_nf['Nota Fiscal'].isna()]
fato_visitas_nf.columns
fato_visitas_nf = fato_visitas_nf[['Protocolo',
                                   'id_participante',
                                   'Visita',
                                   'Status da visita',
                                   'Data Realizada',
                                   'Nota Fiscal',
                                   'co_protocolo',
                                   ]]
colunas_data = ['Data Realizada']

# Converte cada coluna de data separadamente para melhorar o desempenho
for coluna in colunas_data:
    fato_visitas_nf[coluna] = pd.to_datetime(fato_visitas_nf[coluna], errors='coerce').dt.tz_localize(None)
iniciativa = df_protocolo[['id', 'dados_tipo_de_iniciativa']]
iniciativa.rename(columns={
    'id':'co_protocolo',
    'dados_tipo_de_iniciativa': 'Iniciatita'
    }, inplace=True)

colunas_a_extrair_recebimento=[
    'Iniciatita'
]

for coluna in colunas_a_extrair_recebimento:
    iniciativa[coluna] = iniciativa[coluna].apply(extrair_ultima_informacao)
fato_visitas_nf = fato_visitas_nf.merge(iniciativa, how = 'left', on='co_protocolo')
tipo_de_estudo =['Patrocinador']
fato_visitas_nf=fato_visitas_nf[fato_visitas_nf['Iniciatita'].isin(tipo_de_estudo)]

filtro_visita=['Particularidades do Financeiro ']
fato_visitas_nf=fato_visitas_nf[~fato_visitas_nf['Visita'].isin(filtro_visita)]
fato_visitas_nf = fato_visitas_nf[fato_visitas_nf['Visita'].notna()]

fato_visitas_nf = fato_visitas_nf[['id_participante',
                                   'Protocolo',
                                   'Iniciatita',
                                   'Visita',
                                   'Data Realizada',
                                   'Status da visita',
                                   'Nota Fiscal',
                                   ]].sort_values(by='Data Realizada', ascending = True)
# Primeira período para titulo do email
if not fato_visitas_nf.empty:
    fato_visitas_nf_min = fato_visitas_nf['Data Realizada'].min().strftime('%d/%m/%Y')
    fato_visitas_nf_max = fato_visitas_nf['Data Realizada'].max().strftime('%d/%m/%Y')
else:
    fato_visitas_nf_min = None
    fato_visitas_nf_max = None
subject_email =(
   f'Não existem sem nota fiscal ou invoice vinculada'
   if fato_visitas_nf_min==None
   else f'As visitas realizadas em {fato_visitas_nf_min} não possuem nota fiscal ou invoice vinculada'
      if fato_visitas_nf_min == fato_visitas_nf_max
      else f'As visitas realizadas entre {fato_visitas_nf_min} e {fato_visitas_nf_max} não possuem nota fiscal ou invoice vinculada'
)
subject_email
# Salvando o DataFrame em um arquivo Excel
def salvar_dataframe_como_excel(dataframe, filename='visitas_sem_nf.xlsx'):
    buffer = BytesIO()
    dataframe.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)
    return buffer
# Função para criar a tabela do corpo do email 
def filtrar_protocolo_fato_visitas_nf(dataframe, anos=3):
    # Filtrar contratos com data de assinatura não nula
    dataframe = dataframe.loc[dataframe['Data Realizada'].notna(), :]
# Verificar se o DataFrame filtrado está vazio
    if fato_visitas_nf.empty:
        return "Nenhuma visita realizada está sem a NF vinculada"
    else:
        # Formatar o DataFrame para exibição em HTML
        dataframe_filtrado = fato_visitas_nf.style\
            .format(precision=3, thousands=".", decimal=',')\
            .format_index(str.upper, axis=1)\
            .set_properties(**{'background-color': 'white'}, **{'color': 'black'})\
            .set_table_styles([{'selector': 'td:hover', 'props': [('background-color', '#EC0E73')]}])

        return dataframe_filtrado.to_html(index=False)

# Chamando a função
fato_visitas_nf_html = filtrar_protocolo_fato_visitas_nf(fato_visitas_nf)

# Função de envio do e-mail
def enviar_email_protocolos_fato_visitas_nf():
    try:
        if fato_visitas_nf.empty:
            print("Todas as visitas estão com a NF ou Invoice vinculada")
            return
        
        # Criação do arquivo Excel em memória
        excel_file = salvar_dataframe_como_excel(fato_visitas_nf)

        msg = MIMEMultipart("related")
        msg['From'] = username_email
        msg['Bcc'] = ', '.join(enviar_para)
        msg['Subject'] = subject_email
        
        # Corpo do e-mail simplificado
        body = f"""
        <html>
            <head>{css_hover}</head>
            <body>
                <h2>{subject_email}</h2>
                
                <p>{fato_visitas_nf_html}</p>
                <p>Eu vim para te mandar mensagens, mua ha ha</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))
        
        # Anexando o arquivo Excel
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(excel_file.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename="fato_visitas_nf.xlsx"'
        )
        msg.attach(part)
        
        # Enviar o e-mail
        with smtplib.SMTP(server_email, port_email) as server:
            server.starttls()
            server.login(username_email, password_email)
            server.send_message(msg)
        print(f"{subject_email}")
        
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

enviar_email_protocolos_fato_visitas_nf()


# TODO: Distribuição - visitas realizadas que não possuem NF vinculada.



# TODO: Agenda - visitas realizadas quais possuem procedimentos extras