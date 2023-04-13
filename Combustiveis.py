#Importando bibliotecas
import pandas as pd
import glob
import os


"""--------------------------------------------EXTRACTING DATASETS--------------------------------------------"""


#Lista vazia
dados = []

# Diretório dos arquivos CSV
diretorio = r'D:\Portfolio\GitHub\Combustiveis_de_2013_a_2021\Dados_Brutos'

# Obter a lista de arquivos CSV no diretório
arquivos_csv = glob.glob(os.path.join(diretorio, '*.csv'))

# Loop para ler todos os arquivos CSV
for arquivo in arquivos_csv:
    dfs = pd.read_csv(arquivo, delimiter=';')
    dados.append(dfs)

#Concatena todos os arquivos CSV em um arquivo só: "df"
df = pd.concat(dados, ignore_index=True)


"""-------------------------------------------TRANSFORMING DATASETS------------------------------------------"""


#Renomeia colunas
df.rename(columns={'Regiao - Sigla':'Regiao', 'Estado - Sigla':'Estado'}, inplace = True)

#Substitui siglas pelo nome da região
regioes = {'N':'Norte', 'NE':'Nordeste', 'CO':'Centro-Oeste', 'S':'Sudeste', 'SE':'Suldeste'}
df['Regiao'] = df['Regiao'].replace(regioes)

#Substitui o separador decimal de "," para "."
df['Valor de Compra'] = df['Valor de Compra'].str.replace(',', '.').astype(float)
df['Valor de Venda'] = df['Valor de Venda'].str.replace(',', '.').astype(float)

#Converte o tipo da coluna de str para float
df['Valor de Venda'] = (df['Valor de Venda'].astype(float))
df['Valor de Compra'] = (df['Valor de Compra'].astype(float))

#Cria a coluna Margem de Lucro com 2 casas decimais
df['Margem de Lucro'] = (((df['Valor de Venda'] - df['Valor de Compra']) / df['Valor de Venda']) * 100).round(2)

#Arredonda as casas decimais das colunas especificadas
df[['Valor de Compra', 'Valor de Venda']] = df[['Valor de Compra', 'Valor de Venda']].round(2)

#Substitui as celulas vazias da coluna
df['Complemento'].fillna('Não informado', inplace=True)

#Subistitui as celulas vazias e altera o tipo
df[['Valor de Compra', 'Numero Rua', 'Margem de Lucro', 'Valor de Venda']] = df[['Valor de Compra', 'Numero Rua', 'Margem de Lucro', 'Valor de Venda']].fillna(float(0))

 #Converte os valores da coluna para strings
df['Bairro'] = df['Bairro'].astype(str)

#Coloca 'Não informado' nas celulas que possuem apenas caracteres não alfanumericos ou vazio
df['Bairro'] = df['Bairro'].apply(lambda x: 'Não informado' if (not x.strip()) or not x.isalnum() else x)

#Subistitui as celulas vazias
df['Unidade de Medida'].fillna('R$ / litro', inplace=True)
df.drop(df[df['Bandeira'].isnull()].index, inplace=True)


"""------------------------------------------LOAD DATASETS AND SLICING-------------------------------------------"""


# Número de linhas para processar em cada parte
tamanho = 1000000

# Dividir o DataFrame em partes menores
partes = [df[i:i + tamanho] for i in range(0, len(df), tamanho)]

# Diretório de saída para os arquivos CSV
destino = 'D:\Portfolio\GitHub\Combustiveis_de_2013_a_2021\Dados_Tratados'

# Loop para processar e salvar as partes em arquivos CSV separados
for i, df_parte in enumerate(partes, 1):

    # Salvar parte em um novo arquivo CSV
    caminho_saida = os.path.join(destino, f'Combustiveis_{i}.csv')
    df_parte.to_csv(caminho_saida, index=False)

#Informa a conclusão da criação dos arquivos
print(f'Arquivo exportado para {destino}')


"""-----------------------------------------------BUSINESS QUESTIONS---------------------------------------------"""


#1 - Qual a maior, a média e a menor Margem de Lucro de todo o período por produto?

#No País
print('A maior margem de lucro do periodo por produto:')
df['Margem de Lucro'].groupby(df['Produto']).max()

print('A média de margem de lucro do periodo por produto:')
df['Margem de Lucro'].groupby(df['Produto']).mean().round(2)

print('A menor margem de lucro do periodo por produto:')
df['Margem de Lucro'].groupby(df['Produto']).min()

#1.1 - Por Região
print('A maior margem de lucro do periodo por produto e região:')
df.groupby(['Regiao', 'Produto'])['Margem de Lucro'].max()

print('A média de margem de lucro do periodo por produto e região:')
df.groupby(['Regiao', 'Produto'])['Margem de Lucro'].mean().round(2)

