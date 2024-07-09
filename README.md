# Modelo supervisionado de estimativa de produtividade

<img alt="Static Badge" src="https://img.shields.io/badge/python-3.12-blue?style=flat"> <img alt="Static Badge" src="https://img.shields.io/badge/underberg-agro-red?style=flat">

## Índice
[1) Estrutura do diretório](#estrutura-dos-diretórios)

[2) Resumo do treinamento](#resumo-do-treinamento)

[3) Passo a passo](#passo-a-passo)
## Estrutura dos diretórios
O repositório está dividido de forma que as queries para se utilizar poderão ser salvas dentro de **data/queries**, como arquivos .SQL e executadas utilizando função do módulo **utils.query_execution.py**. 

O módulo **models/select_models.py** contém os intervalos de parâmetros otimizáveis pela Otimização Bayesiana, aonde utilizam os agentes de otimização do **models/optimizers_models/**.
```text
├── data
│   └── queries
│       └── arquivos.sql
├── models
│   ├── select_models.py
│   └── optmizers_models
│       ├── gradient_boosting.py
│       ├── knn.py
│       ├── xgboost.py
│       ├── random_forest.py
│       ├── ridge.py
│       └── svr.py
├── utils
│   ├── dataprep.py
│   ├── lofo_agent.py
│   ├── plot_models.py
│   └── query_execution.py
├── README.md
├── lofo_scripts.py
├── requirements-dev.txt
├── requirements.in
├── train_ml.py
└── .gitignore
```
## Resumo do treinamento

<img alt="Static Badge" src="readme\Untitled - Frame 1.jpg">


## Passo-a-passo rápido
1 - Inicialmente crie um ambiente virtual para instalar as dependências e nomeie o ambiente de .venv;
```bash
python3.12 -m venv .venv
```
2 - Ative o ambiente criado através do terminal, dentro do repositório;
```bash
source .venv/bin/activate
pip install --upgrade pip
```
3 - A seguir, instale as dependências do projeto;
```bash
pip install -r requirements.in
```
4 - Para treinar o modelo basta escutar o arquivo __main__.py
```bash
python3.12 __main__.py
```

Dentro do **__main__.py** há opções nas listas para normalização dos dados e otimizadores dos modelos, sendo:
- **Normalização**
  - standard
  - robust
  - minmax
-  **Modelos disponíveis**
   -  rf (Random Forest)
   -  svr (Suport Vector Machine Regressor)
   -  xgboost 
   -  gbr (Gradient Boosting Regressor)
   -  knn
   -  lasso
   -  ridge
   -  mlpregressor (Neural Network)