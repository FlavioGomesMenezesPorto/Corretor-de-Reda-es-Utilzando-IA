import re
from pathlib import Path
from typing import Iterable, List, Tuple

try:
    from rubrics import SCORE_COLUMNS
except ImportError:  # pragma: no cover - used when importing as a package
    from .rubrics import SCORE_COLUMNS


PORTUGUESE_TEXT_RE = re.compile(r"[^a-z0-9áéíóúàèìòùâêîôûãõçñ\s]", re.IGNORECASE)


def clean_text(text: str) -> str:
    """Normalize essay text while preserving Portuguese characters."""
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = PORTUGUESE_TEXT_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_texts(texts: Iterable[str]) -> List[str]:
    return [clean_text(text) for text in texts]


def load_data(
    filepath: str,
    text_col: str = "essay",
    score_col: str = "score",
) -> Tuple[List[str], List[float]]:
    """Load a CSV dataset and return cleaned texts plus numeric scores."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

    import pandas as pd

    df = pd.read_csv(path, encoding="utf-8-sig")
    if score_col not in df.columns and all(col in df.columns for col in SCORE_COLUMNS):
        df[score_col] = df[SCORE_COLUMNS].apply(pd.to_numeric, errors="coerce").sum(axis=1)

    missing = [col for col in (text_col, score_col) if col not in df.columns]
    if missing:
        raise ValueError(
            f"Colunas obrigatórias ausentes: {missing}. Colunas encontradas: {list(df.columns)}"
        )

    df = df[[text_col, score_col]].copy()
    df[text_col] = df[text_col].fillna("").astype(str).map(clean_text)
    df[score_col] = pd.to_numeric(df[score_col], errors="coerce")
    df = df.dropna(subset=[score_col])
    df = df[df[text_col].str.len() > 0]

    if df.empty:
        raise ValueError("Nenhum registro válido encontrado no dataset.")

    return df[text_col].tolist(), df[score_col].astype(float).tolist()


def split_train_test(
    texts: List[str],
    scores: List[float],
    test_size: float = 0.2,
    random_state: int = 42,
):
    if len(texts) != len(scores):
        raise ValueError("Textos e notas devem ter o mesmo tamanho.")
    if len(texts) < 2:
        raise ValueError("São necessários ao menos 2 registros para dividir treino/teste.")
    if not 0 < test_size < 1:
        raise ValueError("test_size deve estar entre 0 e 1.")

    from sklearn.model_selection import train_test_split

    return train_test_split(texts, scores, test_size=test_size, random_state=random_state)
