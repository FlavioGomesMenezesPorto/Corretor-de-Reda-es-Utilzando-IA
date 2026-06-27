import argparse
from pathlib import Path

try:
    from conect import initialize_database
    from data import import_csv_to_database
    from data_processing import clean_texts, load_data, split_train_test
    from model import EssayGraderModel
except ImportError:  # pragma: no cover - used when importing as a package
    from .conect import initialize_database
    from .data import import_csv_to_database
    from .data_processing import clean_texts, load_data, split_train_test
    from .model import EssayGraderModel


def train(args) -> None:
    texts, scores = load_data(args.data, text_col=args.text_column, score_col=args.score_column)

    if args.test_size > 0:
        x_train, x_test, y_train, y_test = split_train_test(
            texts,
            scores,
            test_size=args.test_size,
            random_state=args.random_state,
        )
    else:
        x_train, y_train = texts, scores
        x_test, y_test = [], []

    grader = EssayGraderModel(
        max_features=args.max_features,
        n_estimators=args.n_estimators,
        random_state=args.random_state,
    )
    grader.train(x_train, y_train)
    grader.save(args.model_path)

    if x_test:
        print("\nAvaliação no conjunto de teste:")
        grader.evaluate(x_test, y_test)


def predict(args) -> None:
    raw_texts = _read_prediction_texts(args.text, args.input_file)
    grader = EssayGraderModel()
    grader.load(args.model_path)

    texts = clean_texts(raw_texts)
    predictions = grader.predict(texts)

    for original, score in zip(raw_texts, predictions):
        print(f"Texto: {original}")
        print(f"Previsão de nota: {score:.2f}")
        print("-" * 40)


def evaluate(args) -> None:
    texts, scores = load_data(args.data, text_col=args.text_column, score_col=args.score_column)
    grader = EssayGraderModel()
    grader.load(args.model_path)
    grader.evaluate(texts, scores)


def init_db(args) -> None:
    initialize_database(args.schema)
    print("Banco MySQL inicializado.")


def import_data(args) -> None:
    total = import_csv_to_database(
        args.data,
        text_col=args.text_column,
        score_col=args.score_column,
        source=args.source,
    )
    print(f"{total} redações importadas para o MySQL")


def _read_prediction_texts(text: str | None, input_file: str | None):
    if text:
        return [text]
    if input_file:
        path = Path(input_file)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {input_file}")
        return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    raise ValueError("Passe --text ou --input-file para realizar a previsão.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Corretor automático de redações")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_train = subparsers.add_parser("train", help="Treinar o modelo")
    parser_train.add_argument("--data", required=True, help="Arquivo CSV com redações")
    parser_train.add_argument("--model-path", default="models/essay_grader.joblib")
    parser_train.add_argument("--text-column", default="essay")
    parser_train.add_argument("--score-column", default="score")
    parser_train.add_argument("--test-size", type=float, default=0.2)
    parser_train.add_argument("--random-state", type=int, default=42)
    parser_train.add_argument("--max-features", type=int, default=5000)
    parser_train.add_argument("--n-estimators", type=int, default=100)
    parser_train.set_defaults(func=train)

    parser_predict = subparsers.add_parser("predict", help="Fazer previsão de nota")
    parser_predict.add_argument("--model-path", default="models/essay_grader.joblib")
    parser_predict.add_argument("--text")
    parser_predict.add_argument("--input-file")
    parser_predict.set_defaults(func=predict)

    parser_eval = subparsers.add_parser("evaluate", help="Avaliar modelo com conjunto rotulado")
    parser_eval.add_argument("--data", required=True)
    parser_eval.add_argument("--model-path", default="models/essay_grader.joblib")
    parser_eval.add_argument("--text-column", default="essay")
    parser_eval.add_argument("--score-column", default="score")
    parser_eval.set_defaults(func=evaluate)

    parser_db = subparsers.add_parser("init-db", help="Criar tabelas no MySQL")
    parser_db.add_argument("--schema", default="schema_ava.sql")
    parser_db.set_defaults(func=init_db)

    parser_import = subparsers.add_parser("import-data", help="Importar CSV para o MySQL")
    parser_import.add_argument("--data", required=True)
    parser_import.add_argument("--text-column", default="essay")
    parser_import.add_argument("--score-column", default="score")
    parser_import.add_argument("--source")
    parser_import.set_defaults(func=import_data)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
