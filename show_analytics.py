import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def analytics():
    st.header("Health Analytics Dashboard")
    
    # Mock data for demonstration
    dates = pd.date_range(start='2024-01-01', end='2024-03-23', freq='D')
    weights = np.random.normal(15, 0.5, len(dates))  # Mock weight data
    heights = np.random.normal(100, 1, len(dates))   # Mock height data
    
    # Growth Chart
    fig1 = px.line(
        x=dates, y=weights,
        title="Weight Progress Over Time",
        labels={"x": "Date", "y": "Weight (kg)"}
    )
    st.plotly_chart(fig1)
    
    # Height Chart
    fig2 = px.line(
        x=dates, y=heights,
        title="Height Progress Over Time",
        labels={"x": "Date", "y": "Height (cm)"}
    )
    st.plotly_chart(fig2)
    
    # BMI Calculator and Tracker
    st.subheader("BMI Tracking")
    col1, col2 = st.columns(2)
    
    with col1:
        current_weight = st.number_input("Current Weight (kg)", min_value=0.0, value=15.0)
        current_height = st.number_input("Current Height (m)", min_value=0.0, value=1.0)
        
    with col2:
        if current_height > 0:
            bmi = current_weight / (current_height ** 2)
            st.metric("Current BMI", f"{bmi:.2f}")
            
            # BMI Category
            if bmi < 18.5:
                st.warning("Underweight")
            elif 18.5 <= bmi < 25:
                st.success("Normal weight")
            else:
                st.warning("Overweight")