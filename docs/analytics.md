# Dashboard Análise – Amazon Products Snapshot

## Contexto
Esse dashboard representa uma visão geral de um snapshot diário de vendas de produtos da Amazon.

O principal objetivo dessa análise é mostrar o desenvolvimento das principais categorias de forma isolada,
e conseguir visualizar onde estão as principais possibilidades de ajuste em relação a precificação de produtos.

## Principais KPIs
- Total de produtos vendidos no dia
- Média percentual de desconto por categoria
- Popularidade de produtos (calculado pela fórmula [avaliação-do-produto * log(quantidade-de-avaliações +1)])
- Comparação de preço original e preço com desconto
- Quantidade de produtos com avaliação entre 4 e 5 estrelas por categoria

## Insights
- As categorias *Home Improvement* e *Health & Personal Care* possuem, respectivamente, as maiores médias de porcentagem de desconto, entretanto, ambas não possuem produtos com boas avaliações
- A categoria Electronics se destaca como a mais bem avaliada e, simultaneamente, como a categoria com maior volume de produtos vendidos no dia
- As categorias *Computers & Accessories* e *Home & Kitchen*, ambas presentes no grupo de categorias com mais produtos bem avaliados, possuem preços abaixo da linha de tendência sobre descontos

Insight Geral: Os produtos com maior porcentagem de desconto não são necessariamente aqueles com maior taxa de venda ou popularidade

## Decisões de Design
- Tema escuro inspirado no design da Amazon
- Paleta de cores ccentrada no tom #E47911
- Dashboard baseado em um modelo dimensional com dados de snapshot diário
