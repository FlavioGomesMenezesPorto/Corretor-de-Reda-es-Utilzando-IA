"""Compatibility module. Prefer importing from evaluation.py."""

try:
    from evaluation import evaluate_predictions, print_metrics
except ImportError:  
    from .evaluation import evaluate_predictions, print_metrics


__all__ = ["evaluate_predictions", "print_metrics"]
