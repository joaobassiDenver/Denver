import streamlit as st
import pandas as pd
import base64
import tempfile
import openpyxl
import io
import xlrd
import numpy as np

st.title('Geradora DMPL')

st.image('https://th.bing.com/th/id/R.592a9b01eb077958f53aa385dc40f1d5?rik=ESxDzIaUACogwg&pid=ImgRaw&r=0')

opcoes = ['Vórtx', 'ID Corretora']

adm = st.selectbox('Selecione o administrador: ', opcoes)

if adm == 'Vórtx':
    mov_doc = st.file_uploader(
        'Selecione o Razão de investidores',
        type=['xls', 'xlsx', 'csv']
    )

    hist_doc = st.file_uploader(
        'Selecione o Rentabilidade sintética',
        type=['xls', 'xlsx', 'csv']
    )
elif adm == 'ID Corretora':
    mov_doc = st.file_uploader(
        'Selecione o Movimentação cotista',
        type=['xls', 'xlsx', 'csv']
    )

    hist_doc = st.file_uploader(
        'Selecione o Histórico Cota',
        type=['xls', 'xlsx', 'csv']
    )

#Filtros
aplic = ["Aplicação", "Aplicacão Cotas Especial","Depósito","Entrada","Estorno Aplicação"]
resg = ["Resgate Cotas Especial","Resgate", "Come Cotas", "Resgate líquido","Retirada","Estorno Resgate"]
amort = ["Amortização", "Juros"]
distr = ["Distribuição","OUTRA COISA"]

