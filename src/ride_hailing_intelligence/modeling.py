from __future__ import annotations

import json

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .config import FEATURE_FILE, FIGURE_DIR, MODEL_DIR, REPORT_DIR


CATEGORICAL_FEATURES = [
    "city",
    "pickup_location",
    "drop_location",
    "vehicle_type",
    "payment_method",
    "distance_bucket",
    "fare_bucket",
]

NUMERIC_FEATURES = [
    "ride_distance",
    "booking_value",
    "driver_rating",
    "customer_rating",
    "wait_time",
    "hour",
    "day_of_week",
    "is_weekend",
    "is_peak_hour",
    "fare_per_km",
    "segment_bookings",
    "segment_avg_wait",
    "segment_avg_fare",
    "segment_avg_distance",
    "city_bookings",
    "city_avg_fare",
]


def _available_features(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    categorical = [col for col in CATEGORICAL_FEATURES if col in df.columns]
    numeric = [col for col in NUMERIC_FEATURES if col in df.columns]
    return categorical, numeric


def _build_preprocessor(categorical_features: list[str], numeric_features: list[str]) -> ColumnTransformer:
    categorical_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    numeric_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("cat", categorical_pipe, categorical_features),
            ("num", numeric_pipe, numeric_features),
        ]
    )


def train_cancellation_model(input_file=FEATURE_FILE) -> dict[str, object]:
    df = pd.read_csv(input_file)
    categorical_features, numeric_features = _available_features(df)
    features = categorical_features + numeric_features
    target = "is_cancelled"

    if df[target].nunique() < 2:
        raise ValueError("The target column has only one class. Need both cancelled and non-cancelled rides.")

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    preprocessor = _build_preprocessor(categorical_features, numeric_features)
    models = {
        "logistic_regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "random_forest": RandomForestClassifier(
            n_estimators=350,
            min_samples_leaf=10,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),
        "hist_gradient_boosting": HistGradientBoostingClassifier(
            learning_rate=0.06,
            max_iter=300,
            l2_regularization=0.05,
            random_state=42,
        ),
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    metrics: dict[str, object] = {}
    best_name = ""
    best_auc = -1.0
    best_pipeline: Pipeline | None = None

    for name, estimator in models.items():
        pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", estimator)])
        cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="roc_auc", n_jobs=-1)
        pipeline.fit(X_train, y_train)
        probabilities = pipeline.predict_proba(X_test)[:, 1]
        predictions = (probabilities >= 0.5).astype(int)
        auc = roc_auc_score(y_test, probabilities)

        metrics[name] = {
            "cv_roc_auc_mean": float(cv_scores.mean()),
            "cv_roc_auc_std": float(cv_scores.std()),
            "test_roc_auc": float(auc),
            "test_pr_auc": float(average_precision_score(y_test, probabilities)),
            "classification_report": classification_report(y_test, predictions, output_dict=True),
            "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
        }

        if auc > best_auc:
            best_auc = auc
            best_name = name
            best_pipeline = pipeline

    assert best_pipeline is not None
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_pipeline, MODEL_DIR / "cancellation_model.joblib")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    metrics["best_model"] = best_name
    metrics["best_test_roc_auc"] = float(best_auc)
    (REPORT_DIR / "model_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    _plot_confusion_matrix(metrics[best_name]["confusion_matrix"], best_name)
    _plot_permutation_importance(best_pipeline, X_test, y_test, features)

    print(f"Best model: {best_name}")
    print(f"Best test ROC-AUC: {best_auc:.4f}")
    return metrics


def _plot_confusion_matrix(matrix: list[list[int]], model_name: str) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(5, 4))
    sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues", cbar=False)
    plt.title(f"Confusion Matrix - {model_name}")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "confusion_matrix.png", dpi=140)
    plt.close()


def _plot_permutation_importance(model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series, features: list[str]) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    result = permutation_importance(
        model,
        X_test,
        y_test,
        n_repeats=5,
        random_state=42,
        scoring="roc_auc",
        n_jobs=-1,
    )
    importance = (
        pd.DataFrame({"feature": features, "importance": result.importances_mean})
        .sort_values("importance", ascending=False)
        .head(15)
    )
    importance.to_csv(REPORT_DIR / "feature_importance.csv", index=False)

    plt.figure(figsize=(9, 5))
    sns.barplot(data=importance, x="importance", y="feature", color="#2A6FBB")
    plt.title("Top Cancellation Model Features")
    plt.xlabel("Permutation Importance")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "feature_importance.png", dpi=140)
    plt.close()


if __name__ == "__main__":
    train_cancellation_model()
