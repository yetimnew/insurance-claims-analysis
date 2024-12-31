import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


def preprocess_data(data):
    """Handle missing values and encode categorical variables."""
    data = data.dropna()  # Handle missing values
    data = pd.get_dummies(data, drop_first=True)  # Encode categorical variables
    return data


def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """Train and evaluate Linear Regression and Random Forest models."""
    # Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    print("Linear Regression:")
    print(f"RMSE: {mean_squared_error(y_test, y_pred_lr, squared=False)}")
    print(f"R2 Score: {r2_score(y_test, y_pred_lr)}")

    # Random Forest
    rf = RandomForestRegressor(random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    print("Random Forest:")
    print(f"RMSE: {mean_squared_error(y_test, y_pred_rf, squared=False)}")
    print(f"R2 Score: {r2_score(y_test, y_pred_rf)}")


def main():
    data = pd.read_csv("../data/data.csv")  # Adjust path as necessary

    # Preprocess data
    data = preprocess_data(data)
    X = data.drop(columns=['TotalClaims'])
    y = data['TotalClaims']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train and evaluate models
    train_and_evaluate_models(X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    main()
