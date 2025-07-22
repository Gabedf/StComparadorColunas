import streamlit as st
import pandas as pd

st.title('Comparador de :blue[colunas]!')
st.markdown('Seu facilitador de vida quando... Precisar comparar os nomes :sunglasses:')

st.markdown('### Passo 1: Escolher nome das colunas')
st.markdown('Selecione os arquivos que deseja comparar _(eles devem conter uma coluna de nomes)_.')

col1, col2 = st.columns(2)
with col1:
    colunaA = st.text_input('Coluna A', placeholder='Ex: Coluna A')
with col2:
    colunaB = st.text_input('Coluna B', placeholder='Ex: Coluna B')

if colunaA != '' and colunaB != '':
    file = st.file_uploader('Selecione o arquivo A', type=['csv', 'xlsx'])

    if file is not None:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)

        if colunaA not in df.columns or colunaB not in df.columns:
            st.error("As colunas informadas não existem no arquivo.")
        else:
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