# Tratamento por adm
if mov_doc is not None and hist_doc is not None:
    if adm == 'Vórtx':
        mov = pd.read_csv(mov_doc, encoding='ISO-8859-1', delimiter=';')
        mov = pd.DataFrame(mov)

        file_path = "./temp.csv"
        with open(file_path, "wb") as f:
            f.write(hist_doc.read())

        data = pd.read_csv(file_path, encoding="ISO-8859-1", delimiter=";")

        header = data.iloc[-1]

        hist = pd.read_csv(file_path, encoding="ISO-8859-1", delimiter=";", header=None, names=header)

        hist = hist[:-1]

        mov = mov[['Unnamed: 11','Unnamed: 13','Unnamed: 7','Unnamed: 12']]
        mov = mov.dropna()
        mov.replace(['A','Aplicação'], 'Aplicação', inplace=True)
        mov.replace(['AA','Aplicação'], 'Aplicação', inplace=True)
        mov.replace(['EA','Estorno Aplicação'], 'Estorno Aplicação', inplace=True)
        mov.replace(['AC','Amortização'], 'Amortização', inplace=True)
        mov.replace(['DR','Distribuição'], 'Distribuição', inplace=True)
        mov.replace(['R','Resgate'], 'Resgate', inplace=True)
        mov.replace(['R9','Resgate'], 'Resgate', inplace=True)
        mov.replace(['RA','Resgate'], 'Resgate', inplace=True)
        mov.replace(['ER','Estorno Resgate'], 'Estorno Resgate', inplace=True)
        mov.replace(['RP','Resgate'], 'Resgate', inplace=True)

        mov['Unnamed: 13'] = np.where(mov['Unnamed: 7'] == 'Estorno Aplicação', -1 * mov['Unnamed: 13'], mov['Unnamed: 13'])
        mov['Unnamed: 12'] = np.where(mov['Unnamed: 7'] == 'Estorno Resgate', -1 * mov['Unnamed: 12'], mov['Unnamed: 12'])

        mov['Unnamed: 13'] = np.where(mov['Unnamed: 7'] == 'Estorno Aplicação', -1 * mov['Unnamed: 13'], mov['Unnamed: 13'])
        mov['Unnamed: 12'] = np.where(mov['Unnamed: 7'] == 'Estorno Resgate', -1 * mov['Unnamed: 12'], mov['Unnamed: 12'])

        mov_new_name = {'Unnamed: 11':'Data',
            'Unnamed: 13':'Quantidade',
            'Unnamed: 7': 'Operação',
            'Unnamed: 12':'Valor'  
        }
        mov = mov.rename(columns=mov_new_name)

        mov=mov.drop(mov.tail(1).index)
        mov = mov.drop(mov.index[0])

        mov['Quantidade']=mov['Quantidade'].str.replace('(?<=\d)\.(?=\d)', '', regex=True).str.replace(',', '.')
        mov['Quantidade'] = pd.to_numeric(mov['Quantidade'], errors='coerce')

        mov['Valor']=mov['Valor'].str.replace('(?<=\d)\.(?=\d)', '', regex=True).str.replace(',', '.')
        mov['Valor'] = pd.to_numeric(mov['Valor'], errors='coerce')

        hist.reset_index(drop = True, inplace = True)

        hist = hist[:-1]

        hist = hist.dropna()

        hist = hist[['DataRef','ValCota','NCotas','PL']]
        
        hist_new_name = {'DataRef':'Data',
            'ValCota':'Valor',
            'NCotas': 'Quantidade',
            'PL':'Patrimônio líquido'
        }

        hist = hist.rename(columns=hist_new_name)

        hist['Quantidade']=hist['Quantidade'].str.replace('(?<=\d)\.(?=\d)', '', regex=True).str.replace(',', '.')
        hist['Quantidade'] = pd.to_numeric(hist['Quantidade'], errors='coerce')

        hist['Valor']=hist['Valor'].str.replace('(?<=\d)\.(?=\d)', '', regex=True).str.replace(',', '.')
        hist['Valor'] = pd.to_numeric(hist['Valor'], errors='coerce')

        hist['Patrimônio líquido']=hist['Patrimônio líquido'].str.replace('(?<=\d)\.(?=\d)', '', regex=True).str.replace(',', '.')
        hist['Patrimônio líquido'] = pd.to_numeric(hist['Patrimônio líquido'], errors='coerce')

        hist = hist[hist['Quantidade']!=0]

        hist['Data'] = pd.to_datetime(hist['Data'], format = '%d/%m/%Y')
        hist['Data'] = pd.to_datetime(hist['Data'])        
    elif adm == 'ID Corretora':
        mov = pd.read_excel(mov_doc)
        mov = pd.DataFrame(mov)
        hist = pd.read_excel(hist_doc)
        hist = pd.DataFrame(hist)

        mov = mov[['Unnamed: 5', 'Unnamed: 18','Unnamed: 11','Unnamed: 20','Unnamed: 22']]
        mov = mov.dropna()
        mov['Unnamed: 20'] = pd.to_numeric(mov['Unnamed: 20'], errors='coerce')
        mov['Unnamed: 22'] = pd.to_numeric(mov['Unnamed: 22'], errors='coerce')
        mov['Soma'] = mov['Unnamed: 20'] + mov['Unnamed: 22']
        mov_new_name = {'Unnamed: 5':"Data",
                            'Unnamed: 18': 'Quantidade',
                            'Unnamed: 11': 'Operação',
                            'Soma': 'Valor'
        }     

        mov = mov.rename(columns=mov_new_name)
        mov = mov.drop(mov.columns[[3,4]],axis=1)

        hist = hist[['Unnamed: 1','Unnamed: 17', 'Unnamed: 15','Unnamed: 10']]
        hist = hist.dropna()
        hist = hist.drop(hist.index[0])
        hist_new_name = {'Unnamed: 1':'Data',
                    'Unnamed: 17':'Valor',
                    'Unnamed: 15':'Quantidade',
                    'Unnamed: 10':'Patrimônio líquido' 
        }
        hist = hist.rename(columns=hist_new_name)
        hist['Data'] = pd.to_datetime(hist['Data']) 

    # Código em si
    aplicacoes = mov[mov['Operação'].isin(aplic)]
    resgates = mov[mov['Operação'].isin(resg)]
    amortizacoes = mov[mov['Operação'].isin(amort)]
    distribuicoes = mov[mov['Operação'].isin(distr)]

    # Calulando a soma do montante em R$ dos filtros acima

    soma_valor_aplicacoes = aplicacoes['Valor'].sum()
    soma_valor_resgates = resgates['Valor'].sum()
    soma_valor_amortizacoes = amortizacoes['Valor'].sum()
    soma_valor_distribuicoes = distribuicoes['Valor'].sum()

    # Calculando a soma da quantidade dos filtros acima

    soma_qtde_aplicacoes = aplicacoes['Quantidade'].sum()
    soma_qtde_resgates = resgates['Quantidade'].sum()
    soma_qtde_amortizacoes = amortizacoes['Quantidade'].sum()
    soma_qtde_distribuicoes = distribuicoes['Quantidade'].sum()

    # Criação do data frame para exportação

    dmpl_df = pd.DataFrame(columns=['Operação','Quantidade','Valores'])

    dmpl_df = pd.concat([dmpl_df, pd.DataFrame({'Operação': ['Aplicações', 'Resgates', 'Amortizações', 'Distribuições'],
                                            'Quantidade': [soma_qtde_aplicacoes, soma_qtde_resgates, soma_qtde_amortizacoes, soma_qtde_distribuicoes],
                                            'Valores': [soma_valor_aplicacoes, soma_valor_resgates, soma_valor_amortizacoes, soma_valor_distribuicoes]})], ignore_index=True)
        
    filtro_aplic = mov[mov['Operação'].isin(aplic)]
    filtro_aplic = filtro_aplic[['Data', 'Valor']]

    filtro_resg = mov[mov['Operação'].isin(resg)]
    filtro_resg = filtro_resg[['Data', 'Valor']]

    filtro_amort = mov[mov['Operação'].isin(amort)]
    filtro_amort = filtro_amort[['Data', 'Valor']]

    filtro_distr = mov[mov['Operação'].isin(distr)]
    filtro_distr = filtro_distr[['Data', 'Valor']]

    filtro_aplic['Data'] = pd.to_datetime(filtro_aplic['Data'])
    filtro_resg['Data'] = pd.to_datetime(filtro_resg['Data'])
    filtro_amort['Data'] = pd.to_datetime(filtro_amort['Data'])
    filtro_distr['Data'] = pd.to_datetime(filtro_distr['Data'])

    filtro_aplic.rename(columns={'Valor': 'Aplicação'}, inplace=True)
    filtro_resg.rename(columns={'Valor': 'Resgates'}, inplace=True)
    filtro_amort.rename(columns={'Valor': 'Amortização'}, inplace=True)
    filtro_distr.rename(columns={'Valor': 'Distribuição'}, inplace=True)

    filtro_aplic = filtro_aplic.groupby('Data').sum()
    filtro_resg = filtro_resg.groupby('Data').sum()
    filtro_amort = filtro_amort.groupby('Data').sum()
    filtro_distr = filtro_distr.groupby('Data').sum()

    hist = pd.merge(hist, filtro_aplic, on='Data', how='left')
    hist['Aplicação'] = hist['Aplicação'].fillna(0)

    hist = pd.merge(hist, filtro_resg, on='Data', how='left')
    hist['Resgates'] = hist['Resgates'].fillna(0)

    hist = pd.merge(hist, filtro_amort, on='Data', how='left')
    hist['Amortização'] = hist['Amortização'].fillna(0)

    hist = pd.merge(hist, filtro_distr, on='Data', how='left')
    hist['Distribuição'] = hist['Distribuição'].fillna(0)

    hist['Amort/Distr por cota'] = (hist['Amortização'] + hist['Distribuição']) / hist['Quantidade']

    for a in range(0,len(hist)):
        hist.at[a,'Nova cota'] = hist.at[a,'Amort/Distr por cota'] + hist.at[a,'Valor']

    for i in range(1, len(hist)):
        if hist.at[i, 'Amort/Distr por cota'] <= 0:
            hist.at[i, 'Rentabilidade diária'] = hist.at[i, 'Valor'] / hist.at[i-1, 'Valor'] - 1
        elif hist.at[i, 'Amort/Distr por cota'] > 0:
            hist.at[i, 'Rentabilidade diária'] = hist.at[i, 'Nova cota'] / hist.at[i-1, 'Nova cota'] - 1

    hist['Rentabilidade acumulada'] = 0

    hist['Cota teórica'] = 0
    hist.at[0, 'Cota teórica'] = hist.at[0, 'Nova cota']

    for valores in range(1, len(hist)):
        hist.at[valores, 'Cota teórica'] = hist.at[valores-1, 'Cota teórica'] + (hist.at[valores-1, 'Cota teórica'] * hist.at[valores, 'Rentabilidade diária'])

    hist['Rentabilidade acumulada'] = (1 + hist['Rentabilidade diária']).cumprod() - 1

    hist['Resultado'] = 0

    for contador in range(1, len(hist)):
        hist.at[contador, 'Resultado'] = hist.at[contador, 'Patrimônio líquido'] \
                                     - hist.at[contador - 1, 'Patrimônio líquido'] \
                                     - hist.at[contador, 'Aplicação'] \
                                     + hist.at[contador, 'Resgates'] \
                                     + hist.at[contador, 'Amortização'] \
                                     + hist.at[contador, 'Distribuição']

    # Download dos arquivos
    def download_excel(df):
        output = io.BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        return output
     
    download_link = download_excel(hist)
    st.markdown(download_link, unsafe_allow_html=True)

    st.download_button("Download Rentabilidade", data=download_link, file_name='Rentabilidade.xlsx', 
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    download_link = download_excel(dmpl_df)
    st.markdown(download_link, unsafe_allow_html=True)

    st.download_button("Download DMPL", data=download_link, file_name='DMPL.xlsx', 
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    #st.download_button("Download Anexo", data=download_link, file_name='Anexo_DF.xlsx', 
    #mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
