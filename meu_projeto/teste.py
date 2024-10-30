import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Configurações da página
st.set_page_config(page_title="Dashboard de Análise de Dados", layout="wide")

# Cabeçalho com logomarca e menu de navegação
st.markdown(
    """
    <div style='background-color: #f4f4f4; padding: 10px;'>
        <div style='display: flex; align-items: center;'>
            <img src='https://via.placeholder.com/100' alt='Logomarca' style='width: 100px; margin-right: 20px;'>
            <h1 style='color: #333;'>Dashboard de Análise de Dados</h1>
        </div>
    </div>
    <div style='display: flex; justify-content: center; gap: 30px; background-color: #007bff; padding: 15px;'>
        <a href='#gráfico1' style='text-decoration: none; color: white; font-size: 18px;'>Gráfico 1</a>
        <a href='#gráfico2' style='text-decoration: none; color: white; font-size: 18px;'>Gráfico 2</a>
        <a href='#contato' style='text-decoration: none; color: white; font-size: 18px;'>Contato</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Corpo com os gráficos da análise de dados
st.header("Gráfico 1: Distribuição de Dados")
data = np.random.randn(1000)
fig, ax = plt.subplots()
ax.hist(data, bins=20, color='#007bff', edgecolor='black')
ax.set_title("Histograma de Distribuição de Dados")
ax.set_xlabel("Valor")
ax.set_ylabel("Frequência")
st.pyplot(fig)

st.header("Gráfico 2: Gráfico de Linha")
x = np.linspace(0, 10, 100)
y = np.sin(x)
fig, ax = plt.subplots()
ax.plot(x, y, color='#ff6347', linestyle='-', linewidth=2)
ax.set_title("Gráfico de Linha de Função Seno")
ax.set_xlabel("Eixo X")
ax.set_ylabel("Eixo Y")
st.pyplot(fig)

# Rodapé com dados de contato e outros elementos comuns
st.markdown(
    """
    <footer id='contato' style='background-color: #f4f4f4; padding: 20px; margin-top: 30px;'>
        <div style='text-align: center;'>
            <p>Entre em contato: <a href='mailto:contato@example.com'>contato@example.com</a></p>
            <p>Telefone: (11) 1234-5678</p>
            <img src='https://via.placeholder.com/100' alt='Logomarca' style='width: 100px; margin-top: 10px;'>
            <p>2024 © Todos os direitos reservados.</p>
        </div>
    </footer>
    """,
    unsafe_allow_html=True
)