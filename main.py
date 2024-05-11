"""Script that generates Equivalentes and Equivalentes files"""
import pandas as pd

# inputs
input_path = "Lista Equivalentes.xlsx"
# outputs
output_path_tca = "output/json/TCA.json"
output_path_equivalentes_detalhe = "output/json/EquivalentesDetalhe.json"
output_path_equivalentes = "output/json/Equivalentes.json"
output_path_equivalentes_csv = "output/csv/Equivalentes.csv"
output_path_equivalentes_resumo_csv = "output/csv/EquivalentesResumo.csv"
output_path_equivalentes_detalhe_csv = "output/csv/EquivalentesDetalhe.csv"

##### Import relevante sheets from workbook #####

## TCA
df1 = pd.read_excel(input_path,engine='openpyxl',sheet_name='TCA',usecols='A:AV')

## Equivalentes
df2 = pd.read_excel(input_path,engine='openpyxl',sheet_name='Equivalentes',usecols='A:Q')

## Filter for those that count to the average
df2_filter = df2[df2['Media'] == 'Sim']

## Create table with averages by group and name
df3 = pd.merge(df2,df1,how='inner',left_on='Alimento',right_on='Nome do alimento')
df3['Energia (kcal)'] = df3['Lípidos (g)'] * 9 + df3['Hidratos de carbono (g)'] * 4 + df3['Proteínas (g)'] * 4 + df3['Álcool (g)'] * 7
df3['Hidratos (g) Porcao'] = df3['Hidratos de carbono (g)'] * df3['Porcao'] / 100
df3['Lípidos (g) Porcao'] = df3['Lípidos (g)'] * df3['Porcao'] / 100
df3['Proteínas (g) Porcao'] = df3['Proteínas (g)'] * df3['Porcao'] / 100
df3['Álcool (g) Porcao'] = df3['Álcool (g)'] * df3['Porcao'] / 100
df3_grouped = df3.groupby(by=['Grupo','Nome'])[['Porcao','Lípidos (g) Porcao','Hidratos (g) Porcao','Proteínas (g) Porcao','Álcool (g) Porcao']].mean()
df3_grouped.reset_index(inplace=True)
df3_rounded = df3_grouped.round(decimals={
                    'Porcao':0,
                    'Lípidos (g) Porcao':1,
                    'Hidratos (g) Porcao':1,
                    'Proteínas (g) Porcao':1,
                    'Álcool (g) Porcao':1
                    })

## Calculate average per group
df4 = pd.merge(df2_filter,df1,how='inner',left_on='Alimento',right_on='Nome do alimento')
df4['Energia (kcal)'] = df4['Lípidos (g)'] * 9 + df4['Hidratos de carbono (g)'] * 4 + df4['Proteínas (g)'] * 4 + df4['Álcool (g)'] * 7
df4['Hidratos (g) Porcao'] = df4['Hidratos de carbono (g)'] * df4['Porcao'] / 100
df4['Lípidos (g) Porcao'] = df4['Lípidos (g)'] * df4['Porcao'] / 100
df4['Proteínas (g) Porcao'] = df4['Proteínas (g)'] * df4['Porcao'] / 100
df4['Álcool (g) Porcao'] = df4['Álcool (g)'] * df4['Porcao'] / 100
df5 = df4.groupby(by=['Grupo'])[['Porcao','Lípidos (g) Porcao','Hidratos (g) Porcao','Proteínas (g) Porcao','Álcool (g) Porcao']].mean()
df6 = df5.round(decimals={
                    'Porcao':0,
                    'Lípidos (g) Porcao':1,
                    'Hidratos (g) Porcao':1,
                    'Proteínas (g) Porcao':1,
                    'Álcool (g) Porcao':1
                    })
df6.reset_index(inplace=True)

## Create detail table
df7 = df2[df2['Plano'] == 'Sim']
df7_clean = df7.drop(columns=['Media','Plano'])

## Generate files
df1.to_json(output_path_tca,orient='records')
df2.to_json(output_path_equivalentes_detalhe,orient='records')
df3.to_json(output_path_equivalentes,orient='records')
df3_rounded.to_csv(output_path_equivalentes_csv,sep=',',decimal='.',encoding='utf-8')
df6.to_csv(output_path_equivalentes_resumo_csv,sep=',',decimal='.',encoding='utf-8')
df7_clean.to_csv(output_path_equivalentes_detalhe_csv,sep=',',decimal='.',encoding='utf-8')
