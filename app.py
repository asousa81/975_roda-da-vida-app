
import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio
import os
from fpdf import FPDF
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Roda da Vida - Avaliação Comportamental", layout="centered")

# Título com estilo profissional
st.markdown("## 📊 <span style='color:#004d7a;'>Roda da Vida - Avaliação Comportamental</span>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar para informações adicionais
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/8b/Color_icon_blue.svg", width=100)
    st.markdown("### 💡 Instruções")
    st.write("Responda honestamente às afirmações a seguir. O resultado será visualizado em um gráfico e poderá ser exportado em PDF.")
    st.markdown("---")
    st.markdown("🔒 Seus dados são confidenciais e usados apenas para fins de reflexão.")

# Entrada de nome
nome = st.text_input("Digite seu nome para iniciar:", "")

# Áreas da Roda da Vida
aspectos = [
    "Espiritualidade", "Saúde", "Desenvolvimento Pessoal", "Relacionamentos",
    "Lazer", "Propósito Profissional", "Finanças", "Contribuição Social"
]

respostas = {}
if nome:
    with st.form(key="form_avaliacao"):
        st.markdown("### ✅ Avalie de 0 a 10 sua percepção atual em cada aspecto abaixo:")
        for aspecto in aspectos:
            respostas[aspecto] = st.slider(f"{aspecto}", 0, 10, 5)
        submitted = st.form_submit_button("Gerar gráfico e relatório")

    if submitted:
        # Gerar gráfico
        categorias = list(respostas.keys())
        valores = list(respostas.values())
        valores += valores[:1]  # Fechamento do radar

        fig = go.Figure(
            data=[go.Scatterpolar(r=valores, theta=categorias + [categorias[0]], fill='toself', name=nome)]
        )
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=False,
            margin=dict(l=30, r=30, t=30, b=30)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Caminho temporário
        img_path = f"{nome}_roda.png"
        try:
            pio.write_image(fig, img_path, format="png")
            imagem_ok = True
        except Exception:
            imagem_ok = False

        # Gerar PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.set_text_color(0, 77, 122)
        pdf.cell(200, 10, f"Roda da Vida - Avaliação Comportamental", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(10)
        pdf.cell(200, 10, f"Nome: {nome}", ln=True)
        pdf.cell(200, 10, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
        pdf.ln(10)
        pdf.cell(200, 10, "Resultados:", ln=True)

        for aspecto, valor in respostas.items():
            pdf.cell(200, 10, f"{aspecto}: {valor}/10", ln=True)

        if imagem_ok and os.path.exists(img_path):
            pdf.image(img_path, x=35, w=140)
        else:
            pdf.ln(10)
            pdf.set_text_color(200, 0, 0)
            pdf.multi_cell(0, 10, "⚠️ O gráfico não pôde ser gerado neste ambiente.
Você ainda pode usar os dados acima para sua reflexão.")

        pdf_output = f"{nome}_roda_da_vida.pdf"
        pdf.output(pdf_output)

        with open(pdf_output, "rb") as f:
            st.download_button(
                label="📥 Baixar PDF com resultados",
                data=f,
                file_name=pdf_output,
                mime="application/pdf"
            )

        # Limpeza de arquivos temporários
        if os.path.exists(img_path):
            os.remove(img_path)
        if os.path.exists(pdf_output):
            os.remove(pdf_output)
else:
    st.info("Digite seu nome para iniciar a avaliação.")
