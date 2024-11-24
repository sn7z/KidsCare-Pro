import streamlit as st
import pywhatkit
import datetime
import json
import re
from datetime import timedelta, time

def validate_phone_number(phone_number):
    """Validate Indian phone number format."""
    pattern = r'^\+91[6-9]\d{9}$'
    return bool(re.match(pattern, phone_number))

def schedule_whatsapp_notification(sender_phone, recipient_phone, message, scheduled_date, scheduled_time):
    """Schedule a WhatsApp notification."""
    try:
        # Combine date and time
        scheduled_datetime = datetime.datetime.combine(scheduled_date, scheduled_time)
        
        # Check if scheduled time is in the past
        if scheduled_datetime <= datetime.datetime.now():
            st.error("Cannot schedule notifications in the past")
            return False
        
        # Validate both phone numbers
        if not validate_phone_number(sender_phone):
            st.error("Invalid sender phone number format")
            return False
        if not validate_phone_number(recipient_phone):
            st.error("Invalid recipient phone number format")
            return False
            
        # Configure PyWhatKit with sender's phone
        
        
        # Send message
        pywhatkit.sendwhatmsg(
            recipient_phone,
            message,
            scheduled_time.hour,
            scheduled_time.minute,
            wait_time=20,
            tab_close=True
        )
        return True
    except Exception as e:
        st.error(f"Error scheduling notification: {str(e)}")
        return False

def save_notification_settings(settings):
    """Save notification preferences to session state."""
    if 'notification_settings' not in st.session_state:
        st.session_state.notification_settings = {}
    st.session_state.notification_settings.update(settings)

def show_notification_scheduler(sender_phone, recipient_phone, notification_type):
    """Show the notification scheduler UI for a given notification type."""
    col1, col2 = st.columns(2)
    
    with col1:
        scheduled_date = st.date_input(
            "Select Date",
            value=datetime.datetime.now().date() + timedelta(days=1),
            min_value=datetime.datetime.now().date(),
            key=f'date_{notification_type}'
        )
    
    with col2:
        scheduled_time = st.time_input(
            "Select Time",
            value=datetime.time(9, 0),
            key=f'time_{notification_type}'
        )
    
    custom_message = st.text_area(
        "Custom Message (optional)",
        key=f'message_{notification_type}'
    )
    
    return scheduled_date, scheduled_time, custom_message

def show_dashboard(username):
    st.title("👋 Welcome to KidsCare Pro")
    
    # Notification Settings
    with st.sidebar:
        st.subheader("📱 Phone Configuration")
        
        # Phone Numbers Configuration Section
        with st.expander("Phone Numbers", expanded=True):
            sender_phone = st.text_input(
                "Your WhatsApp Number (with +91)",
                value=st.session_state.get('sender_phone', ''),
                key='sender_phone_input',
                help="This is the phone number you'll use to send notifications from"
            )
            
            recipient_phone = st.text_input(
                "Recipient's WhatsApp Number (with +91)",
                value=st.session_state.get('recipient_phone', ''),
                key='recipient_phone_input',
                help="This is the phone number that will receive notifications"
            )
            
            # Validate phone numbers as they're entered
            if sender_phone and not validate_phone_number(sender_phone):
                st.error("Invalid sender phone number format. Use +91 followed by 10 digits")
            if recipient_phone and not validate_phone_number(recipient_phone):
                st.error("Invalid recipient phone number format. Use +91 followed by 10 digits")

    # Dashboard Layout
    col1, col2, col3 = st.columns(3)
    
    # Last Check-up Card
    with col1:
        st.info("Last Check-up\n\n2 weeks ago")
        with st.expander("Schedule Checkup Reminder"):
            scheduled_date, scheduled_time, custom_message = show_notification_scheduler(
                sender_phone, recipient_phone, "checkup"
            )
            default_message = "🏥 Reminder: It's time for your child's regular checkup!"
            message = custom_message if custom_message else default_message
            
            if st.button("Schedule Checkup Reminder"):
                if schedule_whatsapp_notification(
                    sender_phone, 
                    recipient_phone, 
                    message, 
                    scheduled_date, 
                    scheduled_time
                ):
                    st.success(f"Checkup reminder scheduled for {scheduled_date} at {scheduled_time}")

    # Vaccination Card
    with col2:
        st.success("Upcoming Vaccination\n\nMMR Booster")
        with st.expander("Schedule Vaccination Reminder"):
            scheduled_date, scheduled_time, custom_message = show_notification_scheduler(
                sender_phone, recipient_phone, "vaccination"
            )
            default_message = "💉 Reminder: MMR Booster vaccination is due!"
            message = custom_message if custom_message else default_message
            
            if st.button("Schedule Vaccination Reminder"):
                if schedule_whatsapp_notification(
                    sender_phone, 
                    recipient_phone, 
                    message, 
                    scheduled_date, 
                    scheduled_time
                ):
                    st.success(f"Vaccination reminder scheduled for {scheduled_date} at {scheduled_time}")

    # Doctor Visit Card
    with col3:
        st.warning("Next Doctor Visit\n\nIn 3 days")
        with st.expander("Schedule Visit Reminder"):
            scheduled_date, scheduled_time, custom_message = show_notification_scheduler(
                sender_phone, recipient_phone, "doctor_visit"
            )
            default_message = "👨‍⚕️ Reminder: Doctor's appointment!"
            message = custom_message if custom_message else default_message
            
            if st.button("Schedule Visit Reminder"):
                if schedule_whatsapp_notification(
                    sender_phone, 
                    recipient_phone, 
                    message, 
                    scheduled_date, 
                    scheduled_time
                ):
                    st.success(f"Doctor visit reminder scheduled for {scheduled_date} at {scheduled_time}")

    #Recent Activity Timeline
    st.subheader("Recent Activity")
    activities = [
        {"date": "2024-03-20", "event": "Height measurement updated"},
        {"date": "2024-03-18", "event": "Completed vaccination"},
        {"date": "2024-03-15", "event": "Doctor's appointment"},
    ]

    # Display activities with notification options
    for activity in activities:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{activity['date']}**: {activity['event']}")
        with col2:
            if activity['event'].startswith("Height"):
                with st.expander("Share Update"):
                    scheduled_date, scheduled_time, custom_message = show_notification_scheduler(
                        sender_phone, recipient_phone, f"growth_{activity['date']}"
                    )
                    default_message = f"📊 Growth Update: New height measurement recorded on {activity['date']}"
                    message = custom_message if custom_message else default_message
                    
                    if st.button("Share Update", key=f"share_{activity['date']}"):
                        if schedule_whatsapp_notification(
                            sender_phone, 
                            recipient_phone, 
                            message, 
                            scheduled_date, 
                            scheduled_time
                        ):
                            st.success(f"Update will be shared on {scheduled_date} at {scheduled_time}")