print('A menor margem de lucro do periodo por produto e região:')
df.groupby(['Regiao', 'Produto'])['Margem de Lucro'].min()

#1.2 - Por Estado
print('A maior margem de lucro do periodo por estado e produto:')
df.groupby(['Estado', 'Produto'])['Margem de Lucro'].max()

print('A média de margem de lucro do periodo por estado e produto:')
df.groupby(['Estado', 'Produto'])['Margem de Lucro'].mean().round(2)

print('A menor margem de lucro do periodo por estado e produto:')
df.groupby(['Estado', 'Produto'])['Margem de Lucro'].min()

#1.3 - Por Municipio
print('O município com a maior margem de lucro do periodo:')
df.loc[df['Margem de Lucro'].idxmax(), ['Municipio', 'Estado', 'Margem de Lucro']], df['Margem de Lucro'].max()

print('A média de margem de lucro do periodo por município:')
df['Margem de Lucro'].groupby(df['Municipio']).mean().round(2)

print('A município com a menor margem de lucro do periodo:')
df.loc[df['Margem de Lucro'].idxmin(), ['Municipio', 'Estado', 'Margem de Lucro']], df['Margem de Lucro'].min()

#1.4 - Por CNPJ
print('A empresa com maior margem de lucro do periodo:')
df.loc[df['Margem de Lucro'].idxmax(), ['CNPJ da Revenda', 'Margem de Lucro']], df['Margem de Lucro'].max()

print('A média de margem de lucro do periodo por empresa:')
df['Margem de Lucro'].groupby(df['CNPJ da Revenda']).mean().round(2)

print('A empresa com menor margem de lucro do periodo:')
df.loc[df['Margem de Lucro'].idxmin(), ['CNPJ da Revenda', 'Margem de Lucro']], df['Margem de Lucro'].min()

#1.5 - Por Bandeira
print('A bandeira com maior margem de lucro do periodo:')
df.loc[df['Margem de Lucro'].idxmax(), ['Bandeira', 'Margem de Lucro']], df['Margem de Lucro'].max()

print('A média de margem de lucro do periodo por bandeira:')
df['Margem de Lucro'].groupby(df['Bandeira']).mean().round(2)

print('A empresa com menor margem de lucro do periodo:')
df.loc[df['Margem de Lucro'].idxmin(), ['Bandeira', 'Margem de Lucro']], df['Margem de Lucro'].min()


#2 - Qual o maior, a média e o menor Valor de Compra e Valor de Venda de todo o período por produto?

#2.1 - No País
print('O maior valor de compra e venda do periodo por produto:')
df.groupby(df['Produto'])['Valor de Compra', 'Valor de Venda'].max()

print('A média do valor de compra e venda do periodo por produto:')
df.groupby(df['Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)

print('O menor valor de compra e venda do periodo por produto:')
df.groupby(df['Produto'])['Valor de Compra', 'Valor de Venda'].min()

#2.2 - Por Estado
print('O maior valor de compra e venda do periodo por produto e estado:')
df.groupby(['Estado', 'Produto'])['Valor de Compra', 'Valor de Venda'].max()

print('A média do valor de compra e venda do periodo por produto e estado:')
df.groupby(['Estado', 'Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)

print('O menor valor de compra e venda do periodo por produto e estado:')
df.groupby(['Estado', 'Produto'])['Valor de Compra', 'Valor de Venda'].min()

#2.3 - Por Município
print('O maior valor de compra e venda do periodo por produto e município:')
df.groupby(['Municipio', 'Produto'])['Valor de Compra', 'Valor de Venda'].max()

print('A média do valor de compra e venda do periodo por produto e município:')
df.groupby(['Municipio', 'Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)

print('O menor valor de compra e venda do periodo por produto e município:')
df.groupby(['Municipio', 'Produto'])['Valor de Compra', 'Valor de Venda'].min()

#2.4 - Por CNPJ
print('O maior valor de compra e venda do periodo por produto e empresa:')
df.groupby(['CNPJ da Revenda', 'Produto'])['Valor de Compra', 'Valor de Venda'].max()

print('A média do valor de compra e venda do periodo por produto e empresa:')
df.groupby(['CNPJ da Revenda', 'Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)

print('O menor valor de compra e venda do periodo por produto e empresa:')
df.groupby(['CNPJ da Revenda', 'Produto'])['Valor de Compra', 'Valor de Venda'].min()

#2.5 - Por Bandeira
print('O maior valor de compra e venda do periodo por produto e bandeira:')
df.groupby(['Bandeira', 'Produto'])['Valor de Compra', 'Valor de Venda'].max()

print('A média do valor de compra e venda do periodo por produto e bandeira:')
df.groupby(['Bandeira', 'Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)

print('O menor valor de compra e venda do periodo por produto e bandeira:')
df.groupby(['Bandeira', 'Produto'])['Valor de Compra', 'Valor de Venda'].min()