## Licence

https://github.com/JeffersonLCXaxa/Combust-veis-2013-a-2021/blob/main/LICENCE


## Sobre o projeto

Combustíveis: Compra e Venda no Brasil de 2013 a 2021

Neste projeto, analisei dados relevantes sobre a compra e venda de combustíveis no Brasil ao longo de um período de nove anos, abrangendo de 2013 a 2021.

Os combustíveis desempenham um papel crucial na economia brasileira, afetando os setores de transporte, indústria e comércio. Compreender as tendências e os fatores que influenciam o mercado de combustíveis é de extrema importância para empresas, governos, consumidores e demais interessados no setor.

Durante a pesquisa utilizei uma fonte confiável de dados, e apliquei técnicas de análise de dados para obter insights sobre o mercado de combustíveis no Brasil. Irei compartilhar com vocês cada um dos detalhes desse projeto ao longo desse readme.


## Objetivos do Projeto

Analisar os dados de compra e venda de combustíveis no Brasil de 2013 a 2021 para identificar variações na comercialização de combustíveis durante o período analisado para apresentar conclusões relevantes do setor de combustíveis.

Utilizei uma abordagem integrada, combinando técnicas de análise de dados com o uso das ferramentas Python e Power BI para realizar a análise.


## Fonte de dados(dados públicos)
https://dados.gov.br/dados/conjuntos-dados/serie-historica-de-precos-de-combustiveis-e-de-glp


## Technologies Used:
<table>
    <tr>
        <td>Visual Studio Code</td>
        <td>Python</td>
        <td>Python Library</td>
        <td>Microsoft Power BI</td>
    </tr>
    <tr>
        <td>v1.77</td>
        <td>v3.10.9</td>
        <td> pandas, glob, os</td>
        <td>v2.116.622.0 64-bit</td>
    </tr>
</table>

## Combustíveis-2013-a-2021

### Importando bibliotecas

import pandas as pd
import glob
import os

"""--------------------------------------------EXTRAINDO OS DATASETS--------------------------------------------"""

### Lista vazia
dados = []

### Diretório dos arquivos CSV
diretorio = r'C:\Users\jeffe\Desktop\Dados_Publicos\Combustiveis'

### Obter a lista de arquivos CSV no diretório
arquivos_csv = glob.glob(os.path.join(diretorio, '*.csv'))

### Loop para ler todos os arquivos CSV
for arquivo in arquivos_csv:
    dfs = pd.read_csv(arquivo, delimiter=';')
    dados.append(dfs)

### Concatena todos os arquivos CSV em um arquivo só: "df"
df = pd.concat(dados, ignore_index=True)


"""--------------------------------------------ANÁLISE EXPLORATÓRIA-------------------------------------------


### Retorna a quantidade de linhas e colunas
df.shape

### Retorna o nome de todas as colunas
[nome_coluna for nome_coluna in df]

### Retorna as o nome das colunas e as 10 primeiras linhas
df.head(10)

### Retorna o tipo de cada coluna
df.dtypes

### Retorna o total de celulas em branco em cada coluna
df.isnull().sum()

### Retorna os valores distintos da coluna Regiao
df['Regiao - Sigla'].unique()

"""

"""-------------------------------------------TRANSFORMANDO OS DADOS------------------------------------------"""


### Renomeia colunas
df.rename(columns={'Regiao - Sigla':'Regiao', 'Estado - Sigla':'Estado'}, inplace = True)

### Substitui siglas pelo nome da região
regioes = {'N':'Norte', 'NE':'Nordeste', 'CO':'Centro-Oeste', 'S':'Sudeste', 'SE':'Suldeste'}
df['Regiao'] = df['Regiao'].replace(regioes)

### Substitui o separador decimal de "," para "."
df['Valor de Compra'] = df['Valor de Compra'].str.replace(',', '.').astype(float)
df['Valor de Venda'] = df['Valor de Venda'].str.replace(',', '.').astype(float)

### Converte o tipo da coluna de str para float
df['Valor de Venda'] = (df['Valor de Venda'].astype(float))
df['Valor de Compra'] = (df['Valor de Compra'].astype(float))

### Cria a coluna Margem de Lucro com 2 casas decimais
df['Margem de Lucro'] = (((df['Valor de Venda'] - df['Valor de Compra']) / df['Valor de Venda']) * 100).round(2)

### Arredonda as casas decimais das colunas especificadas
df[['Valor de Compra', 'Valor de Venda']] = df[['Valor de Compra', 'Valor de Venda']].round(2)

### Substitui as celulas vazias da coluna
df['Complemento'].fillna('Não informado', inplace=True)

### Subistitui as celulas vazias e altera o tipo
df[['Valor de Compra', 'Numero Rua', 'Margem de Lucro', 'Valor de Venda']] = df[['Valor de Compra', 'Numero Rua', 'Margem de Lucro', 'Valor de Venda']].fillna(float(0))

### Converte os valores da coluna para strings
df['Bairro'] = df['Bairro'].astype(str)

