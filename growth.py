import streamlit as st
import boto3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import numpy as np
from streamlit_option_menu import option_menu
import uuid
import json
from datetime import datetime
from groq import Groq

#AWS DynamoDB Configuration
DYNAMODB_TABLE = "ChildHealthRecords"

def initialize_aws_clients():
    session = boto3.Session(
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY"],
        aws_secret_access_key=st.secrets["AWS_SECRET_KEY"],
        region_name=st.secrets["AWS_REGION"]
    )
    dynamodb = session.resource('dynamodb')
    return dynamodb

# Initialize DynamoDB
dynamodb = initialize_aws_clients()
table = dynamodb.Table(DYNAMODB_TABLE)


client = Groq(
    api_key="YOUR-API-KEY"
)

def get_ai_insights(profile_data):
    # Construct a prompt for medical insights based on profile data
    prompt = f"""
    Imagine you are a pediatrician. Based on the following child's medical profile, provide a very brief response in single point for:

Key health observations(bold heading),
Dietary suggestions and physical activity recommendations(bold heading),
Future health suggestion(bold heading).
Child's Profile:

Name: {profile_data['Name']}
Age: {profile_data['DOB']}
Gender: {profile_data['Gender']}
Blood Group: {profile_data['BloodGroup']}
Weight: {profile_data['Weight']} kg
Height: {profile_data['Height']} cm
Allergies: {', '.join(profile_data['Allergies'])}
Chronic Conditions: {', '.join(profile_data['ChronicConditions'])}
Current Medications: {profile_data['CurrentMedications']}
Output Format:

Key Health Observations:
[Brief observation]

Preventive Care Recommendations:
[Brief preventive care advice]

Dietary & Physical Activity Recommendations:
[Brief suggestions for diet and activity level]
    """
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting AI insights: {str(e)}"

def manage_child_profile():
    st.header("Child Profile Management")
    
    # Initialize session state for AI insights if not already set
    if "ai_insights" not in st.session_state:
        st.session_state["ai_insights"] = None

    with st.form("child_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Child's Name")
            dob = st.date_input("Date of Birth")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            
        with col2:
            weight = st.number_input("Weight (kg)", min_value=10, max_value=100)
            height = st.number_input("Height (cm)", min_value=50, max_value=200)
            allergies = st.multiselect("Allergies", ["None", "Peanuts", "Dairy", "Eggs", "Other"])
            emergency_contact = st.text_input("Emergency Contact")
            
        # Medical History
        st.subheader("Medical History")
        chronic_conditions = st.multiselect(
            "Chronic Conditions",
            ["None", "Asthma", "Diabetes", "Epilepsy", "Other"]
        )
        
        past_surgeries = st.text_area("Past Surgeries/Procedures")
        current_medications = st.text_area("Current Medications")
        
        if st.form_submit_button("Save Profile"):
            profile_data = {
                "ID": str(uuid.uuid4()),
                "Name": name,
                "DOB": str(dob),
                "Gender": gender,
                "BloodGroup": blood_group,
                "Weight": weight,
                "Height": height,
                "Allergies": allergies,
                "EmergencyContact": emergency_contact,
                "ChronicConditions": chronic_conditions,
                "PastSurgeries": past_surgeries,
                "CurrentMedications": current_medications,
                "LastUpdated": str(datetime.now()),
                "Username": st.session_state.get('username', '')
            }

            # Generate and store AI insights in session state
            with st.spinner("Generating medical insights..."):
                insights = get_ai_insights(profile_data)
                st.session_state["ai_insights"] = insights
                st.markdown(insights)
            
            # Save to DynamoDB
            try:
                table.put_item(Item=profile_data)
                st.success("Profile saved successfully!")
                
            except Exception as e:
                st.error(f"Error saving profile: {str(e)}")
        else:
            # If no new insights are generated, display existing ones
            if st.session_state["ai_insights"]:
                st.markdown(st.session_state["ai_insights"])

    # Custom Query Section
    st.subheader("Ask Medical Questions")
    user_query = st.text_input("Enter your medical query:")
    if st.button("Get Answer"):
        if user_query:
            with st.spinner("Getting response..."):
                try:
                    response = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": f"As a medical professional, please answer this question: {user_query}"
                            }
                        ],
                        model="llama-3.1-8b-instant",
                    )
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error getting response: {str(e)}")
        else:
            st.warning("Please enter a query first.")


