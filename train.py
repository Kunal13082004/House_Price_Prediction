import pandas as pd
from sklearn.model_selection import train_test_split

data = pd.read_csv("dataset.csv")

X = data[["area", "bedrooms", "bathrooms", "parking", "age"]]
y = data["price"]

print("Input Data:")
print(X)

print("\nTarget Data:")
print(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTraining data:", len(X_train))
print("Testing data:", len(X_test))

from sklearn.linear_model import LinearRegression

model = LinearRegression()

model.fit(X_train, y_train)

print("\nModel trained successfully!")

# Make predictions
predictions = model.predict(X_test)

print("\nActual Prices:")
print(y_test.values)

print("\nPredicted Prices:")
print(predictions)

from sklearn.metrics import mean_absolute_error, r2_score

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\nMean Absolute Error:", mae)
print("R2 Score:", r2)

# User Input

print("\n--- House Price Prediction ---")

area = float(input("Enter area (sq ft): "))
bedrooms = int(input("Enter number of bedrooms: "))
bathrooms = int(input("Enter number of bathrooms: "))
parking = int(input("Enter number of parking spaces: "))
age = int(input("Enter house age: "))

user_data = [[area, bedrooms, bathrooms, parking, age]]

predicted_price = model.predict(user_data)

print("\nPredicted House Price: ₹", round(predicted_price[0], 2))