### Coloca 'Não informado' nas celulas que possuem apenas caracteres não alfanumericos ou vazio
df['Bairro'] = df['Bairro'].apply(lambda x: 'Não informado' if (not x.strip()) or not x.isalnum() else x)

### Subistitui as celulas vazias
df['Unidade de Medida'].fillna('R$ / litro', inplace=True)
df.drop(df[df['Bandeira'].isnull()].index, inplace=True)




"""-----------------------------------Dividindo e criando novos arquivos-----------------------------------------


### Número de linhas para processar em cada parte
tamanho = 1000000

### Dividir o DataFrame em partes menores
partes = [df[i:i + tamanho] for i in range(0, len(df), tamanho)]

### Diretório de saída para os arquivos CSV
destino = 'C:/Users/jeffe/Desktop/Dados_Publicos'

### Loop para processar e salvar as partes em arquivos CSV separados
for i, df_parte in enumerate(partes, 1):

    ### Salvar parte em um novo arquivo CSV
    caminho_saida = os.path.join(destino, f'Combustiveis_{i}.csv')
    df_parte.to_csv(caminho_saida, index=False)

### Informa a conclusão da criação dos arquivos
print(f'Arquivo exportado para {destino}')
"""

"""--------------------------------PERGUNTAS DE NEGÓCIO / EXTRAÇÃO DE INFORMAÇÕES-----------------------------"""

### 1 - Qual a maior, a média e a menor Margem de Lucro de todo o período por produto?

#No País
df['Margem de Lucro'].groupby(df['Produto']).max()
df['Margem de Lucro'].groupby(df['Produto']).mean().round(2)
df['Margem de Lucro'].groupby(df['Produto']).min()

### 1.1 - Por Região
df.groupby(['Regiao', 'Produto'])['Margem de Lucro'].max()
df.groupby(['Regiao', 'Produto'])['Margem de Lucro'].mean().round(2)
df.groupby(['Regiao', 'Produto'])['Margem de Lucro'].min()

### 1.2 - Por Estado
df.groupby(['Estado', 'Produto'])['Margem de Lucro'].max()
df.groupby(['Estado', 'Produto'])['Margem de Lucro'].mean().round(2)
df.groupby(['Estado', 'Produto'])['Margem de Lucro'].min()

### 1.3 - Por Municipio
df.loc[df['Margem de Lucro'].idxmax(), ['Municipio', 'Estado', 'Margem de Lucro']], df['Margem de Lucro'].max()
df['Margem de Lucro'].groupby(df['Municipio']).mean().round(2)
df.loc[df['Margem de Lucro'].idxmin(), ['Municipio', 'Estado', 'Margem de Lucro']], df['Margem de Lucro'].min()

### 1.4 - Por CNPJ
df.loc[df['Margem de Lucro'].idxmax(), ['CNPJ da Revenda', 'Margem de Lucro']], df['Margem de Lucro'].max()
df['Margem de Lucro'].groupby(df['CNPJ da Revenda']).mean().round(2)
df.loc[df['Margem de Lucro'].idxmin(), ['CNPJ da Revenda', 'Margem de Lucro']], df['Margem de Lucro'].min()

### 1.5 - Por Bandeira
df.loc[df['Margem de Lucro'].idxmax(), ['Bandeira', 'Margem de Lucro']], df['Margem de Lucro'].max()
df['Margem de Lucro'].groupby(df['Bandeira']).mean().round(2)
df.loc[df['Margem de Lucro'].idxmin(), ['Bandeira', 'Margem de Lucro']], df['Margem de Lucro'].min()



### 2 - Qual o maior, a média e o menor Valor de Compra e Valor de Venda de todo o período por produto?

### 2.1 - No País
df.groupby(df['Produto'])['Valor de Compra', 'Valor de Venda'].max()
df.groupby(df['Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)
df.groupby(df['Produto'])['Valor de Compra', 'Valor de Venda'].min()

### 2.2 - Por Estado
df.groupby(['Estado', 'Produto'])['Valor de Compra', 'Valor de Venda'].max()
df.groupby(['Estado', 'Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)
df.groupby(['Estado', 'Produto'])['Valor de Compra', 'Valor de Venda'].min()

### 2.3 - Por Município
df.groupby(['Municipio', 'Produto'])['Valor de Compra', 'Valor de Venda'].max()
df.groupby(['Municipio', 'Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)
df.groupby(['Municipio', 'Produto'])['Valor de Compra', 'Valor de Venda'].min()

### 2.4 - Por CNPJ
df.groupby(['CNPJ da Revenda', 'Produto'])['Valor de Compra', 'Valor de Venda'].max()
df.groupby(['CNPJ da Revenda', 'Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)
df.groupby(['CNPJ da Revenda', 'Produto'])['Valor de Compra', 'Valor de Venda'].min()

### 2.5 - Por Bandeira
df.groupby(['Bandeira', 'Produto'])['Valor de Compra', 'Valor de Venda'].max()
df.groupby(['Bandeira', 'Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)
df.groupby(['Bandeira', 'Produto'])['Valor de Compra', 'Valor de Venda'].min()
