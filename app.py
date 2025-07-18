import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os

st.set_page_config(page_title="Roda da Vida - Avaliação Comportamental", page_icon="📊", layout="centered")

st.markdown("<h1 style='color:#004d7a'>📊 Roda da Vida - Avaliação Comportamental</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("Instruções")
    st.markdown("Responda as perguntas com atenção. Ao final, será gerado um gráfico e um PDF com seu resultado.")

# Aspectos da roda da vida
aspectos = [
    "Espiritualidade", "Saúde", "Relacionamentos", "Lazer",
    "Desenvolvimento Intelectual", "Vida Profissional",
    "Contribuição Social", "Equilíbrio Emocional"
]

# Perguntas para cada aspecto (duas por item)
perguntas = {
    "Espiritualidade": [
        "Sinto que tenho clareza sobre meus valores e princípios.",
        "Minha rotina inclui momentos intencionais de conexão espiritual."
    ],
    "Saúde": [
        "Sinto-me fisicamente bem e com energia.",
        "Tenho hábitos consistentes de alimentação e sono."
    ],
    "Relacionamentos": [
        "Tenho relações próximas e confiáveis.",
        "Sinto que sou compreendido e valorizado por quem me cerca."
    ],
    "Lazer": [
        "Tenho tempo de qualidade reservado para mim.",
        "Consigo incluir diversão e hobbies na minha semana."
    ],
    "Desenvolvimento Intelectual": [
        "Tenho buscado aprender coisas novas com frequência.",
        "Leio, assisto ou escuto conteúdos que me desafiam intelectualmente."
    ],
    "Vida Profissional": [
        "Sinto-me realizado(a) com o que faço profissionalmente.",
        "Meu trabalho está alinhado com meus valores e metas."
    ],
    "Contribuição Social": [
        "Sinto que minha vida impacta positivamente outras pessoas.",
        "Participo ou apoio causas sociais, ambientais ou comunitárias."
    ],
    "Equilíbrio Emocional": [
        "Consigo lidar bem com as minhas emoções.",
        "Tenho práticas de autocuidado emocional no dia a dia."
    ]
}

nome = st.text_input("Digite seu nome completo")
respostas = {}
formulario_ok = True

if nome:
    with st.form("questionario"):
        st.subheader("Autoavaliação")
        for aspecto in aspectos:
            total = 0
            for i, pergunta in enumerate(perguntas[aspecto]):
                resposta = st.slider(f"{pergunta}", 0, 10, 5, key=f"{aspecto}_{i}")
                total += resposta
            respostas[aspecto] = round(total / 2, 1)
        submitted = st.form_submit_button("Gerar Resultado")

    if submitted:
        # Gráfico radar
        fig = go.Figure()
        categorias = list(respostas.keys())
        valores = list(respostas.values())
        categorias += [categorias[0]]
        valores += [valores[0]]

        fig.add_trace(go.Scatterpolar(r=valores, theta=categorias, fill='toself', name='Você'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False)

        st.success("Avaliação concluída! Veja abaixo seu resultado.")
        st.plotly_chart(fig)

        # Gerar PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Roda da Vida - Avaliação Comportamental", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Nome: {nome}", ln=True)
        pdf.cell(0, 10, f"Data: {datetime.today().strftime('%d/%m/%Y')}", ln=True)
        pdf.ln(5)

        for aspecto, nota in respostas.items():
            pdf.cell(0, 10, f"{aspecto}: {nota}", ln=True)

        try:
            img_path = "/tmp/roda_temp.png"
            fig.write_image(img_path, format="png")
            pdf.image(img_path, x=30, w=150)
        except Exception:
            pdf.ln(10)
            pdf.multi_cell(0, 10, "⚠️ O gráfico não pôde ser gerado neste ambiente.")

        pdf_output_path = "/mnt/data/roda_da_vida_resultado.pdf"
        pdf.output(pdf_output_path)
        st.download_button("📄 Baixar Resultado em PDF", data=open(pdf_output_path, "rb"), file_name="roda_da_vida_resultado.pdf", mime="application/pdf")
else:
    st.info("Por favor, preencha seu nome para iniciar a avaliação.")
