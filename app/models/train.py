import pandas as pd
import joblib
import os

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from app.services.feature_engineering import extract_features

DATA_PATH = "data/raw/startup_profiles.csv"
MODEL_PATH = "app/models/xgboost_model.pkl"


def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


def build_feature_dataframe(df: pd.DataFrame):
    feature_rows = []

    for _, row in df.iterrows():
        text = row["description"]

        features = extract_features(text)
        features["success"] = row["success"]

        feature_rows.append(features)

    feature_df = pd.DataFrame(feature_rows)

    return feature_df


def train_model():
    print("🚀 Loading data...")
    df = load_data()

    print("🧠 Building features...")
    feature_df = build_feature_dataframe(df)

    X = feature_df.drop(columns=["success"])
    y = feature_df["success"]

    print("✂️ Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("🌲 Training XGBoost model...")
    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric="logloss"
    )

    model.fit(X_train, y_train)

    print("📊 Evaluating model...")
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print(f"✅ Accuracy: {acc:.2f}")

    print("💾 Saving model...")
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"🎯 Model saved at {MODEL_PATH}")


if __name__ == "__main__":
    train_model()