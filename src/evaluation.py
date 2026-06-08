from math import sqrt
from typing import Dict, Sequence


def evaluate_predictions(y_true: Sequence[float], y_pred: Sequence[float]) -> Dict[str, float]:
    if len(y_true) != len(y_pred):
        raise ValueError("y_true e y_pred devem ter o mesmo tamanho.")
    if not y_true:
        raise ValueError("Não há dados suficientes para avaliar.")

    errors = [true - pred for true, pred in zip(y_true, y_pred)]
    mse = sum(error**2 for error in errors) / len(errors)
    mae = sum(abs(error) for error in errors) / len(errors)

    mean_true = sum(y_true) / len(y_true)
    total_sum_squares = sum((true - mean_true) ** 2 for true in y_true)
    residual_sum_squares = sum(error**2 for error in errors)
    r2 = 0.0 if total_sum_squares == 0 else 1 - residual_sum_squares / total_sum_squares

    return {
        "mse": float(mse),
        "rmse": float(sqrt(mse)),
        "mae": float(mae),
        "r2": float(r2),
    }


def print_metrics(metrics: Dict[str, float]) -> None:
    print("Avaliação do modelo:")
    print(f"  MSE:  {metrics['mse']:.4f}")
    print(f"  RMSE: {metrics['rmse']:.4f}")
    print(f"  MAE:  {metrics['mae']:.4f}")
    print(f"  R²:   {metrics['r2']:.4f}")
