import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Set MLflow tracking URI to local server
mlflow.set_tracking_uri("http://127.0.0.1:5000")

# Load dataset
data = pd.read_csv("iris.csv")

# Separate features and labels
X = data.drop("species", axis=1)
y = data["species"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train logistic regression model
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Log experiment with MLflow
with mlflow.start_run():
    mlflow.log_param("model_type", "LogisticRegression")
    mlflow.log_param("max_iter", 200)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(model, "logistic_regression_model")
    print(f"Logistic Regression model logged with accuracy: {accuracy:.4f}")
