import streamlit as st
import plotly.graph_objects as go
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Roda da Vida - Avaliação Comportamental", layout="centered")

# Inicialização de estado
if "exibir_resultado" not in st.session_state:
    st.session_state.exibir_resultado = False
if "respostas" not in st.session_state:
    st.session_state.respostas = {}
if "nome" not in st.session_state:
    st.session_state.nome = ""
if "email" not in st.session_state:
    st.session_state.email = ""

st.title("🧭 Roda da Vida - Avaliação Comportamental")

# Etapa 1: Identificação
if not st.session_state.nome:
    with st.form("identificacao_form"):
        nome = st.text_input("Seu nome")
        email = st.text_input("Seu e-mail (opcional)")
        submitted = st.form_submit_button("Iniciar avaliação")
        if submitted and nome:
            st.session_state.nome = nome
            st.session_state.email = email

# Etapa 2: Avaliação
aspectos = {
    "Espiritualidade": ["Sinto-me conectado a um propósito maior.", "Minha fé ou espiritualidade me orienta nas decisões."],
    "Saúde": ["Cuido bem da minha saúde física e mental.", "Tenho hábitos saudáveis e faço acompanhamento médico."],
    "Desenvolvimento Intelectual": ["Busco aprender continuamente.", "Dedico tempo à leitura ou aprendizado intencional."],
    "Relacionamentos": ["Tenho relações saudáveis e significativas.", "Consigo me comunicar de forma aberta e respeitosa."],
    "Contribuição Social": ["Envolvo-me com causas que impactam a sociedade.", "Sinto que contribuo para o bem comum."],
    "Realização Profissional": ["Sinto-me realizado com minha atuação profissional.", "Tenho clareza e propósito no que faço."],
    "Equilíbrio e Lazer": ["Tenho tempo para mim e para lazer.", "Consigo equilibrar trabalho e vida pessoal."],
    "Organização Financeira": ["Tenho controle das minhas finanças.", "Planejo meu futuro financeiro com segurança."]
}

if st.session_state.nome and not st.session_state.exibir_resultado:
    with st.form("avaliacao_form"):
        respostas = {}
        st.subheader("Autoavaliação")
        for aspecto, perguntas in aspectos.items():
            soma = 0
            for i, pergunta in enumerate(perguntas):
                nota = st.slider(pergunta, 0, 10, 5, key=f"{aspecto}_{i}")
                soma += nota
            media = round(soma / len(perguntas), 1)
            respostas[aspecto] = media
        finalizar = st.form_submit_button("Finalizar e gerar gráfico")
        if finalizar:
            st.session_state.respostas = respostas
            st.session_state.exibir_resultado = True

# Etapa 3: Resultado
if st.session_state.exibir_resultado:
    nome = st.session_state.nome
    respostas = st.session_state.respostas

    st.success(f"Avaliação concluída com sucesso, {nome}!")
    st.subheader("Sua Roda da Vida:")

    categorias = list(respostas.keys())
    valores = list(respostas.values())
    categorias += categorias[:1]
    valores += valores[:1]

    fig = go.Figure(
        data=[
            go.Scatterpolar(r=valores, theta=categorias, fill='toself', name="Autoavaliação")
        ],
        layout=go.Layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=False
        )
    )
    st.plotly_chart(fig)

    # Gerar PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, f"Roda da Vida - {nome}", ln=True)
    pdf.set_font("Arial", size=12)
    for aspecto, nota in respostas.items():
        pdf.cell(0, 10, f"{aspecto}: {nota}/10", ln=True)

    tmpdir = tempfile.gettempdir()
    pdf_path = os.path.join(tmpdir, f"roda_da_vida_{nome.replace(' ', '_')}.pdf")
    pdf.output(pdf_path)
    with open(pdf_path, "rb") as f:
        st.download_button("📄 Baixar PDF com resultados", f, file_name=f"roda_da_vida_{nome}.pdf")
