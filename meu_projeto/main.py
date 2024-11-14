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

siv = dim_protocolo.copy()


#------------------------------VISITA DE ENCERRAMENTO----------------------------------------------
#TODO  Close-Out Visit (COV)
cov = dim_protocolo.copy()

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