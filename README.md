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

### Library importing

import pandas as pd

import glob

import os

### Datasets extracting

### Empty list
dados = []

### Directory of csv files
diretorio = r'C:\Users\jeffe\Desktop\Dados_Publicos\Combustiveis'

### Geting list of csv files in directory
arquivos_csv = glob.glob(os.path.join(diretorio, '*.csv'))

### Reading all csv files
for arquivo in arquivos_csv:
    dfs = pd.read_csv(arquivo, delimiter=';')
    dados.append(dfs)

### Concatenates all csv files in df variable
df = pd.concat(dados, ignore_index=True)

## Exploratory analysis

### Returns the number of rows and columns
df.shape

### Returns all colmns name
[nome_coluna for nome_coluna in df]

### Returns the frist 10 row names
df.head(10)

### Returns the type of each column
df.dtypes

### Returns the total number of blank cells in each column
df.isnull().sum()

### Returns the distinct values of the Region column
df['Regiao - Sigla'].unique()

## Transforming the data

### Rename columns
df.rename(columns={'Regiao - Sigla':'Regiao', 'Estado - Sigla':'Estado'}, inplace = True)

### Replaces abbreviations with the name of the region
regioes = {'N':'Norte', 'NE':'Nordeste', 'CO':'Centro-Oeste', 'S':'Sudeste', 'SE':'Suldeste'}
df['Regiao'] = df['Regiao'].replace(regioes)

### Replace the decimal separator "," with "."
df['Valor de Compra'] = df['Valor de Compra'].str.replace(',', '.').astype(float)
df['Valor de Venda'] = df['Valor de Venda'].str.replace(',', '.').astype(float)

### Convert column type from "str" to "float"
df['Valor de Venda'] = (df['Valor de Venda'].astype(float))
df['Valor de Compra'] = (df['Valor de Compra'].astype(float))

### Creates the Profit Margin column with 2 decimal places
df['Margem de Lucro'] = (((df['Valor de Venda'] - df['Valor de Compra']) / df['Valor de Venda']) * 100).round(2)

### Rounds the decimal places of the specified columns
df[['Valor de Compra', 'Valor de Venda']] = df[['Valor de Compra', 'Valor de Venda']].round(2)

### Replace empty cells in column
df['Complemento'].fillna('Não informado', inplace=True)

### Replace empty cells and change type
df[['Valor de Compra', 'Numero Rua', 'Margem de Lucro', 'Valor de Venda']] = df[['Valor de Compra', 'Numero Rua', 'Margem de Lucro', 'Valor de Venda']].fillna(float(0))

### Convert column values to strings
df['Bairro'] = df['Bairro'].astype(str)

### Put 'Não informado' in cells that have only non-alphanumeric or empty characters
df['Bairro'] = df['Bairro'].apply(lambda x: 'Não informado' if (not x.strip()) or not x.isalnum() else x)

### Replace the empty cells
df['Unidade de Medida'].fillna('R$ / litro', inplace=True)
df.drop(df[df['Bandeira'].isnull()].index, inplace=True)

## Splitting and creating new files

### Number of lines to process in each part
tamanho = 1000000

### Split DataFrame into smaller parts
partes = [df[i:i + tamanho] for i in range(0, len(df), tamanho)]

### Output directory for csv files
destino = 'C:/Users/jeffe/Desktop/Dados_Publicos'

### To process and save the parts in separate CSV files
for i, df_parte in enumerate(partes, 1):
    caminho_saida = os.path.join(destino, f'Combustiveis_{i}.csv')
    df_parte.to_csv(caminho_saida, index=False)

### Reports completion of file creation
print(f'Arquivo exportado para {destino}')

## Business questions

### 1 - What is the highest, average and lowest Profit Margin for the entire period by product?

#In the country
df['Margem de Lucro'].groupby(df['Produto']).max()
df['Margem de Lucro'].groupby(df['Produto']).mean().round(2)
df['Margem de Lucro'].groupby(df['Produto']).min()

### 1.1 - By region
df.groupby(['Regiao', 'Produto'])['Margem de Lucro'].max()
df.groupby(['Regiao', 'Produto'])['Margem de Lucro'].mean().round(2)
df.groupby(['Regiao', 'Produto'])['Margem de Lucro'].min()

### 1.2 - By state
df.groupby(['Estado', 'Produto'])['Margem de Lucro'].max()
df.groupby(['Estado', 'Produto'])['Margem de Lucro'].mean().round(2)
df.groupby(['Estado', 'Produto'])['Margem de Lucro'].min()

### 1.3 - By city
df.loc[df['Margem de Lucro'].idxmax(), ['Municipio', 'Estado', 'Margem de Lucro']], df['Margem de Lucro'].max()
df['Margem de Lucro'].groupby(df['Municipio']).mean().round(2)
df.loc[df['Margem de Lucro'].idxmin(), ['Municipio', 'Estado', 'Margem de Lucro']], df['Margem de Lucro'].min()

### 1.4 - By CNPJ/National Register of Legal Entities
df.loc[df['Margem de Lucro'].idxmax(), ['CNPJ da Revenda', 'Margem de Lucro']], df['Margem de Lucro'].max()
df['Margem de Lucro'].groupby(df['CNPJ da Revenda']).mean().round(2)
df.loc[df['Margem de Lucro'].idxmin(), ['CNPJ da Revenda', 'Margem de Lucro']], df['Margem de Lucro'].min()

### 1.5 - By company that sells fuel
df.loc[df['Margem de Lucro'].idxmax(), ['Bandeira', 'Margem de Lucro']], df['Margem de Lucro'].max()
df['Margem de Lucro'].groupby(df['Bandeira']).mean().round(2)
df.loc[df['Margem de Lucro'].idxmin(), ['Bandeira', 'Margem de Lucro']], df['Margem de Lucro'].min()

### 2 - What is the highest, average and lowest Purchase Value and Sale Value for the entire period by product?

### 2.1 - The country
df.groupby(df['Produto'])['Valor de Compra', 'Valor de Venda'].max()
df.groupby(df['Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)
df.groupby(df['Produto'])['Valor de Compra', 'Valor de Venda'].min()

### 2.2 - By state
df.groupby(['Estado', 'Produto'])['Valor de Compra', 'Valor de Venda'].max()
df.groupby(['Estado', 'Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)
df.groupby(['Estado', 'Produto'])['Valor de Compra', 'Valor de Venda'].min()

### 2.3 - By city
df.groupby(['Municipio', 'Produto'])['Valor de Compra', 'Valor de Venda'].max()
df.groupby(['Municipio', 'Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)
df.groupby(['Municipio', 'Produto'])['Valor de Compra', 'Valor de Venda'].min()

### 2.4 - By CNPJ/National Register of Legal Entities
df.groupby(['CNPJ da Revenda', 'Produto'])['Valor de Compra', 'Valor de Venda'].max()
df.groupby(['CNPJ da Revenda', 'Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)
df.groupby(['CNPJ da Revenda', 'Produto'])['Valor de Compra', 'Valor de Venda'].min()

### 2.5 - By company that sells fuel
df.groupby(['Bandeira', 'Produto'])['Valor de Compra', 'Valor de Venda'].max()
df.groupby(['Bandeira', 'Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)
df.groupby(['Bandeira', 'Produto'])['Valor de Compra', 'Valor de Venda'].min()
