{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "1721320c",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import streamlit as st\n",
    "import base64\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "160bbf14",
   "metadata": {},
   "outputs": [
    {
     "ename": "SyntaxError",
     "evalue": "invalid syntax (Temp/ipykernel_12676/2667418340.py, line 87)",
     "output_type": "error",
     "traceback": [
      "\u001b[1;36m  File \u001b[1;32m\"C:\\Users\\Joao\\AppData\\Local\\Temp/ipykernel_12676/2667418340.py\"\u001b[1;36m, line \u001b[1;32m87\u001b[0m\n\u001b[1;33m    streamlit run Untitled.py\u001b[0m\n\u001b[1;37m              ^\u001b[0m\n\u001b[1;31mSyntaxError\u001b[0m\u001b[1;31m:\u001b[0m invalid syntax\n"
     ]
    }
   ],
   "source": [
    "st.title('Geradora DMPL - Britech')\n",
    "\n",
    "uploaded_file = st.file_uploader('Selecione um arquivo', type=['csv', 'txt','xls'])\n",
    "\n",
    "if uploaded_file is not None:\n",
    "    # Ler os dados do arquivo\n",
    "    data = uploaded_file.read()\n",
    "    st.write('Dados do arquivo:')\n",
    "    st.write(data)\n",
    "\n",
    "    \n",
    "relatorio_his = pd.read_excel('ReportHistoricoCota.xls')\n",
    "relatorio_mov = pd.read_excel('ReportMovimentacaoCotista.xls')\n",
    "\n",
    "hist_cota_df = pd.DataFrame(relatorio_his)\n",
    "mov_cotista_df = pd.DataFrame(relatorio_mov)\n",
    "\n",
    "hist_cota = pd.DataFrame(hist_cota_df)\n",
    "mov_cotista = pd.DataFrame(mov_cotista_df)\n",
    "\n",
    "# Selecionando apenas as colunas que irão ser utilizadas em ambos os relatórios\n",
    "\n",
    "hist_cota = hist_cota_df[['Unnamed: 1', 'Unnamed: 10','Unnamed: 15', 'Unnamed: 17']]\n",
    "mov_cotista = mov_cotista_df[['Unnamed: 5', 'Unnamed: 18','Unnamed: 11','Unnamed: 20','Unnamed: 22']]\n",
    "\n",
    "# Removendo os valores duplicados\n",
    "\n",
    "mov_cotista=mov_cotista.dropna()\n",
    "\n",
    "# Removendo os valores duplicados\n",
    "\n",
    "hist_cota=hist_cota.dropna()\n",
    "\n",
    "# Juntando a coluna do Mov_cotista de Valor Bruto e IR, por conta do Come Cotas\n",
    "# Converter as colunas para o tipo numerico\n",
    "\n",
    "mov_cotista['Unnamed: 20'] = pd.to_numeric(mov_cotista['Unnamed: 20'], errors='coerce')\n",
    "mov_cotista['Unnamed: 22'] = pd.to_numeric(mov_cotista['Unnamed: 22'], errors='coerce')\n",
    "\n",
    "\n",
    "mov_cotista['Soma'] = mov_cotista['Unnamed: 20'] + mov_cotista['Unnamed: 22']\n",
    "\n",
    "# Criação dos filtros que irao dar as saidas respectivas\n",
    "\n",
    "aplic = [\"Aplicação\", \"Aplicacão Cotas Especial\",\"Depósito\",\"Entrada\"]\n",
    "resg = [\"Resgate Cotas Especial\",\"Resgate\", \"Come Cotas\", \"Resgate líquido\",\"Retirada\"]\n",
    "amort = [\"Amortização\", \"Juros\"]\n",
    "\n",
    "# Armazendo os filtros em data frames\n",
    "\n",
    "aplicacoes = mov_cotista[mov_cotista['Unnamed: 11'].isin(aplic)]\n",
    "resgates = mov_cotista[mov_cotista['Unnamed: 11'].isin(resg)]\n",
    "amortizacoes = mov_cotista[mov_cotista['Unnamed: 11'].isin(amort)]\n",
    "\n",
    "# Calulando a soma do montante em R$ dos filtros acima\n",
    "\n",
    "soma_valor_aplicacoes = aplicacoes['Soma'].sum()\n",
    "soma_valor_resgates = resgates['Soma'].sum()\n",
    "soma_valor_amortizacoes = amortizacoes['Soma'].sum()\n",
    "\n",
    "# Calculando a soma da quantidade dos filtros acima\n",
    "\n",
    "soma_qtde_aplicacoes = aplicacoes['Unnamed: 18'].sum()\n",
    "soma_qtde_resgates = resgates['Unnamed: 18'].sum()\n",
    "soma_qtde_amortizacoes = amortizacoes['Unnamed: 18'].sum()\n",
    "\n",
    "# Criação do data frame para exportação\n",
    "\n",
    "dmpl_df = pd.DataFrame(columns=['Operação','Quantidade','Valores'])\n",
    "\n",
    "dmpl_df = dmpl_df.append({'Operação':'Aplicações','Quantidade':soma_qtde_aplicacoes,'Valores':soma_valor_aplicacoes}, ignore_index=True)\n",
    "dmpl_df = dmpl_df.append({'Operação':'Resgates','Quantidade':soma_qtde_resgates,'Valores':soma_valor_resgates}, ignore_index=True)\n",
    "dmpl_df = dmpl_df.append({'Operação':'Amortizações','Quantidade':soma_qtde_amortizacoes,'Valores':soma_valor_amortizacoes}, ignore_index=True)\n",
    "\n",
    " \n",
    "caminho_arquivo = 'C:\\\\Users\\\\Joao\\\\Documents\\\\Python\\\\Gerador DMPL - Britech.xlsx'\n",
    "dmpl_df.to_excel(excel_writer=caminho_arquivo, index=False)\n",
    "\n",
    "with open(caminho_arquivo, \"rb\") as file:\n",
    "    excel_data = file.read()\n",
    "    b64 = base64.b64encode(excel_data).decode()\n",
    "    \n",
    "\n",
    "href = f'<a href=\"data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}\" download=\"dataframe.xlsx\">Baixar DataFrame</a>'\n",
    "st.markdown(href, unsafe_allow_html=True)\n",
    "\n",
    "streamlit run Untitled.py\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "188a0716",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "27230f03",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
