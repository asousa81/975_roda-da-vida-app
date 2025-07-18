
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import tempfile
from fpdf import FPDF
import base64
import os

st.set_page_config(page_title="Roda da Vida - Avaliação Comportamental", layout="centered")
st.title("🧭 Roda da Vida - Avaliação Comportamental")

# Coleta de informações iniciais
with st.form(key="user_info"):
    nome = st.text_input("Informe seu nome completo")
    submitted_info = st.form_submit_button("Iniciar avaliação")

if submitted_info and nome:
    st.session_state.nome = nome
    st.session_state.etapa = "avaliacao"

if "etapa" not in st.session_state:
    st.session_state.etapa = "inicio"

aspectos = {
    "Amigos e Familiares": [
        "Sinto que posso contar com pessoas próximas quando preciso.",
        "Tenho conversas profundas e significativas com familiares ou amigos."
    ],
    "Lazer": [
        "Costumo reservar tempo para atividades prazerosas na semana.",
        "Concluo o dia sentindo que fiz algo que me deu prazer ou descanso."
    ],
    "Vida Financeira": [
        "Consigo pagar minhas despesas mensais com tranquilidade.",
        "Minha vida financeira está sob controle e consigo me planejar."
    ],
    "Intelecto": [
        "Busco aprender algo novo com frequência.",
        "Tenho clareza sobre o que ainda quero estudar ou aprender."
    ],
    "Espiritualidade": [
        "Tenho um momento reservado para minha fé, meditação ou reflexão.",
        "Sinto que vivo de acordo com meus valores mais profundos."
    ],
    "Amor": [
        "Sinto-me acolhido e valorizado no meu relacionamento afetivo.",
        "Conseguimos conversar com respeito mesmo em momentos difíceis."
    ],
    "Trabalho e Carreira": [
        "Estou satisfeito com o que faço profissionalmente.",
        "Vejo propósito no meu trabalho e sei aonde quero chegar."
    ],
    "Saúde": [
        "Tenho hábitos saudáveis na alimentação e prática de exercícios.",
        "Cuido da minha saúde física e mental com atenção."
    ],
}

if st.session_state.etapa == "avaliacao":
    respostas = {}
    with st.form("form_avaliacao"):
        for aspecto, perguntas in aspectos.items():
            with st.expander(f"{aspecto}"):
                for pergunta in perguntas:
                    resposta = st.slider(pergunta, 0, 10, 5, key=f"{aspecto}_{pergunta}")
                    respostas.setdefault(aspecto, []).append(resposta)
        finalizar = st.form_submit_button("Finalizar")

    if finalizar:
        st.session_state.etapa = "resultado"
        st.session_state.respostas = respostas

if st.session_state.etapa == "resultado":
    nome = st.session_state.nome
    respostas = st.session_state.respostas
    medias = {aspecto: sum(vals) / len(vals) for aspecto, vals in respostas.items()}

    st.subheader(f"Roda da Vida - {nome}")

    fig = go.Figure()
    categorias = list(medias.keys())
    valores = list(medias.values())
    categorias += [categorias[0]]
    valores += [valores[0]]

    fig.add_trace(go.Scatterpolar(r=valores, theta=categorias, fill='toself', name='Autoavaliação'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False)
    st.plotly_chart(fig)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf_output_path = tmp.name
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, f"Roda da Vida - {nome}", ln=True, align="C")
        pdf.set_font("Arial", size=12)
        for aspecto, media in medias.items():
            pdf.cell(200, 8, f"{aspecto}: {media:.2f}", ln=True)
        pdf.output(pdf_output_path)

        with open(pdf_output_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
            pdf_link = f'<a href="data:application/pdf;base64,{base64_pdf}" download="Roda_da_Vida_{nome}.pdf">📄 Baixar resultado em PDF</a>'
            st.markdown(pdf_link, unsafe_allow_html=True)
        os.unlink(pdf_output_path)

    st.markdown("""
---

### A história da Roda da Vida

A felicidade plena depende de diversos fatores de nossa vida, como a maneira que nos vemos, como são nossos relacionamentos, como lidamos com nossas carreiras, como nos portamos diante do mundo.  
Pensando nisso, os Hindus chegaram à conclusão de que era necessário ter um sistema no qual a pessoa pudesse avaliar cada parte importante de sua vida para entender quais pontos estão satisfatórios e quais precisam de atenção. Assim foi criada a Roda da Vida, uma técnica de avaliação pessoal separada em setores essenciais para encontrarmos um equilíbrio pessoal.

A Roda da Vida é um círculo dividido em oito, dez ou doze partes como um gráfico de pizza, representando aspectos pessoais, como:

- **Amigos e Familiares**
- **Lazer**
- **Vida Financeira**
- **Intelecto**
- **Espiritualidade**
- **Amor**
- **Trabalho e Carreira**
- **Saúde**
""")

import ace_tools as tools; tools.create_file("app.py", app_code)
