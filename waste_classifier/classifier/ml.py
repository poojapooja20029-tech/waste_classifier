"""Machine-learning part: preprocessing, training, evaluation, prediction."""
import joblib
import pandas as pd
from django.conf import settings
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

NUMERIC = ["weight", "size"]
CATEGORICAL = ["shape", "texture", "color"]
FEATURES = NUMERIC + CATEGORICAL


def _pipeline(estimator):
    # Preprocessing: scale numbers, one-hot encode categories
    pre = ColumnTransformer([
        ("num", StandardScaler(), NUMERIC),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])
    return Pipeline([("pre", pre), ("clf", estimator)])


def _estimators():
    return {
        "decision_tree": DecisionTreeClassifier(max_depth=8, random_state=42),
        "random_forest": RandomForestClassifier(n_estimators=150, random_state=42),
        "neural_network": MLPClassifier(hidden_layer_sizes=(32, 16), max_iter=800, random_state=42),
    }


def train_and_store():
    """Train all 3 models, save them to disk, store accuracy in the database."""
    from .models import ModelMetric, WasteSample

    df = pd.DataFrame(list(WasteSample.objects.values(*FEATURES, "waste_type")))
    if df.empty or df["waste_type"].nunique() < 2:
        raise ValueError("Not enough data. Run: python manage.py generate_dataset")

    X, y = df[FEATURES], df["waste_type"]
    stratify = y if y.value_counts().min() >= 2 else None
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=stratify
    )

    settings.MODEL_DIR.mkdir(exist_ok=True)
    results = []
    for key, est in _estimators().items():
        pipe = _pipeline(est)
        pipe.fit(X_tr, y_tr)
        acc = accuracy_score(y_te, pipe.predict(X_te)) * 100
        joblib.dump(pipe, settings.MODEL_DIR / f"{key}.joblib")
        ModelMetric.objects.create(
            model_key=key, accuracy=round(acc, 2),
            train_size=len(X_tr), test_size=len(X_te),
        )
        results.append((key, round(acc, 2)))
    return results


def predict(model_key, data):
    """Return (waste_type, confidence_percent)."""
    path = settings.MODEL_DIR / f"{model_key}.joblib"
    if not path.exists():
        raise FileNotFoundError("Model not trained yet. Run: python manage.py train_model")
    pipe = joblib.load(path)
    row = pd.DataFrame([data])[FEATURES]
    proba = pipe.predict_proba(row)[0]
    i = int(proba.argmax())
    return pipe.classes_[i], round(float(proba[i]) * 100, 2)
