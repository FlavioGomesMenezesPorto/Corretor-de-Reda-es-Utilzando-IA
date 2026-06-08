from src.evaluation import evaluate_predictions


def test_evaluate_predictions_returns_expected_keys():
    metrics = evaluate_predictions([10.0, 8.0, 6.0], [9.0, 8.5, 6.5])

    assert set(metrics) == {"mse", "rmse", "mae", "r2"}
    assert metrics["mae"] > 0
