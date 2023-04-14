## Fuels: Purchase and Sale in Brazil from 2013 to 2021

![header](https://cbie.com.br/storage/2019/03/MKT_2019_imagem_destacada_voce_sabia_quantas_plataformas_de_petroleo_v2.jpg)

## Licence

https://github.com/JeffersonLCXaxa/Combust-veis-2013-a-2021/blob/main/LICENCE


## About the project

Fuels: Purchase and Sale in Brazil from 2013 to 2021

In this project, I analyzed relevant data on the purchase and sale of fuels in Brazil over a nine-year period, spanning from 2013 to 2021.

Fuels play a crucial role in the Brazilian economy, affecting the transport, industry and commerce sectors. Understanding the trends and factors that influence the fuel market is extremely important for companies, governments, consumers and other stakeholders in the sector.

## Project objectives

Analyze fuel purchase and sale data in Brazil from 2013 to 2021 to identify variations in fuel sales during the analyzed period to present relevant conclusions for the fuel sector.

I used an integrated approach, combining data analysis techniques with the use of Python and Power BI tools to perform the analysis.


## Data source (public data)

https://dados.gov.br/dados/conjuntos-dados/serie-historica-de-precos-de-combustiveis-e-de-glp

If the link doesn't work, copy and paste it into your browser.

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

## Starting code

- Library importing

        import pandas as pd
        import glob
        import os

## Datasets extracting

- Empty list
        
        dados = []

- Directory of csv files
        
        diretorio = r'C:\Users\jeffe\Desktop\Dados_Publicos\Combustiveis'

- Geting list of csv files in directory
        
        arquivos_csv = glob.glob(os.path.join(diretorio, '*.csv'))

- Reading all csv files
        
        for arquivo in arquivos_csv:
            dfs = pd.read_csv(arquivo, delimiter=';')
            dados.append(dfs)

- Concatenates all csv files in df variable
        
        df = pd.concat(dados, ignore_index=True)

## Exploratory analysis

- Returns the number of rows and columns
        
        df.shape

- Returns all colmns name
        
        [nome_coluna for nome_coluna in df]

- Returns the frist 10 row names
        
        df.head(10)

- Returns the type of each column
        
        df.dtypes

- Returns the total number of blank cells in each column
        
        df.isnull().sum()

- Returns the distinct values of the Region column
        
        df['Regiao - Sigla'].unique()

## Transforming the data

- Rename columns
        
        df.rename(columns={'Regiao - Sigla':'Regiao', 'Estado - Sigla':'Estado'}, inplace = True)

- Replaces abbreviations with the name of the region
        
        regioes = {'N':'Norte', 'NE':'Nordeste', 'CO':'Centro-Oeste', 'S':'Sudeste', 'SE':'Suldeste'}
        df['Regiao'] = df['Regiao'].replace(regioes)

- Replace the decimal separator "," with "."
        
        df['Valor de Compra'] = df['Valor de Compra'].str.replace(',', '.').astype(float)
        df['Valor de Venda'] = df['Valor de Venda'].str.replace(',', '.').astype(float)

- Convert column type from "str" to "float"
        
        df['Valor de Venda'] = (df['Valor de Venda'].astype(float))
        df['Valor de Compra'] = (df['Valor de Compra'].astype(float))

- Creates the Profit Margin column with 2 decimal places
        
        df['Margem de Lucro'] = (((df['Valor de Venda'] - df['Valor de Compra']) / df['Valor de Venda']) * 100).round(2)

- Rounds the decimal places of the specified columns
        
        df[['Valor de Compra', 'Valor de Venda']] = df[['Valor de Compra', 'Valor de Venda']].round(2)

- Replace empty cells in column
        
        df['Complemento'].fillna('Não informado', inplace=True)

- Replace empty cells and change type
        
        df[['Valor de Compra', 'Numero Rua', 'Margem de Lucro', 'Valor de Venda']] = \
        df[['Valor de Compra', 'Numero Rua', 'Margem de Lucro', 'Valor de Venda']].fillna(float(0))

- Convert column values to strings
        
        df['Bairro'] = df['Bairro'].astype(str)

- Put 'Não informado' in cells that have only non-alphanumeric or empty characters
        
        df['Bairro'] = df['Bairro'].apply(lambda x: 'Não informado' if (not x.strip()) or not x.isalnum() else x)

- Replace the empty cells
        
        df['Unidade de Medida'].fillna('R$ / litro', inplace=True)
        df.drop(df[df['Bandeira'].isnull()].index, inplace=True)

## Splitting and creating new files

- Number of lines to process in each part
        
        tamanho = 1000000

- Split DataFrame into smaller parts
        
        partes = [df[i:i + tamanho] for i in range(0, len(df), tamanho)]

- Output directory for csv files
        
        destino = 'C:/Users/jeffe/Desktop/Dados_Publicos'

- To process and save the parts in separate CSV files
        
        for i, df_parte in enumerate(partes, 1):
            caminho_saida = os.path.join(destino, f'Combustiveis_{i}.csv')
            df_parte.to_csv(caminho_saida, index=False)

- Reports completion of file creation
        
        print(f'Arquivo exportado para {destino}')

## Business questions

### 1 - What is the highest, average and lowest Profit Margin for the entire period by product?

- In the country
        
        print('The highest profit margin for the period by product:')
        df['Margem de Lucro'].groupby(df['Produto']).max()
        
        print('The average profit margin for the period by product:')
        df['Margem de Lucro'].groupby(df['Produto']).mean().round(2)
        
        print('The lowest profit margin for the period by product:')
        df['Margem de Lucro'].groupby(df['Produto']).min()

- By region
        
        
        print('The highest profit margin for the period by product and region:')
        df.groupby(['Regiao', 'Produto'])['Margem de Lucro'].max()
        
        print('Average profit margin for the period by product and region:')
        df.groupby(['Regiao', 'Produto'])['Margem de Lucro'].mean().round(2)
        
        print('The lowest profit margin for the period by product and region:')
        df.groupby(['Regiao', 'Produto'])['Margem de Lucro'].min()

- By state
        
        print('The highest profit margin for the period by state and product:')
        df.groupby(['Estado', 'Produto'])['Margem de Lucro'].max()
        
        print('Average profit margin for the period by state and product:')
        df.groupby(['Estado', 'Produto'])['Margem de Lucro'].mean().round(2)
        
        print('The lowest profit margin for the period by state and product:')
        df.groupby(['Estado', 'Produto'])['Margem de Lucro'].min()

- By city
        
        print('The city with the highest profit margin in the period:')
        df.loc[df['Margem de Lucro'].idxmax(), ['Municipio', 'Estado', 'Margem de Lucro']], df['Margem de Lucro'].max()
        
        print('The average profit margin for the period by city:')
        df['Margem de Lucro'].groupby(df['Municipio']).mean().round(2)
        
        print('The city with the lowest profit margin in the period:')
        df.loc[df['Margem de Lucro'].idxmin(), ['Municipio', 'Estado', 'Margem de Lucro']], df['Margem de Lucro'].min()

- By CNPJ/National Register of Legal Entities
        
        print('The company with the highest profit margin for the period:')
        df.loc[df['Margem de Lucro'].idxmax(), ['CNPJ da Revenda', 'Margem de Lucro']], df['Margem de Lucro'].max()
        
        print('The average profit margin for the period by company:')
        df['Margem de Lucro'].groupby(df['CNPJ da Revenda']).mean().round(2)
        
        print('The company with the lowest profit margin for the period:')
        df.loc[df['Margem de Lucro'].idxmin(), ['CNPJ da Revenda', 'Margem de Lucro']], df['Margem de Lucro'].min()

- By company that sells fuel
        
        print('The company that sells fuel with the highest profit margin for the period:')
        df.loc[df['Margem de Lucro'].idxmax(), ['Bandeira', 'Margem de Lucro']], df['Margem de Lucro'].max()
        
        print('The average profit margin for the period by company that sells fuel:')
        df['Margem de Lucro'].groupby(df['Bandeira']).mean().round(2)
        
        print('The company that sells fuel with the lowest profit margin for the period:')
        df.loc[df['Margem de Lucro'].idxmin(), ['Bandeira', 'Margem de Lucro']], df['Margem de Lucro'].min()

### 2 - What is the highest, average and lowest Purchase Value and Sale Value for the entire period by product?

- The country
        
        print('The highest purchase and sale value of the period per product:')
        df.groupby(df['Produto'])['Valor de Compra', 'Valor de Venda'].max()
        
        print('Average purchase and sale value for the period per product:')
        df.groupby(df['Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)
        
        print('The lowest purchase and sale value of the period per product:')
        df.groupby(df['Produto'])['Valor de Compra', 'Valor de Venda'].min()

- By state
        
        print('The highest purchase and sale value of the period by product and state:')
        df.groupby(['Estado', 'Produto'])['Valor de Compra', 'Valor de Venda'].max()
        
        print('Average purchase and sale value for the period by product and state:')
        df.groupby(['Estado', 'Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)
        
        print('The lowest purchase and sale value of the period by product and state:')
        df.groupby(['Estado', 'Produto'])['Valor de Compra', 'Valor de Venda'].min()

- By city
        
        print('The highest purchase and sale value of the period by product and city:')
        df.groupby(['Municipio', 'Produto'])['Valor de Compra', 'Valor de Venda'].max()
        
        print('Average purchase and sale value for the period by product and city:')
        df.groupby(['Municipio', 'Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)
        
        print('The lowest purchase and sale value of the period by product and city:')
        df.groupby(['Municipio', 'Produto'])['Valor de Compra', 'Valor de Venda'].min()

- By CNPJ/National Register of Legal Entities
                
        print('The highest purchase and sale value of the period by product and company:')
        df.groupby(['CNPJ da Revenda', 'Produto'])['Valor de Compra', 'Valor de Venda'].max()
        
        print('Average purchase and sale value for the period by product and company:')
        df.groupby(['CNPJ da Revenda', 'Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)
        
        print('The lowest purchase and sale value for the period by product and company:')
        df.groupby(['CNPJ da Revenda', 'Produto'])['Valor de Compra', 'Valor de Venda'].min()

- By company that sells fuel
        
        print('The highest purchase and sale value of the period by product and company that sells fuel:')
        df.groupby(['Bandeira', 'Produto'])['Valor de Compra', 'Valor de Venda'].max()
        
        print('Average purchase and sale value for the period by product and company that sells fuel:')
        df.groupby(['Bandeira', 'Produto'])['Valor de Compra', 'Valor de Venda'].mean().round(2)
        
        print('The lowest purchase and sale value of the period by product and company that sells fuel:')
        df.groupby(['Bandeira', 'Produto'])['Valor de Compra', 'Valor de Venda'].min()

## How to run this project on your computer

1. Download and install Python (I recommend Anaconda Python, as it already has the main libraries installed);
2. Download and install Visual Studio Code, you can also run it in an IDE of your choice;
3. Go to the data source website and download all files, including the most current ones, if you prefer, not needing to be from 2013 to 2021;
4. Download the Combustiveis.py file from this GitHub repository;
5. With the file Combustiveis.py open, change the path of the variable "directory = r'C:\Users\jeffe\Desktop\Dados_Publicos\Combustiveis'" to the path of the folder where you left your source files.
6. Now change the variable "destination = 'C:/Users/jeffe/Desktop/Dados_Publicos'" to the path of the folder where you want the transformed files to be created;
7. Run the entire algorithm from Combustiveis.py.

At the end of the run, you will be shown all the questions followed by your answer based on the data. In addition, we will have the destination folder with csv files in parts of up to 1 million lines, each one, treated and ready to be used as a data source for the Microsoft Power BI Dashboard, which will update its information automatically when it starts.

## Project authorship

Jefferson Luiz da Costa Xaxá

LinkedIn: https://www.linkedin.com/in/jefferson-xax%C3%A1-815516b0/
