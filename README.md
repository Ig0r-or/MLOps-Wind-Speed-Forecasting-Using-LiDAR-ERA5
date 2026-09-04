```
Previsão_de_vento(lidar + Era5)/
├── .venv/                      # Pasta do ambiente virtual (criada automaticamente)
├── .gitignore                  # Arquivos que NÃO vão para o GitHub (.venv, dados brutos etc)
├── README.md                   # Documentação do projeto
├── requirements.txt            # Dependências do projeto com versões
├── setup.py                    # Torna a pasta 'src' instalável como um pacote Python
├── Dockerfile                  # Containerização do projeto (Passo futuro)
│
├── data/                       # Armazenamento de dados (NÃO versionar no Git)
│   ├── raw/                    # Dados brutos (dataset.csv do LiDAR, era5_dataset.nc)
│   └── processed/              # Dados limpos/alinhados (df_analise.parquet/csv)
│
├── src/                        # Código-fonte modularizado
│   ├── __init__.py
│   ├── data/                   # Ingestão e carregamento de dados
│   │   ├── __init__.py
│   │   └── loader.py
│   │
│   ├── processing/             # Limpeza, fuso horário (UTC) e interpolação
│   │   ├── __init__.py
│   │   └── aligner.py
│   │
│   ├── features/               # Wavelets e engenharia de atributos
│   │   ├── __init__.py
│   │   └── wavelets.py
│   │
│   ├── evaluation/             # Métricas (RMSE, MAE, Bias, gráficos)
│   │   ├── __init__.py
│   │   └── metrics.py
│   │
│   └── models/                 # Modelos preditivos (LSTM, Seq2Seq, etc)
│       ├── __init__.py
│       └── predict.py
│
├── notebooks/                  # Notebooks APENAS para exploração/rascunho
│   └── 
│
├── wind_forecasting.egg-info/
│   └── 
└── main.py                     # Script principal que executa a pipeline ponta a ponta
```
