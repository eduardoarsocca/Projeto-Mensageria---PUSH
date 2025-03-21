import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as po

# Configuração da página
st.set_page_config(
    page_title="Gráficos com Grid CSS", 
    layout="wide",
    page_icon="📊"
    )

# CSS Personalizado para o Grid
st.markdown(
    """
    <style>
   .stAppHeader{
        background-color: #ffffff;
    }
    .stApp{
        background-color: blue ;
    }
   
    .stVerticalBlock{
        border: 5px solid green;
        padding:5px;
        
      
    }
    .st-emotion-cache-1rsyhoq{
        display: flex;
        align-items: starts;
        justify-content: space-between;
        gap: 30px;
        
        
        
    }
    /* stMainBlockContainer e st-emotion-cache-pgf13w filhos da classe .st-emotion-cache-1rsyhoq */
    
    /* main-sv é pai da classe st-emotion-cache-pgf13w  */
    
    .main-svg{
        width: 97%;
       
    }
    .st-emotion-cache-pgf13w{        
        width: 97%;
        padding: 0px 0 10px 0 ;
        margin: 0px 0;
        border: 10px solid #FFFAA0;
    }
    
    
    .stMainBlockContainer{
        background-color: black;
        border: 5px solid #FFFAA0;
    }
    
    
   
    h1{
        color: black;
        font-size: 48px;
        font-weight: bold;
        background-color: #FFFFFF;
        text-align: center;
    }
    .graph-container{
        background-color: #ff0000;
        
        width: 97%;
        text-align: center;
        font-size: 48px;
        color: #FFFFFF;
    }
    

    
    </style>
    """,
    unsafe_allow_html=True
)

# Gerar dados para os gráficos
df1 = pd.DataFrame({
    "Categoria": ["A", "B", "C", "D"],
    "Valores": [10, 20, 30, 40]
})
df2 = pd.DataFrame({
    "Categoria": ["W", "X", "Y", "Z"],
    "Valores": [15, 25, 35, 45]
})
altura= 400
largura=600

fig1 = px.bar(df1, x="Categoria", y="Valores", title="Gráfico 1")

fig2 = px.line(df2, x="Categoria", y="Valores", title="Gráfico 2")


#Configurando o Header do Streamlit
st.markdown(
    """
    <div class="stMainBlockContainer">
        <img class=imagem  src="https://image.similarpng.com/file/similarpng/very-thumbnail/2021/05/Logo-design-illustration-on-transparent-background-PNG.png" width="100" height="100">
    </div>
    <div class="main-svg">
        <h1 class="h1">Gráficos com Grid CSS</h1>
    </div>
    
    """,
    unsafe_allow_html=True
)
# Colocando uma imagem no header do stramlit na classe stMainBlockContainer


# Configurando a área de conteúdo
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        <div class="graph-container">
            <div class="graph-title">Gráfico de Barras</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.plotly_chart(fig1, use_container_width=True, theme='streamlit')
with col2:
    st.markdown(
        """
        <div class="graph-container">
            <div class="graph-title">Gráfico de Linhas</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.plotly_chart(fig2, use_container_width=True,theme='streamlit')
