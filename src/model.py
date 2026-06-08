from pathlib import Path
from typing import Dict, Sequence

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

try:
    from evaluation import evaluate_predictions, print_metrics
except ImportError:  # pragma: no cover - used when importing as a package
    from .evaluation import evaluate_predictions, print_metrics


class EssayGraderModel:
    def __init__(
        self,
        max_features: int = 5000,
        n_estimators: int = 100,
        random_state: int = 42,
    ):
        self.max_features = max_features
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.pipeline = Pipeline(
            steps=[
                (
                    "vectorizer",
                    TfidfVectorizer(max_features=max_features, ngram_range=(1, 2)),
                ),
                (
                    "regressor",
                    RandomForestRegressor(
                        n_estimators=n_estimators,
                        random_state=random_state,
                        n_jobs=-1,
                    ),
                ),
            ]
        )

    def train(self, texts: Sequence[str], scores: Sequence[float]) -> None:
        if len(texts) != len(scores):
            raise ValueError("Textos e notas devem ter o mesmo tamanho.")
        if not texts:
            raise ValueError("Não há textos para treinar.")

        print(f"Treinando modelo com {len(texts)} redações...")
        self.pipeline.fit(list(texts), list(scores))
        print("Treinamento concluído.")

    def predict(self, texts: Sequence[str]):
        if not texts:
            return []
        predictions = self.pipeline.predict(list(texts))
        return [float(round(prediction, 2)) for prediction in predictions]

    def evaluate(self, texts: Sequence[str], scores: Sequence[float]) -> Dict[str, float]:
        predictions = self.predict(texts)
        metrics = evaluate_predictions(list(scores), predictions)
        print_metrics(metrics)
        return metrics

    def save(self, filepath: str) -> None:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(
            {
                "pipeline": self.pipeline,
                "metadata": {
                    "max_features": self.max_features,
                    "n_estimators": self.n_estimators,
                    "random_state": self.random_state,
                },
            },
            path,
        )
        print(f"Modelo salvo em: {path}")

    def load(self, filepath: str) -> None:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Modelo não encontrado: {filepath}")

        data = joblib.load(path)
        self.pipeline = data["pipeline"]
        metadata = data.get("metadata", {})
        self.max_features = metadata.get("max_features", self.max_features)
        self.n_estimators = metadata.get("n_estimators", self.n_estimators)
        self.random_state = metadata.get("random_state", self.random_state)
        print(f"Modelo carregado de: {path}")
