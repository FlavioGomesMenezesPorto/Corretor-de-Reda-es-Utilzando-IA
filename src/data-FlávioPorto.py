from typing import Optional

try:
    from conect import connect
    from data_processing import load_data
except ImportError:  # pragma: no cover - used when importing as a package
    from .conect import connect
    from .data_processing import load_data


def import_csv_to_database(
    csv_path: str,
    text_col: str = "essay",
    score_col: str = "score",
    source: Optional[str] = None,
) -> int:
    texts, scores = load_data(csv_path, text_col=text_col, score_col=score_col)

    connection = connect()
    cursor = connection.cursor()
    try:
        for text, score in zip(texts, scores):
            cursor.execute(
                "INSERT INTO essays (text, source) VALUES (%s, %s)",
                (text, source or csv_path),
            )
            essay_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO evaluations (essay_id, score, evaluator) VALUES (%s, %s, %s)",
                (essay_id, score, "dataset"),
            )
        connection.commit()
    finally:
        cursor.close()
        connection.close()

    return len(texts)
