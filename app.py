
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Roda da Vida - Avaliação Comportamental", layout="centered")

def gerar_grafico(resultados, nome):
    categorias = list(resultados.keys())
    valores = list(resultados.values())
    N = len(categorias)
    valores += valores[:1]
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, valores, linewidth=2, linestyle='solid')
    ax.fill(angles, valores, alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categorias)
    ax.set_title(f"Roda da Vida - {nome}", size=14, y=1.08)
    return fig

def gerar_pdf(nome, resultados, fig):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Roda da Vida - Avaliação de {nome}", ln=True)
    pdf.set_font("Arial", '', 12)
    for aspecto, valor in resultados.items():
        pdf.cell(0, 10, f"{aspecto}: {valor}", ln=True)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        fig.savefig(tmpfile.name, format="png")
        pdf.image(tmpfile.name, x=30, y=pdf.get_y() + 10, w=150)
        os.unlink(tmpfile.name)
    pdf_output_path = os.path.join(tempfile.gettempdir(), f"{nome}_roda_vida.pdf")
    pdf.output(pdf_output_path)
    return pdf_output_path

st.title("Roda da Vida - Avaliação Comportamental")
nome = st.text_input("Digite seu nome")

aspectos = {
    "Amigos e Familiares": [
        "Você tem se sentido confortável para conversar com familiares ou amigos sobre algo pessoal?",
        "Com que frequência você tem se sentido emocionalmente próximo de alguém querido?"
    ],
    "Lazer": [
        "Você tem separado tempo livre para fazer algo prazeroso nos últimos dias?",
        "Na última semana, você teve momentos de relaxamento ou diversão?"
    ],
    "Vida Financeira": [
        "Você tem conseguido pagar suas contas sem grandes dificuldades?",
        "Nos últimos dias, sua situação financeira gerou algum desconforto?"
    ],
    "Intelecto": [
        "Você sentiu que aprendeu algo novo ou estimulante recentemente?",
        "Nos últimos tempos, você dedicou tempo a desenvolver algum conhecimento ou habilidade?"
    ],
    "Espiritualidade": [
        "Você tem recorrido a alguma prática ou crença pessoal para lidar com desafios?",
        "Nos últimos dias, sentiu-se conectado a algo maior ou refletiu sobre seus valores?"
    ],
    "Amor": [
        "Você tem se sentido emocionalmente satisfeito em sua relação afetiva ou consigo mesmo?",
        "Nos últimos tempos, o carinho e o respeito estiveram presentes em sua vida amorosa?"
    ],
    "Trabalho e Carreira": [
        "Você tem se sentido produtivo e realizado em suas atividades profissionais ou acadêmicas?",
        "Nos últimos dias, o trabalho ou rotina contribuíram positivamente para seu bem-estar?"
    ],
    "Saúde": [
        "Você tem cuidado de sua saúde, com alimentação equilibrada ou atividade física?",
        "Nos últimos dias, sua saúde impactou negativamente sua disposição ou humor?"
    ]
}

respostas = {}
if nome:
    with st.form("formulario"):
        for aspecto, perguntas in aspectos.items():
            st.markdown(f"### {aspecto}")
            total = 0
            for i, pergunta in enumerate(perguntas):
                resposta = st.slider(pergunta, 0, 10, 5, key=f"{aspecto}_{i}")
                total += resposta
            media = round(total / 2, 1)
            respostas[aspecto] = media
        enviado = st.form_submit_button("Finalizar")

    if enviado:
        st.success("Avaliação concluída com sucesso!")
        fig = gerar_grafico(respostas, nome)
        st.pyplot(fig)
        pdf_path = gerar_pdf(nome, respostas, fig)
        with open(pdf_path, "rb") as file:
            st.download_button("📥 Baixar PDF com resultado", data=file, file_name=f"{nome}_roda_da_vida.pdf")

        st.markdown("---")
        st.markdown("""
### A história da Roda da Vida

A felicidade plena depende de diversos fatores de nossa vida, como a maneira que nos vemos, como são nossos relacionamentos, como lidamos com nossas carreiras, como nos portamos diante do mundo.

Pensando nisso, os Hindus chegaram à conclusão de que era necessário ter um sistema no qual a pessoa pudesse avaliar cada parte importante de sua vida para entender quais pontos estão satisfatórios e quais precisam de atenção. Assim foi criada a Roda da Vida, uma técnica de avaliação pessoal separada em setores essenciais para encontrarmos um equilíbrio pessoal.
""")
