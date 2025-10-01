# Projeto Mensageria PUSH

> Plataforma em Python para orquestração, envio e monitoramento de mensagens (push / notificações) com interface interativa para análise e operação.

## Sumário
- [Contexto](#contexto)
- [Objetivos](#objetivos)
- [Principais Funcionalidades](#principais-funcionalidades)
- [Arquitetura (Visão Geral)](#arquitetura-visão-geral)
- [Stack Tecnológica](#stack-tecnológica)
- [Estrutura Sugerida de Diretórios](#estrutura-sugerida-de-diretórios)
- [Instalação e Ambiente](#instalação-e-ambiente)
- [Configuração (.env)](#configuração-env)
- [Execução](#execução)
- [Fluxo Operacional (Exemplo)](#fluxo-operacional-exemplo)
- [Boas Práticas e Qualidade](#boas-práticas-e-qualidade)
- [Métricas Possíveis](#métricas-possíveis)
- [Limitações Atuais (Prováveis)](#limitações-atuais-prováveis)
- [Possíveis Evoluções](#possíveis-evoluções)
- [Licença](#licença)
- [Contato](#contato)

---

## Contexto
Este projeto visa centralizar o envio e acompanhamento de mensagens (ex.: notificações push, campanhas de engajamento ou alertas internos), oferecendo uma interface explorável para operadores acompanharem métricas, status e histórico. A ênfase recai em agilidade, rastreabilidade e visualização de resultados.

## Objetivos
- Padronizar o processo de disparo de mensagens/campanhas.
- Permitir visualização interativa (dashboard) de desempenho e falhas.
- Facilitar ingestão de listas a partir de fontes tabulares (Excel / CSV).
- Reduzir retrabalho ao registrar versões de campanhas e configurações.
- Criar base escalável para integrações futuras (APIs externas, filas, automação).

## Principais Funcionalidades
(Algumas inferidas a partir das dependências; ajustar conforme código real.)
- Upload e validação de bases (Excel / CSV) para destinatários.
- Painel analítico (gráficos via Altair / Plotly / Seaborn / Matplotlib).
- Envio orquestrado ou simulado de mensagens (ex.: via requests a provedores).
- Registro de status (sucesso, erro, tempo de resposta).
- Histórico versionado (possível uso de GitPython para log ou auditoria).
- Configuração dinâmica via `.env` (chaves de API, endpoints, throttling).
- Exportações de relatórios (Excel / Parquet / CSV).

## Arquitetura (Visão Geral)
1. Camada de Interface: Streamlit para interação (upload, filtros, dashboards).
2. Camada de Processamento: Scripts de limpeza, normalização e enriquecimento (pandas / numpy).
3. Camada de Envio: Módulos de integração (requests) com provedores ou endpoints internos.
4. Persistência / Logs: Armazenamento (possivelmente CSV, Parquet ou diretório dedicado).
5. Observabilidade: Geração de métricas e gráficos (Altair, Plotly).
6. Configuração: Variáveis externas e seguras via `python-dotenv`.

(Se houver filas ou mensageria real – ex.: Kafka, Redis, Firebase, FCM – inserir aqui.)

## Stack Tecnológica
- Linguagem: Python
- UI / App: Streamlit
- Dados / ETL leve: pandas, numpy, pyarrow
- Visualizações: Altair, Plotly, Seaborn, Matplotlib
- Arquivos: openpyxl (Excel), pyarrow (Parquet)
- Configuração: python-dotenv
- Logs / Ops: rich
- Versionamento auxiliar / automação: GitPython
- Outros utilitários: requests (APIs), watchdog (hot-reload / monitoramento de arquivos)

## Estrutura Sugerida de Diretórios
(Ajustar conforme a estrutura real do repositório.)
```
Projeto-Mensageria---PUSH/
├── app/                     # Componentes Streamlit
│   ├── __init__.py
│   ├── main.py              # Entrada principal (streamlit run)
│   ├── pages/               # Páginas adicionais
├── core/
│   ├── config.py            # Carrega variáveis .env
│   ├── messaging.py         # Funções de envio
│   ├── loaders.py           # Leitura / validação de bases
│   ├── analytics.py         # Cálculo de métricas
│   ├── storage.py           # Persistência (local / remoto)
├── data/
│   ├── input/               # Bases carregadas
│   ├── processed/           # Dados tratados
│   └── logs/                # Logs de envio / auditoria
├── reports/
│   ├── exports/             # Relatórios gerados
│   └── figs/                # Gráficos salvos
├── tests/
│   ├── test_messaging.py
│   └── test_loaders.py
├── requirements.txt
├── .env.example
├── README.md
└── LICENSE
```

## Instalação e Ambiente
```
git clone https://github.com/eduardoarsocca/Projeto-Mensageria---PUSH.git
cd Projeto-Mensageria---PUSH
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuração (.env)
Criar um arquivo `.env` (ou copiar de `.env.example`):
```
API_PROVIDER_URL=https://api.exemplo.com/send
API_KEY=chave_aqui
TIMEOUT_SECONDS=10
DEFAULT_BATCH_SIZE=200
LOG_LEVEL=INFO
```
Adicionar ao `.gitignore` se contiver segredos.

## Execução
Executar a interface:
```
streamlit run app/main.py
```
(Se o entry-point estiver diferente, ajustar.)

Modo notebook (exploração):
```
jupyter notebook
```

## Fluxo Operacional (Exemplo)
1. Carregar base de destinatários (Excel / CSV).
2. Validar colunas obrigatórias (ex.: id, canal, token/endereço).
3. Selecionar modelo de mensagem / template.
4. Executar envio (batch / simulação).
5. Monitorar status em dashboard (gráfico de sucesso, latência).
6. Exportar relatório consolidado.
7. Auditar logs e anotar campanha.

## Boas Práticas e Qualidade
- Separação clara: interface vs núcleo de negócio.
- Funções puras para transformação de dados.
- Parametrização (evitar literais fixos).
- Testes unitários mínimos em parsing / validação.
- Logging estruturado (json ou colunas) para auditoria futura.

## Métricas Possíveis
- Total de mensagens processadas / entregues / falhas.
- Latência média por provedor.
- Taxa de erro (%) por janela de tempo.
- Retries executados.
- Throughput (msg/min).

## Limitações Atuais (Prováveis)
- Ausência (ou não) de filas assíncronas robustas.
- Escalabilidade limitada a execução local (Streamlit single-process).
- Falta de persistência relacional / NoSQL (se não implementada).
- Dependência do formato correto de entrada manual.

## Possíveis Evoluções
- Suporte a múltiplos canais (push + e-mail + SMS).
- Adoção de filas (RabbitMQ, Kafka) para desacoplamento.
- Mecanismo de retry exponencial e DLQ.
- Autenticação na interface (OAuth / JWT).
- Painel de auditoria com drill-down em falhas.
- Exportações automáticas para data lake / warehouse.
- Observabilidade (Prometheus + Grafana / OpenTelemetry).



## Contato
Autor: Eduardo Augusto Rabelo Socca  
E-mail: eduardo_socca@yahoo.com.br  
LinkedIn: www.linkedin.com/in/soccaear  

