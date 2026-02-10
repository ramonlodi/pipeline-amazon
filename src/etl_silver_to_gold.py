import pandas as pd
import sys
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ABRIR ARQUIVOS CSV
categories_path = os.path.join(BASE_DIR, 'data', 'silver', 'dim_categories.csv')
products_path = os.path.join(BASE_DIR, 'data', 'silver', 'dim_products.csv')
time_path = os.path.join(BASE_DIR, 'data', 'silver', 'dim_time.csv')
fact_snapshot_path = os.path.join(BASE_DIR, 'data', 'silver', 'fact_products_snapshot.csv')

try:
  categories_df = pd.read_csv(categories_path)
  products_df = pd.read_csv(products_path)
  time_df = pd.read_csv(time_path)
  fact_snapshot_df = pd.read_csv(fact_snapshot_path)
  print(f"Arquivos encontrados. Total de linhas carregadas: {len(categories_df) + len(products_df)+ len(time_df) + len(fact_snapshot_df)}")
except Exception as e:
  print(f"Arquivos não encontrados. Erro: {e}")
  sys.exit(1)

# CRIAR TABELA GOLD
gold_df = fact_snapshot_df.merge(
  products_df,
  on='product_id',
  how='left'
).merge(
  categories_df,
  on='category_id',
  how='left'
).merge(
  time_df[['date_id', 'full_date', 'year', 'month', 'month_name']],
  on='date_id',
  how='left'
)

gold_df['discount_pct'] = ((gold_df['actual_price'] - gold_df['discounted_price']) / gold_df['actual_price']) * 100
gold_df['discount_pct'] = gold_df['discount_pct'].round(2)

gold_df['popularity_score'] = (gold_df['rating'] * np.log(gold_df['rating_count'] + 1)).round(1)

gold_df['principal_category'] = (gold_df['full_path'].str.split('|').str[0])
gold_df = gold_df.drop(columns=['full_path'])

gold_df = gold_df[[
    'product_id',
    'product_name',
    'principal_category',
    'category_name',
    'discounted_price',
    'actual_price',
    'discount_pct',
    'rating',
    'rating_count',
    'popularity_score',
    'full_date',
    'month',
    'month_name',
    'year'
]]

# EXPORTAR TABELA GOLD
output_path = os.path.join(BASE_DIR, 'data', 'gold')

if not os.path.exists(output_path):
  os.makedirs(output_path)

gold_df.to_csv(os.path.join(output_path, 'gold_df.csv'), index=False)

print(" ")
print(f"Arquivo criado com sucesso em: {output_path}")
