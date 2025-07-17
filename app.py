import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO

st.title("📊 Comparativo de Pendentes e Finalizadas")

st.write("Cole as tarefas **pendentes** e **finalizadas** em caixas separadas. Cada linha deve ser `Tarefa: número`")

# Campo para pendentes
pendentes_text = st.text_area("📌 Tarefas PENDENTES:", height=250, value=
"""Acordo com Sindicato: 38
Acordos Judiciais: 1
Agravo de Instrumento: 33
Apelação: 29
Atualizar documentos: 204
Audiência de Conciliação: 33
Audiência Instrução: 7
Boas Vindas/Coleta de documentos: 1647
Cálculo: 1248""")

# Campo para finalizadas
finalizadas_text = st.text_area("✅ Tarefas FINALIZADAS:", height=250, value=
"""Acordo com Sindicato: 12
Acordos Judiciais: 5
Agravo de Instrumento: 8
Apelação: 15
Atualizar documentos: 50
Audiência de Conciliação: 20
Audiência Instrução: 3
Boas Vindas/Coleta de documentos: 800
Cálculo: 500""")

def texto_para_dict(texto):
    dados = {}
    for linha in texto.strip().split("\n"):
        if ":" in linha:
            chave, valor = linha.split(":", 1)
            try:
                dados[chave.strip()] = int(valor.strip())
            except:
                dados[chave.strip()] = 0
    return dados

# Converter os textos para dicionários
dados_pendentes = texto_para_dict(pendentes_text)
dados_finalizadas = texto_para_dict(finalizadas_text)

def gerar_grafico(dados, titulo):
    # Cria DataFrame e ORDENA ALFABETICAMENTE pela Tarefa
    df = pd.DataFrame(list(dados.items()), columns=["Tarefa", "Quantidade"])
    df_sorted = df.sort_values(by="Tarefa")  # <-- ORDENA PELO NOME, NÃO PELO NÚMERO

    fig, ax = plt.subplots(figsize=(10, len(df)//2))
    bars = ax.barh(df_sorted["Tarefa"], df_sorted["Quantidade"], color="skyblue")

    for bar in bars:
        width = bar.get_width()
        ax.text(width + max(df_sorted["Quantidade"])*0.01,
                bar.get_y() + bar.get_height()/2,
                str(int(width)), va='center')

    ax.set_xlabel("Quantidade")
    ax.set_ylabel("Tarefa")
    ax.set_title(titulo)
    plt.tight_layout()
    return fig

def salvar_pdf(fig):
    buf = BytesIO()
    fig.savefig(buf, format="PDF")
    return buf

# Mostrar gráficos e botões
if dados_pendentes:
    st.subheader("📌 Gráfico de Tarefas Pendentes")
    fig_pendentes = gerar_grafico(dados_pendentes, "Pendentes (Ordenado A-Z)")
    st.pyplot(fig_pendentes)

    buf_pendentes = salvar_pdf(fig_pendentes)
    st.download_button(
        label="📥 Baixar gráfico Pendentes (PDF)",
        data=buf_pendentes.getvalue(),
        file_name="grafico_pendentes.pdf",
        mime="application/pdf"
    )

if dados_finalizadas:
    st.subheader("✅ Gráfico de Tarefas Finalizadas")
    fig_finalizadas = gerar_grafico(dados_finalizadas, "Finalizadas (Ordenado A-Z)")
    st.pyplot(fig_finalizadas)

    buf_finalizadas = salvar_pdf(fig_finalizadas)
    st.download_button(
        label="📥 Baixar gráfico Finalizadas (PDF)",
        data=buf_finalizadas.getvalue(),
        file_name="grafico_finalizadas.pdf",
        mime="application/pdf"
    )
