import streamlit as st
import uuid
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError


import boto3
import uuid
import streamlit as st

DYNAMODB_TABLE = 'Appointments'

def book1():
    # AWS Configuration
    try:
        # Initialize DynamoDB resource
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=st.secrets["AWS_ACCESS_KEY"],
            aws_secret_access_key=st.secrets["AWS_SECRET_KEY"],
            region_name=st.secrets["AWS_REGION"]
        )
        table = dynamodb.Table(DYNAMODB_TABLE)

        # Success message
        st.success("Connected to AWS DynamoDB successfully!")

        # Appointment Booking Input
        st.write("Book an Appointment")
        name = st.text_input("Enter your name:")
        appointment_date = st.date_input("Select an appointment date:")
        appointment_time = st.time_input("Select an appointment time:")

        if st.button("Book Appointment"):
            if name and appointment_date and appointment_time:
                # Generate a unique AppointmentID
                appointment_id = str(uuid.uuid4())

                # Prepare the item
                item = {
                    "AppointmentID": appointment_id,  # Primary key
                    "Name": name,
                    "Date": str(appointment_date),
                    "Time": str(appointment_time)
                }

                # Save the item to DynamoDB
                response = table.put_item(Item=item)
                st.success("Appointment booked successfully!")
                st.write(f"Your Appointment ID: {appointment_id}")
                st.json(response)
            else:
                st.warning("Please fill in all fields.")
    except Exception as e:
        # Error Handling
        st.error(f"AWS Connection Error: {str(e)}")
        st.warning("App will run in demo mode without saving data.")


    # Main app
    st.title("Pediatric Appointment Booking")

    # Create two columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Child Details")
        child_name = st.text_input("Child's Name*")
        child_age = st.number_input("Child's Age (in years)*", 0, 18, 5)
        parent_contact = st.text_input("Parent's Contact Number*")

    with col2:
        st.subheader("Appointment Details")
        appointment_date = st.date_input(
            "Select Date*",
            min_value=datetime.today().date(),
            max_value=datetime.today().date() + timedelta(days=30)
        )
        
        appointment_time = st.time_input(
            "Select Time*",
            value=datetime.strptime("09:00", "%H:%M").time()
        )
        
        purpose = st.selectbox(
            "Purpose of Visit*",
            ["General Check-up", "Vaccination", "Follow-up", "Health Concern", "Other"]
        )

    additional_notes = st.text_area("Additional Notes (Optional)")

    if st.button("Book Appointment", use_container_width=True):
        # Validate inputs
        if not all([child_name, parent_contact]):
            st.error("Please fill in all required fields!")
        else:
            # Generate appointment ID
            appointment_id = str(uuid.uuid4())
            
            # Create appointment data
            appointment_data = {
                "AppointmentID": appointment_id,
                "ChildName": child_name,
                "ChildAge": child_age,
                "ParentContact": parent_contact,
                "AppointmentDate": str(appointment_date),
                "AppointmentTime": appointment_time.strftime("%H:%M"),
                "Purpose": purpose,
                "AdditionalNotes": additional_notes,
                "CreatedAt": datetime.now().isoformat(),
                "Status": "Scheduled"
            }
            
            try:
                # Try to save to DynamoDB
                table.put_item(Item=appointment_data)
                st.success("✅ Appointment booked successfully!")
                
                # Show appointment details
                st.info(f"""
                📋 Appointment Details:
                - Appointment ID: {appointment_id}
                - Date: {appointment_date}
                - Time: {appointment_time.strftime("%I:%M %p")}
                - Child: {child_name}
                
                Please save your appointment ID for reference.
                """)
                
            except Exception as e:
                st.error(f"Error saving appointment: {str(e)}")
                st.info("Running in demo mode - appointment details shown but not saved.")
                # Show appointment details anyway
                st.warning(f"""
                📋 Demo Appointment Details:
                - Appointment ID: {appointment_id}
                - Date: {appointment_date}
                - Time: {appointment_time.strftime("%I:%M %p")}
                - Child: {child_name}
                """)

    # Add some helpful information at the bottom
    st.markdown("---")
    st.markdown("### ℹ️ Important Information")
    st.markdown("""
    - Appointments are available Monday through Friday
    - Office hours are 9:00 AM to 5:00 PM
    - Please arrive 15 minutes before your appointment
    - Bring your child's medical records if available
    """)