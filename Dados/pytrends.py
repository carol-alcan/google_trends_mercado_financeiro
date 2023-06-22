# -*- coding: utf-8 -*-
"""pytrends.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1w63nsOOZd7-40avtJ4TFGb6hJRZdZ0hu
"""

!pip install vectorbt
!pip install pytrends

from pytrends.request import TrendReq
import yfinance as yf
import vectorbt as vbt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import datetime

pytrends = TrendReq(hl= 'pt-BR', tz = 360)

termos = ['petrobras', 'dólar']

pytrends.build_payload(termos, cat=0, timeframe= 'all', geo = 'BR', gprop= '')
busca = pytrends.interest_over_time()

busca.head()

busca[['petrobras', 'dólar']].plot();

pytrends = TrendReq(hl= 'pt-BR', tz = 360)
lista_termos = ['petrobras', 'dólar', 'PETR4', 'VAL3', 'bitcoin']
pytrends.build_payload(lista_termos, cat=0, timeframe= '2008-12-14 2023-06-14', geo = 'BR', gprop= '')
busca = pytrends.interest_over_time()
busca[lista_termos].plot(figsize = (10,6));

"""1.2 Cruzamento das informações do Google Trends com Mercado Financeiro

1.2.1 Pré-processamento do dado
"""

busca.index.name = 'Date'

busca.head()

busca.shape

busca.index = pd.to_datetime(busca.index)

busca.head()

busca.index[0].strftime("%Y-%m-%d")

from yfinance.utils import auto_adjust

"""Extração das cotações"""

dolar = yf.download('USDBRL=X', start = busca.index[0].strftime("%Y-%m-%d"),auto_adjust= True)

dolar.index = pd.to_datetime(dolar.index)

pd.merge(busca, dolar, how = 'inner', on = 'Date')

total = pd.merge(busca, dolar, how = 'inner', on = 'Date')[['dólar', 'Close']]

"""1.2.2 Plotagem da informação"""

fig, ax1 = plt.subplots(figsize = (8,5))

