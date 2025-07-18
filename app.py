import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Roda da Vida", layout="centered")
st.title("🎨 Roda da Vida - Avaliação Comportamental")

# Login e identificação
with st.form("identificacao"):
    nome = st.text_input("Digite seu nome completo")
    email = st.text_input("Email para identificação (opcional)")
    iniciar = st.form_submit_button("Iniciar Avaliação")

if iniciar and nome:
    st.markdown("Responda as perguntas abaixo de forma sincera, usando a escala de 0 (nada) a 10 (muito)")

    # Aspectos e perguntas
    aspectos = {
        "Amigos e Familiares": [
            "Existe troca verdadeira com pessoas próximas a você?",
            "Você sente que tem uma rede de apoio confiável?"
        ],
        "Lazer": [
            "Você se permite pausas e momentos sem obrigações?",
            "Tem vivido experiências leves e espontâneas?"
        ],
        "Vida Financeira": [
            "Você sente liberdade para tomar decisões financeiras?",
            "Suas escolhas materiais refletem seus valores?"
        ],
        "Intelecto": [
            "Com que frequência sente curiosidade para aprender algo novo?",
            "Suas atividades têm desafiado seu raciocínio ou conhecimento?"
        ],
        "Espiritualidade": [
            "Suas atitudes estão coerentes com seus valores pessoais?",
            "Você se conecta com algo maior que você?"
        ],
        "Amor": [
            "Seus vínculos afetivos contribuem positivamente para sua vida emocional?",
            "Você se sente acolhido nas relações mais íntimas?"
        ],
        "Trabalho e Carreira": [
            "Suas atividades diárias trazem realização pessoal?",
            "Seu ambiente de trabalho permite expressão pessoal?"
        ],
        "Saúde": [
            "Como você avalia sua disposição física ao longo dos dias?",
            "Seu corpo tem dado sinais de equilíbrio ou de alerta?"
        ]
    }

    resultados = {}

    # Coleta de respostas
    for aspecto, perguntas in aspectos.items():
        st.subheader("★")
        st.markdown(f"**{aspecto}**")
        respostas = []
        for pergunta in perguntas:
            nota = st.slider(pergunta, 0, 10, 5, key=pergunta)
            respostas.append(nota)
        media = round(sum(respostas) / len(respostas), 1)
        resultados[aspecto] = media

    # Geração do gráfico
    if st.button("Gerar Gráfico da Roda da Vida"):
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
            title=f"Roda da Vida de {nome}"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Exportar gráfico para imagem temporária
        with tempfile.TemporaryDirectory() as tmpdir:
            img_path = os.path.join(tmpdir, "roda_da_vida.png")
            pio.write_image(fig, img_path, format="png")

            # Criar PDF
            pdf_path = os.path.join(tmpdir, "roda_da_vida.pdf")
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Roda da Vida - {nome}", ln=True)
            pdf.image(img_path, x=10, y=30, w=180)
            pdf.output(pdf_path)

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Baixar PDF da Avaliação",
                    data=f.read(),
                    file_name=f"roda_da_vida_{nome.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
