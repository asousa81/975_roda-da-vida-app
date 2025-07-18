
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

# Etapa 2: Perguntas
perguntas = [
    ("Você tem pessoas com quem pode contar de verdade?", "Amigos e Familiares"),
    ("Seus vínculos mais próximos têm sido fonte de apoio ou de desgaste?", "Amigos e Familiares"),
    ("Você tem feito coisas que te divertem ou te fazem relaxar?", "Lazer"),
    ("Faz quanto tempo que você tirou um tempo só pra você, sem culpa?", "Lazer"),
    ("Você consegue pagar suas contas sem ficar no aperto?", "Vida Financeira"),
    ("Tem conseguido guardar ou planejar algo com o dinheiro que recebe?", "Vida Financeira"),
    ("Você sente que está aprendendo coisas novas que fazem sentido?", "Intelecto"),
    ("Você costuma investir tempo em algo que te faça crescer como pessoa?", "Intelecto"),
    ("Você tem se sentido em paz com o que acredita ou com seus valores?", "Espiritualidade"),
    ("Tem feito algo que alimente sua fé, espiritualidade ou propósito de vida?", "Espiritualidade"),
    ("Você sente que há afeto e respeito nas suas relações afetivas?", "Amor"),
    ("Sua vida amorosa tem te feito bem ou te traz mais frustração que alegria?", "Amor"),
    ("Você sente que faz sentido o que você faz profissionalmente?", "Trabalho e Carreira"),
    ("Você sente motivação ao pensar na sua vida profissional atual?", "Trabalho e Carreira"),
    ("Seu corpo tem te dado sinais positivos ou de cansaço?", "Saúde"),
    ("Você sente que cuida da sua saúde com responsabilidade?", "Saúde")
]

if st.session_state.nome and not st.session_state.exibir_resultado:
    with st.form("avaliacao_form"):
        respostas = {}
        for i, (pergunta, aspecto) in enumerate(perguntas):
            nota = st.slider(pergunta, 0, 10, 5, key=f"pergunta_{i}")
            if aspecto not in respostas:
                respostas[aspecto] = []
            respostas[aspecto].append(nota)
        finalizar = st.form_submit_button("Finalizar e gerar gráfico")
        if finalizar:
            medias = {k: round(sum(v)/len(v), 1) for k, v in respostas.items()}
            st.session_state.respostas = medias
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

        st.markdown('''
---

### 🌀 A História da Roda da Vida

A felicidade plena depende de diversos fatores da nossa vida, como a maneira que nos vemos, como são nossos relacionamentos, como lidamos com nossas carreiras, como nos portamos diante do mundo.

Pensando nisso, os Hindus chegaram à conclusão de que era necessário ter um sistema no qual a pessoa pudesse avaliar cada parte importante de sua vida para entender quais pontos estão satisfatórios e quais precisam de atenção. Assim foi criada a **Roda da Vida**, uma técnica de avaliação pessoal separada em setores essenciais para encontrarmos um equilíbrio pessoal.

Ela é tradicionalmente representada como um gráfico de pizza com 8, 10 ou 12 fatias — neste teste, usamos **8 áreas principais**:

- **Amigos e Familiares**: a forma como você se relaciona com pessoas próximas, o diálogo, o apoio e a resolução de conflitos.
- **Lazer**: o tempo e a qualidade das atividades que te relaxam e te divertem.
- **Vida Financeira**: sua capacidade de suprir necessidades, planejar e viver com tranquilidade financeira.
- **Intelecto**: sua busca por conhecimento, educação continuada e satisfação com o aprendizado.
- **Espiritualidade**: a coerência entre seus valores, sua fé e sua força interior.
- **Amor**: a qualidade dos seus vínculos afetivos, respeito mútuo, planos em conjunto e companheirismo.
- **Trabalho e Carreira**: motivação com sua trajetória, ambiente profissional e senso de propósito.
- **Saúde**: seus cuidados físicos, emocionais e preventivos com o próprio corpo.

---

Use essa visão como ponto de partida para tomar decisões mais conscientes e equilibradas 🌱
''')

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
