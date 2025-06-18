from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from confluent_kafka import Producer
import json

app = Flask(__name__)
FEATURES = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']

# === Kafka Producer Setup ===
producer = Producer({'bootstrap.servers': 'localhost:57891'})
TOPIC_NAME = 'iris_app'

# === Load and Clean Dataset ===
def load_iris_dataset(csv_path='iris.csv'):
    df = pd.read_csv(csv_path)
    df = df[FEATURES]
    df.dropna(inplace=True)
    for col in FEATURES:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    return df

# === Train a model for each feature ===
def train_models(df):
    models = {}
    for target in FEATURES:
        input_features = [f for f in FEATURES if f != target]
        X = df[input_features]
        y = df[target]
        model = LinearRegression()
        model.fit(X, y)
        models[target] = model
    return models

iris_df = load_iris_dataset()
models = train_models(iris_df)

FEATURE_RANGES = {
    feature: (float(iris_df[feature].min()), float(iris_df[feature].max()))
    for feature in FEATURES
}

# === Kafka Publisher ===
def publish_to_topic(data):
    try:
        producer.produce(TOPIC_NAME, json.dumps(data).encode('utf-8'))
        producer.flush()
        print(f"✔️ Published to Kafka topic: {TOPIC_NAME}")
    except Exception as e:
        print("❌ Kafka publish error:", e)

# === Flask Route ===
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({'error': 'Invalid JSON input'}), 400

    try:
        provided = {k: float(v) for k, v in data.items() if k in FEATURES}
    except ValueError:
        return jsonify({'error': 'All feature values must be numeric'}), 400

    if len(provided) != 3:
        return jsonify({'error': 'Exactly 3 of the 4 features must be provided'}), 400

    for feature, value in provided.items():
        min_val, max_val = FEATURE_RANGES[feature]
        if not (min_val <= value <= max_val):
            return jsonify({'error': f"{feature} out of range ({min_val} - {max_val})"}), 400

    missing_feature = list(set(FEATURES) - set(provided.keys()))[0]
    input_features = [provided[f] for f in FEATURES if f != missing_feature]
    predicted_value = round(float(models[missing_feature].predict([input_features])[0]), 2)

    full_data = provided.copy()
    full_data[missing_feature] = predicted_value

    publish_to_topic(full_data)

    return jsonify({
        'predicted_feature': missing_feature,
        'predicted_value': predicted_value,
        'full_data': full_data
    })

if __name__ == '__main__':
    print("🌐 Starting Flask server at http://127.0.0.1:5000")
    app.run(debug=True)
