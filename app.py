import streamlit as st
import pandas as pd
import base64
import tempfile
import openpyxl
import io

st.title('Geradora DMPL - Britech')

st.image('https://th.bing.com/th/id/R.592a9b01eb077958f53aa385dc40f1d5?rik=ESxDzIaUACogwg&pid=ImgRaw&r=0')

mov_cotista = st.file_uploader(
    'Selecione o Movimentação Cotista',
    type = ['xls','xlsx']
)

if mov_cotista:

    relatorio_mov = pd.read_excel(mov_cotista)

    mov_cotista_df = pd.DataFrame(relatorio_mov)

    mov_cotista = mov_cotista_df[['Unnamed: 5', 'Unnamed: 18','Unnamed: 11','Unnamed: 20','Unnamed: 22']]

    mov_cotista=mov_cotista.dropna()

    mov_cotista['Unnamed: 20'] = pd.to_numeric(mov_cotista['Unnamed: 20'], errors='coerce')

    mov_cotista['Unnamed: 22'] = pd.to_numeric(mov_cotista['Unnamed: 22'], errors='coerce')

    mov_cotista['Soma'] = mov_cotista['Unnamed: 20'] + mov_cotista['Unnamed: 22']

    aplic = ["Aplicação", "Aplicacão Cotas Especial","Depósito","Entrada"]
    resg = ["Resgate Cotas Especial","Resgate", "Come Cotas", "Resgate líquido","Retirada"]
    amort = ["Amortização", "Juros"]

    aplicacoes = mov_cotista[mov_cotista['Unnamed: 11'].isin(aplic)]
    resgates = mov_cotista[mov_cotista['Unnamed: 11'].isin(resg)]
    amortizacoes = mov_cotista[mov_cotista['Unnamed: 11'].isin(amort)]

    # Calulando a soma do montante em R$ dos filtros acima

    soma_valor_aplicacoes = aplicacoes['Soma'].sum()
    soma_valor_resgates = resgates['Soma'].sum()
    soma_valor_amortizacoes = amortizacoes['Soma'].sum()

    # Calculando a soma da quantidade dos filtros acima

    soma_qtde_aplicacoes = aplicacoes['Unnamed: 18'].sum()
    soma_qtde_resgates = resgates['Unnamed: 18'].sum()
    soma_qtde_amortizacoes = amortizacoes['Unnamed: 18'].sum()
    
    dmpl_df = pd.DataFrame(columns=['Operação','Quantidade','Valores'])

    nova_linha_aplicacoes = {'Operação':'Aplicações', 'Quantidade':soma_qtde_aplicacoes, 'Valores':soma_valor_aplicacoes}
    nova_linha_resgates = {'Operação':'Resgates', 'Quantidade':soma_qtde_resgates, 'Valores':soma_valor_resgates}
    nova_linha_amortizacoes = {'Operação':'Amortizações', 'Quantidade':soma_qtde_amortizacoes, 'Valores':soma_valor_amortizacoes}

    dmpl_df = pd.concat([dmpl_df, pd.DataFrame([nova_linha_aplicacoes])], ignore_index=True)
    dmpl_df = pd.concat([dmpl_df, pd.DataFrame([nova_linha_resgates])], ignore_index=True)
    dmpl_df = pd.concat([dmpl_df, pd.DataFrame([nova_linha_amortizacoes])], ignore_index=True)

    def download_excel(df):
        output = io.BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        return output

    if st.button('Gerar DMPL'):
        # Código para gerar o DataFrame dmpl_df
        
        st.dataframe(dmpl_df)
        
        download_link = download_excel(dmpl_df)
        st.markdown(download_link, unsafe_allow_html=True)

        st.download_button("Download DMPL", data=download_link, file_name='DMPL.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

