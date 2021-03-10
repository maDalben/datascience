import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns

'''
req = requests.get('https://www.basketball-reference.com/leagues/NBA_2018_standings.html')

if req.status_code == 200:
    print('Requisição bem sucedida!')
    content = req.content

soup = BeautifulSoup(content, 'html.parser')
table = soup.find(name='table', attrs={'id':'confs_standings_W'})

table_str = str(table)
df = pd.read_html(table_str)[0]


print(df)
'''
def scrape_stats(base_url, year_start, year_end):
    years = range(year_start,year_end+1,1)

    final_df = pd.DataFrame()

    for year in years:
        print('Extraindo ano {}'.format(year))
        req_url = base_url.format(year)
        req = requests.get(req_url)
        soup = BeautifulSoup(req.content, 'html.parser')
        table = soup.find('table', {'id':'totals_stats'})
        df = pd.read_html(str(table))[0]
        df['Year'] = year
        final_df = final_df.append(df)
    return final_df
url = 'https://www.basketball-reference.com/leagues/NBA_{}_totals.html'
df = scrape_stats(url, 2013, 2018)

############################## Tratamento dos Dados ###################
drop_indexes = df[df['Rk'] == 'Rk'].index # Pega indexes onde a coluna 'Rk' possui valor 'Rk'
df.drop(drop_indexes, inplace=True) # elimina os valores dos index passados da tabela

#Convertendo colunas numericas para tipo numerico
numeric_cols = df.columns.drop(['Player','Pos','Tm'])
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)

#Gráficos
#sns.barplot(x='year',y='3PA')

#Ordena dataframe por bola de 3 pontos convertidas em ordem decrescente
sorted_df = df.sort_values(by=['3P'], axis=0, ascending=False)
#Top 5 arremessadores
sorted_df[['Player', '3P', 'Year']].head()

#Agrupando dados por jogador e somando os valores
grouped_df = df.groupby('Player',as_index=False).sum()
#Ordena dataframe por bola de 3 pontos convertidas em ordem decrescente
sorted_df = df.sort_values(by=['3P'], axis=0, ascending=False)
#Top 5
sorted_df[['Player', '3P', '3PA']].head()


