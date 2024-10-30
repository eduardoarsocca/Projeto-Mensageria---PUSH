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

#------------------------------------------PROTOCOLO---------------------------------------------- 
rota_protocolo = url_request+"/protocolo?nested=true"
df_protocolo = requests.get(rota_protocolo, headers = headers).json()
df_protocolo = pd.DataFrame(df_protocolo)

dim_protocolo = df_protocolo[[
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
    'data_primeira_inclusao',
    'data_ultima_atualizacao',
    'meta_inclusao',
    'nu_meta_inclusao',
    'dados_co_centro',
    'status',
    'tipo_iniciativa',
    'nome_patrocinador',
    'status_contrato',
    'status_orcamento',
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
print(df_generica_limpo_contrato.head())
print(df_generica_limpo_orcamento.head())

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
    'data_primeira_inclusao',
    'data_ultima_atualizacao']

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
