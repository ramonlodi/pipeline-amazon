# 🛒 Amazon Products Analytics Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-ETL-150458?logo=pandas&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
![Status](https://img.shields.io/badge/status-concluído-brightgreen)

Este projeto consiste no desenvolvimento de um pipeline de dados completo, partindo de um arquivo CSV bruto contendo dados de produtos da Amazon até a construção de um dashboard analítico no Power BI.

O foco do projeto é demonstrar boas práticas de engenharia de dados, modelagem dimensional e visualização de dados, utilizando um snapshot diário para análise exploratória e geração de insights de negócio.

---

## 📌 Visão Geral do Projeto

O pipeline foi estruturado em três camadas de dados:

| Camada | Descrição |
| --- | --- |
| **Raw** | Dados brutos exatamente como fornecidos (arquivo CSV original disponível em: [Kaggle - Amazon Sales Dataset](https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset)) |
| **Silver** | Dados tratados, normalizados e organizados em dimensões e fatos |
| **Gold** | Dados prontos para consumo analítico no Power BI |

A partir da camada Gold, foi desenvolvido um dashboard no Power BI para análise de preços, descontos, avaliações e popularidade dos produtos.

## 🏗️ Arquitetura do Pipeline

```
CSV Bruto
   ↓
ETL Raw → Silver (Pandas)
   ↓
Modelo Dimensional (Star Schema)
   ↓
ETL Silver → Gold (Pandas)
   ↓
Dashboard (Power BI)
```

## 📊 Dashboard

O dashboard foi desenvolvido no Power BI utilizando exclusivamente dados da camada Gold.

**Principais análises abordadas:**

- Média de desconto por categoria
- Distribuição de produtos bem avaliados (4–5 estrelas)
- Relação entre desconto, popularidade e volume de produtos
- Comparação entre preço original e preço com desconto

<!-- Adicione um print do dashboard e descomente a linha abaixo, ajustando o nome do arquivo -->
<!-- ![Preview do dashboard](docs/preview-dashboard.png) -->

📄 **Preview em PDF:** [`docs/dashboard-overview-amazon.pdf`](docs/dashboard-overview-amazon.pdf)

📁 **Arquivo Power BI:** [`dashboard/dashboard-overview-amazon.pbix`](dashboard/dashboard-overview-amazon.pbix)

> **Observação:**
> Para uma análise detalhada dos insights de negócio obtidos, consulte o arquivo: [`docs/insights-amazon.md`](docs/insights-amazon.md)

## 📈 Principais KPIs

- Total de produtos vendidos no dia
- Média percentual de desconto por categoria
- Popularidade do produto → *(avaliação × log(número de avaliações + 1))*
- Relação entre preço original e preço com desconto
- Quantidade de produtos com avaliação entre 4 e 5 estrelas por categoria

## 🛠️ Tecnologias Utilizadas

- **Python** (Pandas)
- **Power BI**
- **Git & GitHub**
- **Modelagem Dimensional** (Star Schema e Snapshot diário)

## 📁 Estrutura do repositório

```
.
├── dashboard/
│   └── dashboard-overview-amazon.pbix   # dashboard Power BI
├── data/                                # camadas Raw, Silver e Gold
├── docs/
│   ├── dashboard-overview-amazon.pdf    # preview do dashboard
│   └── insights-amazon.md               # insights de negócio
├── src/                                 # scripts ETL
├── .gitignore
├── LICENSE
└── README.md
```

## ⚙️ Reprodutibilidade

Os scripts ETL estão disponíveis no repositório para fins de transparência e reprodutibilidade do processo de transformação dos dados.
Os arquivos resultantes das camadas Silver e Gold já estão materializados neste repositório.

## 🎯 Objetivo Profissional do Projeto

Este projeto tem como objetivo demonstrar habilidades em:

- Engenharia de dados
- Estruturação de pipelines ETL
- Modelagem dimensional
- Visualização e análise de dados
- Comunicação de insights de negócio

## 👤 Autor

Desenvolvido por **Ramon Lodi de Sousa** 🚀
[GitHub](https://github.com/ramonlodi) · [LinkedIn](https://linkedin.com/in/ramonlodi)

## 📄 Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
