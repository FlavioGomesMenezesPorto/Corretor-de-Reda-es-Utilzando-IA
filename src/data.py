from typing import Optional

try:
    from conect import connect
    from data_processing import load_data
except ImportError:  # pragma: no cover - used when importing as a package
    from .conect import connect
    from .data_processing import load_data


def import_csv_to_database(
    csv_path: str,
    database_path: str = "IA.db",
    text_col: str = "essay",
    score_col: str = "score",
    source: Optional[str] = None,
) -> int:
    texts, scores = load_data(csv_path, text_col=text_col, score_col=score_col)

    with connect(database_path) as connection:
        for text, score in zip(texts, scores):
            cursor = connection.execute(
                "INSERT INTO essays (text, source) VALUES (?, ?)",
                (text, source or csv_path),
            )
            connection.execute(
                "INSERT INTO evaluations (essay_id, score, evaluator) VALUES (?, ?, ?)",
                (cursor.lastrowid, score, "dataset"),
            )

    return len(texts)
