# IntelliWrite AI

Plataforma de análise e treinamento de redações usando Python, NLP e Machine Learning.

## Objetivo

Este projeto oferece um baseline funcional para avaliar redações a partir de notas históricas. A versão atual usa:

- limpeza e normalização de texto;
- vetorização TF-IDF com uni/bigramas;
- regressão com Random Forest;
- CLI para treino, avaliação e previsão;
- três perfis de correção: Alto Padrão, Médio Padrão e Baixo Padrão;
- rubrica com Tema, Tipo de texto, Coerência, Coesão e Modalidade escrita;
- schema SQLite para persistir redações, avaliações e execuções de modelo.

## Estrutura

```text
.
├── data/# IntelliWrite AI 

Fala! Boas-vindas ao repositório do **IntelliWrite AI**. 

Eu construí esse projeto em 2025 para o meu TCC, com uma ideia bem clara na cabeça: como a gente pode usar Inteligência Artificial para facilitar a correção de redações, sem perder a qualidade e o critério? 

A resposta que cheguei foi esse sistema. Ele junta Python e Machine Learning para ler, analisar e dar notas aos textos baseados em rubricas (regras) bem definidas. É uma tentativa de organizar os pensamentos e critérios de quem corrige, automatizando o trabalho braçal.

## 🧭 Como eu organizei a casa

Eu tentei deixar a estrutura o mais limpa possível, separando bem o que cada parte faz para o código não virar uma bagunça:

* **O Motor Principal (`src/`):** É aqui que a mágica acontece. Tem a parte que limpa e prepara os textos (`data.py` e `data_processing.py`), a inteligência em si (`model.py` e `evaluation.py`), e os critérios de nota que o modelo precisa respeitar (`rubrics.py`).
* **A Porta de Entrada (`app.py` e `src/api.py`):** É por onde o sistema recebe as redações. Configurei como uma API para ficar fácil de integrar depois.
* **Área de Testes e Brincadeiras (`notebooks/`):** Se você quiser só ver a coisa funcionando na prática sem configurar muita coisa, abra o `demo.ipynb`. É o melhor lugar para entender os bastidores.
* **Garantia de Qualidade (`tests/`):** Deixei alguns testes prontos para garantir que, se eu (ou você) mexer no código amanhã, a gente não quebre a lógica de correção.

## 🛠️ Quer rodar na sua máquina?

É bem tranquilo. Não tem muito segredo:

1. Clona o repositório pra sua máquina.
2. Cria o seu ambiente virtual favorito (`venv`, por exemplo) pra não bagunçar o seu Python.
3. Instala as bibliotecas que o projeto precisa:
```bash
   pip install -r requirements.txt
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
python src\api.py train --data data\redacoes_padrao.csv --model-path models\essay_grader.joblib
```

Avaliar um modelo salvo:

```powershell
python src\api.py evaluate --data data\redacoes_padrao.csv --model-path models\essay_grader.joblib
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
- `tema`, `tipo_texto`, `coerencia`, `coesao`, `modalidade`: cinco critérios, cada um de 0 a 2.

Nos perfis de correção, a nota total vai de 0 a 10. O Alto Padrão é mais rígido, o Médio Padrão é equilibrado e o Baixo Padrão é mais tolerante/formativo.

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
