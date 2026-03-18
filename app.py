import streamlit as st
import numpy as np
from PIL import Image

# Dummy prediction function (since TensorFlow not supported on Streamlit Cloud)
def predict_dummy():
    return "bear", 0.92

# Streamlit UI
st.title("Animal Footprint Classification")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Dummy prediction
    label, confidence = predict_dummy()

    st.subheader("Prediction Result")
    st.write(f"Animal: {label}")
    st.write(f"Confidence: {confidence}")