
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
import tempfile
import os
import base64

st.set_page_config(page_title="📊 Roda da Vida - Avaliação Comportamental", layout="centered")
st.title("📊 Roda da Vida - Avaliação Comportamental")

if "iniciar_avaliacao" not in st.session_state:
    st.session_state.iniciar_avaliacao = False

if not st.session_state.iniciar_avaliacao:
    with st.form("identificacao"):
        nome = st.text_input("Digite seu nome completo")
        email = st.text_input("Email para identificação (opcional)")
        iniciar = st.form_submit_button("Iniciar Avaliação")
        if iniciar and nome:
            st.session_state.iniciar_avaliacao = True
            st.session_state.nome = nome
else:
    st.markdown("Responda as perguntas abaixo de forma sincera, usando a escala de 0 (nada) a 10 (muito)")

    perguntas = [
        "Existe troca verdadeira com pessoas próximas a você?",
        "Você sente que tem uma rede de apoio confiável?",
        "Você se permite pausas e momentos sem obrigações?",
        "Tem vivido experiências leves e espontâneas?",
        "Você sente liberdade para tomar decisões financeiras?",
        "Suas escolhas materiais refletem seus valores?",
        "Com que frequência sente curiosidade para aprender algo novo?",
        "Suas atividades têm desafiado seu raciocínio ou conhecimento?",
        "Suas atitudes estão coerentes com seus valores pessoais?",
        "Você se conecta com algo maior que você?",
        "Seus vínculos afetivos contribuem positivamente para sua vida emocional?",
        "Você se sente acolhido nas relações mais íntimas?",
        "Suas atividades diárias trazem realização pessoal?",
        "Seu ambiente de trabalho permite expressão pessoal?",
        "Como você avalia sua disposição física ao longo dos dias?",
        "Seu corpo tem dado sinais de equilíbrio ou de alerta?"
    ]

    respostas = []
    for idx, pergunta in enumerate(perguntas):
        respostas.append(st.slider(pergunta, 0, 10, 5, key=f"q{idx}"))

    if st.button("Gerar Gráfico da Roda da Vida"):
        aspectos = {
            "Amigos e Familiares": respostas[0:2],
            "Lazer": respostas[2:4],
            "Vida Financeira": respostas[4:6],
            "Intelecto": respostas[6:8],
            "Espiritualidade": respostas[8:10],
            "Amor": respostas[10:12],
            "Trabalho e Carreira": respostas[12:14],
            "Saúde": respostas[14:16]
        }

        resultados = {k: round(sum(v)/len(v), 1) for k, v in aspectos.items()}

        categorias = list(resultados.keys())
        valores = list(resultados.values())
        categorias += [categorias[0]]
        valores += [valores[0]]

        fig = go.Figure(
            data=[
                go.Scatterpolar(r=valores, theta=categorias, fill='toself', name='Você')
            ]
        )

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=False,
            title=f"Roda da Vida de {st.session_state.nome}"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Tentar gerar imagem e incluir no PDF
        try:
            img_bytes = fig.to_image(format="png")
            with tempfile.TemporaryDirectory() as tmpdir:
                img_path = os.path.join(tmpdir, "grafico.png")
                with open(img_path, "wb") as img_file:
                    img_file.write(img_bytes)

                pdf_path = os.path.join(tmpdir, "roda_da_vida.pdf")
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 14)
                pdf.cell(200, 10, txt=f"Roda da Vida - {st.session_state.nome}", ln=True)
                pdf.ln(5)
                pdf.set_font("Arial", "", 12)
                for aspecto, nota in resultados.items():
                    pdf.cell(0, 10, txt=f"{aspecto}: {nota}", ln=True)
                pdf.image(img_path, x=10, y=80, w=180)
                pdf.output(pdf_path)

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="Baixar PDF com Gráfico",
                        data=f.read(),
                        file_name=f"roda_da_vida_{st.session_state.nome.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
        except Exception as e:
            st.error("Ocorreu um erro ao gerar a imagem do gráfico. PDF será gerado apenas com os dados.")
            with tempfile.TemporaryDirectory() as tmpdir:
                pdf_path = os.path.join(tmpdir, "roda_da_vida_texto.pdf")
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 14)
                pdf.cell(200, 10, txt=f"Roda da Vida - {st.session_state.nome}", ln=True)
                pdf.ln(5)
                pdf.set_font("Arial", "", 12)
                for aspecto, nota in resultados.items():
                    pdf.cell(0, 10, txt=f"{aspecto}: {nota}", ln=True)
                pdf.output(pdf_path)

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="Baixar PDF com Resultados (sem gráfico)",
                        data=f.read(),
                        file_name=f"roda_da_vida_{st.session_state.nome.replace(' ', '_')}_sem_grafico.pdf",
                        mime="application/pdf"
                    )
