import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df['timestamp'] = pd.to_datetime (df['timestamp'])
    df = df.sort_values(["site_id", "timestamp"]).copy()
    df["rolling_packet_loss"] = df.groupby("site_id")["packet_loss_rate"].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    df["rolling_temp"] = df.groupby("site_id")["temperature_c"].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    df["temp_spike"] = np.where(df["temperature_c"] > 62, 1, 0)
    return df.dropna()

def train_and_export_pipeline():
    data_path = os.path.join("data", "telecom_site_logs.csv")
    raw_df = pd.read_csv(data_path)
    processed_df = engineer_features(raw_df)

    feature_cols = ["traffic_volume_gb", "packet_loss_rate", "temperature_c", "rssi_dbm", "rolling_packet_loss", "rolling_temp", "temp_spike"]
    X = processed_df[feature_cols]
    y = processed_df["target_failure"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    clf = RandomForestClassifier(n_estimators=150, max_depth=10, class_weight='balanced', random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]

    print("==MODEL EVALUATION REPORT==")
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print(f"ROC AUC Score: {roc_auc_score(y_test, y_prob):.4f}")
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    export_path = os.path.join("data", "telecom_predictions_powerbi.xlsx")
    processed_df.to_excel(export_path, index=False)
    print(f"Scored dataset successfully exported to '{export_path}'.")

if __name__ == "__main__":
    train_and_export_pipeline()


#python src/rain_model.py 
#THEN
# 1. Build your Docker image:docker build -t telecom-downtime-prediction
# 2. Run the container to execute the pipeline inside Docker: docker run --rm telecom-downtime-prediction
