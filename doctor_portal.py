import streamlit as st

def doctor():
    st.header("Doctor's Portal")
    
    if st.session_state.get('user_type') != 'Doctor':
        st.warning("Access restricted to medical professionals.")
        return
    
    # Patient List
    st.subheader("Patient List")
    
    # Mock patient data
    patients = [
        {"name": "John Doe", "age": 5, "last_visit": "2024-03-15"},
        {"name": "Jane Smith", "age": 3, "last_visit": "2024-03-18"},
        {"name": "Mike Johnson", "age": 7, "last_visit": "2024-03-20"},
    ]
    
    for patient in patients:
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            st.write(f"**{patient['name']}**")
        with col2:
            st.write(f"Age: {patient['age']}")
        with col3:
            st.write(f"Last Visit: {patient['last_visit']}")
            
        if st.button(f"View Details - {patient['name']}"):
            st.info("Patient Details")
            st.json({
                "Name": patient['name'],
                "Age": patient['age'],
                "Medical History": "No significant issues",
                "Allergies": "None",
                "Recent Symptoms": "Mild fever",
                "Current Medications": "None"
            })