
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime
import os

st.set_page_config(page_title="Roda da Vida", layout="centered", page_icon="🧭")

# Estilo visual
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f2f6fc;
            font-family: 'Segoe UI', sans-serif;
        }
        .title {
            font-size: 2.6em;
            font-weight: 700;
            color: #1a237e;
        }
        .subtitle {
            font-size: 1.2em;
            color: #3949ab;
        }
        .question {
            font-size: 1.05em;
            color: #1a237e;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>🧭 Roda da Vida</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Avaliação comportamental para reflexão pessoal</div><br>", unsafe_allow_html=True)


with st.form(key="form_nome"):
    nome = st.text_input("Digite seu nome completo para iniciar:")
    iniciar = st.form_submit_button("Iniciar Avaliação ✅")
if not nome:
    st.stop()


perguntas = [
    "Costuma refletir sobre o que realmente importa na vida?",
    "Tem momentos de silêncio, meditação ou oração que fazem sentido para você?",
    "Você se sente fisicamente bem para encarar sua rotina?",
    "Com que frequência você se alimenta e dorme de forma equilibrada?",
    "Você se sente desafiado intelectualmente no seu dia a dia?",
    "Costuma buscar novos aprendizados ou habilidades nos últimos tempos?",
    "Você costuma conversar com alguém quando precisa de apoio?",
    "Você sente que pode ser você mesmo com as pessoas próximas?",
    "Você já se envolveu com algo que impacta outras pessoas positivamente?",
    "Você acredita que faz diferença no ambiente onde está inserido?",
    "Você se sente útil ou valorizado(a) naquilo que faz hoje?",
    "Você consegue enxergar crescimento ou progresso em sua ocupação atual?",
    "Nos últimos dias, você teve algum tempo só para você?",
    "Você conseguiu fazer algo só porque gosta, sem obrigação?",
    "Você sente que tem controle sobre o quanto gasta e economiza?",
    "Suas finanças têm atrapalhado ou limitado suas escolhas recentes?"
]

respostas = []
if nome:
    with st.form(key="formulario"):
        for i, pergunta in enumerate(perguntas):
            st.markdown(f"<div class='question'>{i+1}. {pergunta}</div>", unsafe_allow_html=True)
            resposta = st.slider("", 0, 10, 5, key=i)
            respostas.append(resposta)
        submit = st.form_submit_button("Finalizar")

    if submit:
        st.success("✅ Avaliação concluída com sucesso!")

        aspectos = [
            "Espiritualidade",
            "Saúde",
            "Intelecto",
            "Relacionamentos",
            "Contribuição",
            "Profissão",
            "Lazer",
            "Finanças"
        ]
        medias = [round((respostas[i] + respostas[i+1]) / 2, 1) for i in range(0, len(respostas), 2)]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=medias + [medias[0]],
            theta=aspectos + [aspectos[0]],
            fill='toself',
            name='Roda da Vida'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 10])
            ),
            showlegend=False,
            margin=dict(l=30, r=30, t=30, b=30)
        )
        st.subheader(f"📊 Resultado da Roda da Vida - {nome}")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("🧩 Sobre a Roda da Vida"):
            st.markdown("[Acesse a fonte do conteúdo aqui](https://www.ibccoaching.com.br/portal/coaching/conheca-ferramenta-roda-vida-coaching/)")
            st.markdown("""
**A história da Roda da Vida**

A felicidade plena depende de diversos fatores de nossa vida, como a maneira que nos vemos, como são nossos relacionamentos, como lidamos com nossas carreiras, como nos portamos diante do mundo.

Pensando nisso, os Hindus chegaram à conclusão de que era necessário ter um sistema no qual a pessoa pudesse avaliar cada parte importante de sua vida para entender quais pontos estão satisfatórios e quais precisam de atenção. Assim foi criada a Roda da Vida, uma técnica de avaliação pessoal separada em setores essenciais para encontrarmos um equilíbrio pessoal.

**Componentes Avaliados:**
- Amigos e Familiares
- Lazer
- Vida Financeira
- Intelecto
- Espiritualidade
- Amor
- Trabalho e Carreira
- Saúde
""")

        # Geração automática, sem reset do app\ngerar_pdf = True
        if True:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Roda da Vida - Avaliação Comportamental", ln=True, align="C")
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, f"Nome: {nome}", ln=True)
            pdf.cell(0, 10, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
            pdf.ln(5)
            for asp, val in zip(aspectos, medias):
                pdf.cell(0, 10, f"{asp}: {val}", ln=True)
            pdf_output_path = f"roda_da_vida_{nome.replace(' ', '_')}.pdf"
            pdf.output(pdf_output_path)
            with open(pdf_output_path, "rb") as f:
                st.download_button("📥 Baixar PDF", f, file_name=pdf_output_path)
            os.remove(pdf_output_path)
