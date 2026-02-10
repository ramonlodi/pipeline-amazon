import pandas as pd
import re
import sys
import os
from datetime import datetime, timedelta

SNAPSHOT_DATE = datetime(2026, 2, 8)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ABRIR ARQUIVO CSV
dataset_path = os.path.join(BASE_DIR, 'data', 'raw', 'amazon.csv')

try:
  raw_df = pd.read_csv(dataset_path)
  print(f"Arquivo encontrado. Total de linhas carregadas: {len(raw_df)}")
except Exception as e:
  print(f"Arquivo não encontrado. Erro: {e}")
  sys.exit(1)

# LIMPAR OS DADOS DE VALORES
def clean_value(value):
  if isinstance(value, str):
    value = re.sub(r'[^\d.]', '',value)
    if value == '':
      return None
    return float(value)
  return value

raw_df['actual_price'] = raw_df['actual_price'].apply(clean_value)
raw_df['discounted_price'] = raw_df['discounted_price'].apply(clean_value)
raw_df['rating'] = raw_df['rating'].apply(clean_value).fillna(0)
raw_df['rating_count'] = (
  raw_df['rating_count']
  .apply(clean_value)
  .pipe(pd.to_numeric, errors='coerce')
  .astype('Int64')
)

# CRIAR DIM_CATEGORIES
path_to_id = {}
all_categories = []

for path in raw_df['category'].dropna():
  parts = [p.strip() for p in path.split('|')]
    
  for i in range(len(parts)):
    category_name = parts[i]
    parent_name = parts[i-1] if i > 0 else None
    full_path = '|'.join(parts[:i+1])

    if full_path not in path_to_id:
       new_id = len(path_to_id) + 1
       path_to_id[full_path] = new_id
       
       all_categories.append({
          'category_id': new_id,
          'category_name': category_name,
          'parent_name': parent_name,
          'full_path': full_path
        })

df_cats = pd.DataFrame(all_categories)

def find_parent_id(row):
  if row['parent_name'] is None:
      return None
    
  parent_path = '|'.join(row['full_path'].split('|')[:-1]) 
  return path_to_id.get(parent_path)

df_cats['parent_category_id'] = df_cats.apply(find_parent_id, axis=1)
df_cats['parent_category_id'] = df_cats['parent_category_id'].astype('Int64')

dim_categories = df_cats[['category_id', 'category_name', 'parent_category_id', 'full_path']].copy()
dim_categories = dim_categories.sort_values('category_id').reset_index(drop=True)

raw_df['category_id'] = raw_df['category'].apply(
  lambda x: path_to_id.get(x.strip()) if pd.notna(x) else None
)

# CRIAR DIM_PRODUCTS
products_data = []
processed_products = set()

for i, row in raw_df.iterrows():
  product_id = row['product_id']
    
  if product_id not in processed_products:
    product_info = {
      'product_id': product_id,
      'product_name': row['product_name'],
      'category_id': row['category_id'],
      'product_link': row['product_link']
    }
        
    products_data.append(product_info)
    processed_products.add(product_id)

dim_products = pd.DataFrame(products_data)

dim_products = dim_products.groupby('product_id', as_index=False).agg({
  'product_name': 'first',
  'category_id': 'first',
  'product_link': 'first'
})

# CRIAR DIM_TIME
def create_dim_time(start_date='2020-01-01', end_date='2030-12-31'):
  dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
  dim_time = pd.DataFrame({
    'date_id': dates.strftime('%Y%m%d').astype(int),
    'full_date': dates,
    'year': dates.year,
    'quarter': dates.quarter,
    'month': dates.month,
    'month_name': dates.strftime('%B'),
    'day': dates.day,
    'day_of_year': dates.dayofyear,
    'day_of_week': dates.dayofweek + 1,  # Segunda=1, Domingo=7
    'week_of_year': dates.isocalendar().week
  })
    
  day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  dim_time['day_name'] = dates.dayofweek.map(lambda x: day_names[x])
    
  dim_time['quarter_name'] = 'Q' + dim_time['quarter'].astype(str)
    
  dim_time['month_abbr'] = dates.strftime('%b')
  
  dim_time['week_of_year'] = dim_time['week_of_year'].astype(int)

  dim_time['year_month'] = dates.strftime('%Y-%m')
    
  dim_time = dim_time.sort_values('full_date').reset_index(drop=True)
    
  return dim_time

dim_time = create_dim_time(
    start_date='2020-01-01',
    end_date=SNAPSHOT_DATE.strftime('%Y-%m-%d')
)

# CRIAR FACT_PRODUCTS_SNAPSHOTS
fact_products_snapshot = raw_df.groupby('product_id', as_index=False).agg({
  'discounted_price': 'first',
  'actual_price': 'first',
  'rating': 'mean',
  'rating_count': 'max'
})

fact_products_snapshot['date_id'] = int(SNAPSHOT_DATE.strftime('%Y%m%d'))

fact_products_snapshot['sk_fact'] = range(1, len(fact_products_snapshot) + 1)

fact_products_snapshot = fact_products_snapshot[['sk_fact', 'product_id', 'date_id', 'discounted_price', 'actual_price', 'rating', 'rating_count']]

# VERIFICAR DE DUPLICIDADE TABELA FACT
fact_duplicates = fact_products_snapshot.duplicated(subset=['product_id', 'date_id']).sum()

if fact_duplicates > 0:
  print (f"AVISO: {fact_duplicates} registros duplicados na fact")
else:
  print(f"  -> Nenhuma duplicata na fact")

# VERIFICAR DE CONSISTÊNCIA DE PREÇOS
inconsistent_prices = fact_products_snapshot[fact_products_snapshot['discounted_price'] > fact_products_snapshot['actual_price']]

if len(inconsistent_prices) > 0:
  print(f"AVISO: {len(inconsistent_prices)} registros com desconto maior que o preço original")
else:
  print(f"  -> Preços consistentes")

# EXPORTAR TABELAS DIMENSÃO E FATOS
output_path = os.path.join(BASE_DIR, 'data', 'silver')

if not os.path.exists(output_path):
  os.makedirs(output_path)

dim_products.to_csv(os.path.join(output_path, 'dim_products.csv'),index=False)
dim_categories.to_csv(os.path.join(output_path, 'dim_categories.csv'), index=False)
dim_time.to_csv(os.path.join(output_path, 'dim_time.csv'), index=False)
fact_products_snapshot.to_csv(os.path.join(output_path, 'fact_products_snapshot.csv'), index=False)

print(" ")
print(f"Arquivos criados com sucesso em: {output_path}")

# RESUMO FINAL
print("\n" + "="*60)
print("RESUMO DO PIPELINE ETL")
print("="*60)
print(f"Dimensões criadas:")
print(f"   - dim_categories: {len(dim_categories)} categorias")
print(f"   - dim_products: {len(dim_products)} produtos únicos")
print(f"   - dim_time: {len(dim_time)} dias (2020-02-08)")
print(f"\nFact criada:")
print(f"   - fact_products_snapshot: {len(fact_products_snapshot)} registros")
print(f"   - Date_id usado: {fact_products_snapshot['date_id'].iloc[0]}")
print(f"   - Data correspondente: {dim_time[dim_time['date_id'] == fact_products_snapshot['date_id'].iloc[0]]['full_date'].iloc[0].date()}")
