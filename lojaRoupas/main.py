'''
As bibliotecas utilizadas neste código são pandas e numpy.
Apesar de elas não serem recomendadas para trabalhar com big data,
elas são úteis quando o volume de dados não é expressivo.
'''
import pandas as pd
import numpy as np

#Importação de dados
'''
Nesta parte do código, estamos importando dados do tipo csv (comma-separated-values) e 
especificando as colunas que possuem dados do tipo int e do tipo float.
Quando se trabalha com dados é de extrema importância deixar claro no código qual o tipo
de dado de cada coluna, pois alguns algoritmos, por exemplo, podem se comportar de maneira diferente ao
encontrar um texto com valor "10" e um número inteiro com com o valor 10 
porque são valores diferentes.
'''
me = pd.read_csv('dados/meta.csv',
                 dtype={'Data': np.int32,
                        'Meta Valor': np.int32,
                        'Meta Unidades': np.int32})
pr = pd.read_csv('dados/precos.csv',
                 decimal=",",
                 dtype={"Preço": np.float32}
                 )
ve = pd.read_csv('dados/vendas.csv',
                 parse_dates=[1],
                 dtype={'Ano': np.int32, 'Unidades':  np.int32}
                 )

#Join dataframes de vendas com preços
val_ve = ve.set_index('Produto').join(pr.set_index('Produto'))

#Objeto preços para uma coluna de texto
val_ve["Preço"] = val_ve["Preço"].astype(str)

#Substituição de ',' por '.'
val_ve["Preço"] = val_ve["Preço"].str.replace(',', '.')

#Coluna de preço do tipo string para numerico
val_ve["Preço"] = pd.to_numeric(val_ve["Preço"], errors='coerce')

#Valor total de vendas
val_ve["valor_total"] = val_ve["Unidades"]*val_ve['Preço']

#Valor total por loja e ano
val_ve_acumuladas = val_ve.groupby(["Loja", "Ano"])["valor_total"].sum()

#Total de unidades vendidas e agrupadas por loja e ano
qtde_ve_acumuladas = val_ve.groupby(["Loja", "Ano"])["Unidades"].sum()

#Junção de total de vendas com o total de unidades
vendas_por_unid = pd.merge(val_ve_acumuladas, qtde_ve_acumuladas,
                           left_on=["Loja", "Ano"], right_on=["Loja", "Ano"])

#Junção dos dataframes vendas_por_unid com o de metas
juncao_vendasUnid_metas = pd.merge(vendas_por_unid, me,
                                   left_on=["Loja", "Ano"], right_on=["Loja", "Data"])

#percentual de valores vendidos
juncao_vendasUnid_metas["% Meta Valor"] = juncao_vendasUnid_metas["valor_total"].\
    div(juncao_vendasUnid_metas["Meta Valor"])

#percentual de unidades vendidos
juncao_vendasUnid_metas["% Meta Unidades"] = juncao_vendasUnid_metas["Unidades"].\
    div(juncao_vendasUnid_metas["Meta Unidades"])

#Rename a coluna Data para Ano
juncao_vendasUnid_metas = juncao_vendasUnid_metas.\
    rename(columns={"Data": "Ano"})

#Selecionando apenas as colunas de interesse
resultado_proposto = juncao_vendasUnid_metas[["Ano", "Loja", "% Meta Valor", "% Meta Unidades"]]

print(resultado_proposto)
