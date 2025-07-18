
import streamlit as st
import plotly.graph_objects as go
from fpdf import FPDF
import tempfile
import os

# ----- Configuração da Página -----
st.set_page_config(page_title="Roda da Vida - Avaliação Comportamental", layout="centered")

# ----- Estilo customizado -----
st.markdown(
    '''
    <style>
        .main {background-color: #f9f9f9;}
        h1, h2, h3 {
            color: #202020;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .stTextInput>div>input {
            border: 1px solid #ccc;
        }
    </style>
    ''',
    unsafe_allow_html=True
)

# ----- Título e descrição -----
st.title("🧭 Roda da Vida - Avaliação Comportamental")
st.markdown("Preencha a autoavaliação abaixo de forma espontânea. Ao final, você visualizará sua Roda da Vida.")

# ----- Coleta de informações iniciais -----
with st.form("identificacao_form"):
    nome = st.text_input("Seu nome")
    email = st.text_input("Seu e-mail (opcional)")
    submitted = st.form_submit_button("Iniciar avaliação")

# ----- Aspectos e perguntas -----
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

notas_finais = {}
exibir_resultado = False

if submitted and nome:
    with st.form("avaliacao_form"):
        st.subheader("Autoavaliação")
        for aspecto, perguntas in aspectos.items():
            soma = 0
            peso_total = 0
            for i, pergunta in enumerate(perguntas):
                nota = st.slider(pergunta, 0, 10, 5, key=f"{aspecto}_{i}")
                peso = 1  # Por padrão, peso igual para todas
                soma += nota * peso
                peso_total += peso
            media = round(soma / peso_total, 1) if peso_total > 0 else 0
            notas_finais[aspecto] = media
        finalizar = st.form_submit_button("Finalizar e gerar gráfico")
        if finalizar:
            exibir_resultado = True

# ----- Exibição dos resultados -----
if exibir_resultado:
    st.success(f"Avaliação concluída com sucesso, {nome}!")
    st.subheader("Sua Roda da Vida:")

    # Oculta perguntas, exibe só gráfico
    categorias = list(notas_finais.keys())
    valores = list(notas_finais.values())
    valores += valores[:1]  # para fechar o gráfico
    categorias += categorias[:1]

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

    # ----- Geração do PDF -----
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, f"Roda da Vida - {nome}", ln=True)
    pdf.set_font("Arial", size=12)
    for aspecto, nota in notas_finais.items():
        pdf.cell(0, 10, f"{aspecto}: {nota}/10", ln=True)
    try:
        # Aviso sobre ambiente restrito para imagem
        tmpdir = tempfile.gettempdir()
        pdf_path = os.path.join(tmpdir, f"roda_da_vida_{nome.replace(' ', '_')}.pdf")
        pdf.output(pdf_path)
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Baixar PDF com resultados", f, file_name=f"roda_da_vida_{nome}.pdf")
    except Exception as e:
        st.warning("⚠️ O PDF foi gerado sem o gráfico devido a restrições de ambiente.")