color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('Buscas por Dólar', color=color)
ax1.plot(busca.index, busca['dólar'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2=ax1.twinx()#Configurar um outro eixo vertical que compartilha o mesmo eixo x

color = 'tab:blue'
ax2.set_ylabel('Cotação do Dólar', color=color)
ax2.plot(dolar.index, dolar['Close'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.show()

fig, ax1 = plt.subplots(figsize = (8,5))

color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('Buscas por Dólar', color=color)
ax1.plot(total.index, total['dólar'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2=ax1.twinx()#Configurar um outro eixo vertical que compartilha o mesmo eixo x

color = 'tab:blue'
ax2.set_ylabel('Cotação do Dólar', color=color)
ax2.plot(total.index, total['Close'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.show()

import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y":True}]])

#Add traces
fig.add_trace(
    go.Scatter(x= busca.index, y= busca['dólar'], name="Busca pelo dólar"),
    secondary_y= True
)

fig.add_trace(
    go.Scatter(x= dolar.index, y= dolar['Close'], name="Cotação do dólar"),
    secondary_y= False
)

#Add figure title
fig.update_layout(
    title_text= "Buscas no google vs. cotação"
)

#Set x-axis title
fig.update_xaxes(title_text="Date")

#Set y axis titles
fig.update_yaxes(title_text="<b>primary</b> Buscas no google", secondary_y=False)
fig.update_yaxes(title_text="<b>primary</b> Cotação do dólar", secondary_y=True)

fig.show()

"""1.2.3 Comparativo de ações"""

pytrends = TrendReq(hl= 'pt-BR', tz = 360)
acoes = ['PETR4', 'MGLU3', 'ITUB4', 'AMER3', 'VALE3']
pytrends.build_payload(acoes, cat=0, timeframe= '2018-12-14 2023-06-14', geo = 'BR', gprop= '')
busca_acoes = pytrends.interest_over_time()
busca_acoes[acoes].plot(figsize = (10,6));

"""1.2.4 Petrobras vs. PETR4"""

pytrends = TrendReq(hl= 'pt-BR', tz = 360)
termos = ['PETR4', 'petrobras']
pytrends.build_payload(termos, cat=0, timeframe= 'today 5-y', geo = 'BR', gprop= '')
busca_petro = pytrends.interest_over_time()
busca_petro[termos].plot(figsize = (10,6));

busca_petro.head()

busca_petro.index.name='Date'

busca_petro.head()

busca_petro.shape

busca_petro.index= pd.to_datetime(busca_petro.index)

busca_petro.head()

busca_petro.index[0].strftime("%Y-%m-%d")

petro = yf.download('PETR4.SA',start = busca_petro.index[0].strftime("%Y-%m-%d"), auto_adjust = True)

petro.index = pd.to_datetime(petro.index)

#Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y":True}]])

#Add traces
fig.add_trace(
    go.Scatter(x= busca_petro.index, y= busca_petro['petrobras'], name="Busca por Petrobras"),
    secondary_y= False
)

fig.add_trace(
    go.Scatter(x= busca_petro.index, y= busca_petro['PETR4'], name="Busca por PETR4"),
    secondary_y= False
)

fig.add_trace(
    go.Scatter(x= petro.index, y= petro['Close'], name="Cotação do PETR4"),
    secondary_y= True
)

#Add figure title
fig.update_layout(
    title_text= "Cotação de PETR4 vs. buscas no google"
)

#Set x-axis title
fig.update_xaxes(title_text="Data")

#Set y axis titles
fig.update_yaxes(title_text="<b>primary</b> Intensidade das buscas", secondary_y=False)
fig.update_yaxes(title_text="<b>secondary</b> Preço de PETR4", secondary_y=True)

fig.show()

busca_petro['busca_total'] = busca_petro['PETR4'] + busca_petro['petrobras']

#Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y":True}]])

#Add traces
fig.add_trace(
    go.Scatter(x= busca_petro.index, y= busca_petro['busca_total'], name="Busca por PETR4"),
    secondary_y= False
)

fig.add_trace(
    go.Scatter(x= petro.index, y= petro['Close'], name="Cotação do PETR4"),
    secondary_y= True
)

#Add figure title
fig.update_layout(
    title_text= "Cotação de PETR4 vs. buscas no google"
)

#Set x-axis title
fig.update_xaxes(title_text="Data")

#Set y axis titles
fig.update_yaxes(title_text="<b>primary</b> Intensidade das buscas", secondary_y=False)
fig.update_yaxes(title_text="<b>secondary</b> Preço de PETR4", secondary_y=True)

fig.show()

"""2. Explorando as funcionalidades da biblioteca

Problemas com a função "get_historical_interest" ( foi descontinuada devido a um erro que trazia os dados distorcidos. O código esta em: https://github.com/GeneralMills/pytrends)

---
"""

pytrends = TrendReq(hl = 'en-US', tz = 360)
kw_list = ['petrobras', 'dólar']

"""Função "multirange_interest_over_time"
"""

pytrends.build_payload(kw_list = ['lion', 'cat'], timeframe = ['2019-09-04 2022-09-10', '2019-09-18 2022-09-24'])
data = pytrends.multirange_interest_over_time()

data

"""Métodos gerais"""

pytrend = TrendReq(geo = 'BR')

pytrend.trending_searches(pn = 'brazil')

"""Buscas anuais"""

pytrend.top_charts(2022, hl = 'pt-BR', geo = 'BR')

"""3. Backtesting Bitcoin: trends vs. preço

3.1 Obtenção de dados
"""

pytrend = TrendReq()

termos = ['Bitcoin']

pytrend.build_payload(termos, timeframe= '2019-01-01 2023-06-15', cat = 7, geo = '')

dados_bitcoin = pytrend.interest_over_time()

dados_bitcoin

"""Cotação do Bitcoin"""

preco_btc = yf.download('BTC-USD', start = dados_bitcoin.index[0].strftime('%Y-%m-%d'), auto_adjust = True)

dados_bitcoin.index.name='Date'

dados_bitcoin.index= pd.to_datetime(dados_bitcoin.index)
preco_btc.index= pd.to_datetime(preco_btc.index)

"""3.2 Visualização de dados"""

fig, ax1 = plt.subplots(figsize = (8,5))

color = 'tab:red'
ax1.set_xlabel('Date')
ax1.set_ylabel('Buscas por Bitcoin', color = color)
ax1.plot(dados_bitcoin.index, dados_bitcoin['Bitcoin'], color = color)
ax1.tick_params(axis= 'y', labelcolor= color)

ax2 = ax1.twinx()#Configurar um outro eixo vertical que compartilha o mesmo eixo x

color = 'tab:blue'
ax2.set_ylabel('Cotação do Bitcoin', color = color)
ax2.plot(preco_btc.index, preco_btc['Close'], color = color)
ax2.tick_params(axis= 'y', labelcolor= color)

plt.show()

trends_btc = pd.merge(dados_bitcoin, preco_btc, how= 'inner', on= 'Date')[['Bitcoin', 'Close']]

trends_btc

trends_btc.index

"""Vamos normalizar os dados de preço e trends para que fique em uma unidade comparável."""

trends_btc_normalizado = trends_btc/trends_btc.iloc[0]

trends_btc_normalizado.vbt.plot().update_layout(template='simple_white', width=800, height=400,
                                                title_text='<b>Bitcoin: preço x trends',
                                                xaxis_title= "<b>Data", yaxis_title="<b>Valor normalizado").show()

"""Ao olhar para o gráfico acima, fica bem sugestivo que as duas variáveis estão caminhando juntas.

3.3 Criação e backtesting da estratégia

Para backtestar nossa teoria, poderíamos pensar em uma estratégia de comprar o ativo nos momenros onde houve aumento das pesquisas em relação aos períodos anteriores.

Nesse sentido, o desvio padrão pode ser uma ferramenta interessante para ver quanto as pesquisas estão divergindo da média.

As bandas de bollinger podem nos ajudar nessa tarefa. Elas são representadas por 3 linhas, onde:
A linha central é a média de n períodos atrás(vamos definir n como 10, ou seja, média dos últimos 10 dias).
A linha superior = média + x desvios (aui vamos definir x como 1).
A linha inferior = média - x desvios (aqui vamos definir x como 1).
OBS: Tradicionalmente as Bandas de Bollinger são o preço de 20 perídos +- 2 desvios.
"""

vbt.BBANDS.run(trends_btc['Bitcoin'], 10, alpha = 1).\
plot(template = 'simple_white', width = 800, height = 400).show()

"""Agora extraímos os valores das bandas superior e inferior para usar nos sinais de entrada."""

BBand_sup_1std = vbt.BBANDS.run(trends_btc['Bitcoin'], 10, alpha = 1).upper
BBand_inf_1std = vbt.BBANDS.run(trends_btc['Bitcoin'], 10, alpha = 1).lower

"""Criamos uma estrutura booleana, se o número de pesquisa cruzar para cima a banda superior, compramos (entradas). Quando procurar ficarem abaixo da banda inferior, venderemos (exits)."""

entradas = trends_btc['Bitcoin'].vbt.crossed_above(BBand_sup_1std)
saidas = trends_btc['Bitcoin'].vbt.crossed_below(BBand_inf_1std)

"""Usando a vectorbt, criamos nosso backtesting, informando as variações no preço, nossas entradas e saídas, a frequencia para plotagem (W,weekly)além de outros parâmetros.
Para fins de simplificação, mostraremos apenas a ponta compradora(longonly) e não explicaremos os diversos parâmetros da biblioteca para otimizar o backtest e as estrategias.
"""

setup_sentimento = vbt.Portfolio.from_signals(trends_btc['Close'], entradas, saidas, direction = 'longonly', freq = 'W')

setup_sentimento.plot().show()

setup_sentimento.stats()