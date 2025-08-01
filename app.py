import streamlit as st
import pandas as pd

colunaA = None
colunaB = None

st.title('Comparador de :blue[colunas]!')
st.markdown('Seu facilitador de vida quando... Precisar comparar os nomes :sunglasses:')

st.markdown('### Passo 1: Selecione o arquivo')

file = st.file_uploader('Selecione o arquivo A', type=['csv', 'xlsx'])

if file is not None:
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        df = pd.read_excel(file)

    st.markdown('### Passo 2: Escolha as colunas a serem comparadas')
    col1, col2 = st.columns([1, 1])
    with col1:
        colunaA = st.selectbox(
            label='Coluna A',
            options=['SELECIONE'] + df.columns.tolist(),
            placeholder='Ex: Coluna A'
        )
    with col2:
        colunaB = st.selectbox(
            label='Coluna B',
            options=['SELECIONE'] + df.columns.tolist(),
            placeholder='Ex: Coluna B'
        )

if (colunaA is not None and colunaA != 'SELECIONE') and (colunaB is not None and colunaB != 'SELECIONE'):
        nomesA = df[colunaA].dropna().astype(str).tolist()
        nomesB = df[colunaB].dropna().astype(str).tolist()

        # Pegando os nomes que estão em A e não estão em B
        diferentes = [nome for nome in nomesA if nome not in nomesB]

        if diferentes:
            st.markdown(f"**{len(diferentes)} nomes encontrados apenas na Coluna A:**")
            for nome in diferentes:
                st.write(f"- {nome}")

            # Criando conteúdo do arquivo .txt
            txt_conteudo = "\n".join(diferentes)
            txt_bytes = txt_conteudo.encode("utf-8")

            # Botão para baixar o arquivo
            st.download_button(
                label="📥 Baixar nomes faltantes da Coluna B (.txt)",
                data=txt_bytes,
                file_name="nomes_exclusivos_colunaA.txt",
                mime="text/plain"
            )
        else:
            st.success("Todos os nomes da Coluna A estão presentes na Coluna B!")