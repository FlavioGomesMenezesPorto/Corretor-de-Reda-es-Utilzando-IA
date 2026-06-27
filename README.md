# IntelliWrite AI

Plataforma de análise e treinamento de redações no padrão ITA usando Python, NLP e Machine Learning.

## Objetivo

Este projeto oferece um baseline funcional para avaliar redações no padrão ITA a partir de notas históricas. A versão atual usa:

- limpeza e normalização de texto;
- vetorização TF-IDF com uni/bigramas;
- regressão com Random Forest;
- CLI para treino, avaliação e previsão;
- rubrica ITA com Tema, Tipo de texto, Coerência, Coesão e Modalidade escrita;
- schema SQLite para persistir redações, avaliações e execuções de modelo.

## Estrutura

```text
.
├── data/
│   └── redacoes.csv
├── notebooks/
│   └── demo.ipynb
├── src/
│   ├── api.py
│   ├── conect.py
│   ├── data.py
│   ├── data_processing.py
│   ├── evaluation.py
│   ├── model.py
│   └── validatiing.py
├── tests/
│   ├── test_data_processing.py
│   └── test_evaluation.py
├── requirements.txt
├── schema_ava.sql
└── README.md
```

## Ambiente recomendado

Use Python 3.10, 3.11 ou 3.12. O ambiente atual foi criado com Python 3.14, e bibliotecas científicas como `pandas` e `scikit-learn` podem ficar instáveis ou muito lentas nessa versão.

No Prompt de Comando (`cmd.exe`):

```bat
py install 3.12
deactivate.bat
rmdir /s /q .venv
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

No PowerShell:

```powershell
py install 3.12
deactivate
Remove-Item -Recurse -Force .venv
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Dependências opcionais para notebooks, gráficos e NLP avançado:

```powershell
python -m pip install -r requirements-optional.txt
```

## Uso rápido

Treinar e salvar o modelo:

```powershell
python src\api.py train --data data\redacoes_ita.csv --model-path models\essay_grader.joblib
```

Avaliar um modelo salvo:

```powershell
python src\api.py evaluate --data data\redacoes.csv --model-path models\essay_grader.joblib
```

Prever a nota de uma redação:

```powershell
python src\api.py predict --model-path models\essay_grader.joblib --text "A educação é essencial para reduzir desigualdades e ampliar oportunidades."
```

Abrir a interface web:

```powershell
python -m streamlit run app.py
```

Criar as tabelas do banco SQLite:

```powershell
python src\api.py init-db --database IA.db --schema schema_ava.sql
```

## Dados

O CSV esperado deve conter, no mínimo:

- `essay`: texto da redação;
- `score`: nota numérica total; ou
- `tema`, `tipo_texto`, `coerencia`, `coesao`, `modalidade`: cinco critérios ITA, cada um de 0 a 2.

No modo ITA, a nota total vai de 0 a 10. A redação esperada é dissertativo-argumentativa, com título e extensão estimada entre 25 e 35 linhas.

## Testes

```powershell
pytest
```

## Próximos passos técnicos

- Aumentar o dataset real de redações corrigidas.
- Separar notas por competência, se houver rubrica do ENEM ou rubrica própria.
- Adicionar validação cruzada e comparação entre modelos.
- Criar uma interface web simples para submissão de redações.
- Experimentar embeddings e modelos Transformer depois que o baseline estiver medido.
