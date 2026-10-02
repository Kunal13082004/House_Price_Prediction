import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Page configuration
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="centered"
)

# Load dataset
data = pd.read_csv("dataset.csv")

# Features and target
X = data[["area", "bedrooms", "bathrooms", "parking", "age"]]
y = data["price"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Title
st.title("🏠 House Price Prediction")

st.write(
    "Enter the details of a house to estimate its market price using Machine Learning."
)

st.divider()

# Input section
st.subheader("🏡 House Details")

col1, col2 = st.columns(2)

with col1:
    area = st.number_input(
        "Area (sq ft)",
        min_value=500,
        value=1500,
        step=100
    )

    bedrooms = st.number_input(
        "Bedrooms",
        min_value=1,
        max_value=10,
        value=3
    )

    bathrooms = st.number_input(
        "Bathrooms",
        min_value=1,
        max_value=10,
        value=2
    )

with col2:
    parking = st.number_input(
        "Parking Spaces",
        min_value=0,
        max_value=10,
        value=2
    )

    age = st.number_input(
        "House Age (years)",
        min_value=0,
        max_value=100,
        value=5
    )

st.divider()

# Prediction
if st.button("🔮 Predict House Price", use_container_width=True):

    user_data = pd.DataFrame(
        [[area, bedrooms, bathrooms, parking, age]],
        columns=["area", "bedrooms", "bathrooms", "parking", "age"]
    )

    predicted_price = model.predict(user_data)[0]

    st.success("Prediction Completed!")

    st.metric(
        "🏠 Estimated House Price",
        f"₹{predicted_price:,.2f}"
    )

st.divider()

# Model information
st.subheader("🤖 Model Information")

col1, col2 = st.columns(2)

with col1:
    st.info("Algorithm\n\nLinear Regression")

with col2:
    st.info("Features\n\n5 House Features")

st.divider()

st.subheader("📊 Area vs House Price")

chart_data = data[["area", "price"]].set_index("area")

st.line_chart(chart_data)    