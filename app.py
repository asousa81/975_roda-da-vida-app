
import streamlit as st
import plotly.graph_objects as go
import os
from fpdf import FPDF
from datetime import datetime

# --- Configuração da página ---
st.set_page_config(page_title="Roda da Vida", page_icon="📊", layout="centered")

# --- Funções auxiliares ---
def gerar_grafico_roda(valores, nome_arquivo):
    categorias = list(valores.keys())
    notas = list(valores.values())
    notas.append(notas[0])
    categorias.append(categorias[0])

    fig = go.Figure(
        data=go.Scatterpolar(
            r=notas,
            theta=categorias,
            fill='toself',
            line=dict(color='rgba(0,100,200,0.7)')
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], showticklabels=False, ticks='')
        ),
        showlegend=False,
        margin=dict(l=30, r=30, t=30, b=30)
    )

    fig.write_image(nome_arquivo, format="png")
    return nome_arquivo

def gerar_pdf(nome, grafico_path, valores):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(200, 10, txt=f"Roda da Vida - {nome}", ln=True, align="C")
    pdf.ln(10)

    # Adiciona o gráfico
    if os.path.exists(grafico_path):
        pdf.image(grafico_path, x=35, y=30, w=140)
        pdf.ln(100)
    else:
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, "O gráfico não pôde ser gerado neste ambiente.")

    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for k, v in valores.items():
        pdf.cell(0, 10, f"{k}: {v}", ln=True)

    output_path = f"Roda_da_Vida_{nome.replace(' ', '_')}.pdf"
    pdf.output(output_path)
    return output_path

# --- Interface principal ---
st.title("📊 Roda da Vida - Avaliação Comportamental")

with st.form("formulario"):
    nome = st.text_input("Seu nome completo")
    email = st.text_input("Seu e-mail")
    st.markdown("### Avalie de 0 a 10 (sem identificar o tema da pergunta)")

    perguntas = {
        "Sinto que tenho equilíbrio entre minha vida pessoal e profissional.": "Equilíbrio",
        "Tenho objetivos claros e trabalho ativamente para alcançá-los.": "Propósito",
        "Tenho energia e disposição na maior parte do tempo.": "Saúde",
        "Consigo manter bons relacionamentos com pessoas próximas.": "Relacionamentos",
        "Administro bem meu tempo e prioridades.": "Gestão de Tempo",
        "Tenho controle sobre minhas finanças e faço planejamentos.": "Finanças",
        "Dedico tempo ao meu desenvolvimento pessoal e aprendizado.": "Desenvolvimento",
        "Consigo lidar bem com emoções e frustrações.": "Emocional"
    }

    respostas = {}
    for pergunta in perguntas:
        respostas[perguntas[pergunta]] = st.slider(pergunta, 0, 10, 5)

    enviado = st.form_submit_button("Gerar Análise")

if enviado:
    with st.spinner("Gerando sua Roda da Vida..."):
        img_path = f"grafico_{nome.replace(' ', '_')}.png"
        gerar_grafico_roda(respostas, img_path)
        pdf_path = gerar_pdf(nome, img_path, respostas)

    st.success("✅ Análise concluída!")
    st.image(img_path, caption="Sua Roda da Vida", use_column_width=True)

    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📄 Baixar PDF com Análise",
            data=f,
            file_name=f"Roda_da_Vida_{nome.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )

    # Oculta perguntas após envio
    st.markdown("---")
    st.markdown(f"**Nome:** {nome}")
    st.markdown(f"**E-mail:** {email}")
    os.remove(img_path)
    os.remove(pdf_path)
