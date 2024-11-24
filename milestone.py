import streamlit as st
import numpy as np
from streamlit_option_menu import option_menu
import uuid
import json
from plotly import graph_objects as go
import boto3


DYNAMODB_TABLE='Milestone'



def save_to_dynamodb(item):
    session = boto3.Session(
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY"],
        aws_secret_access_key=st.secrets["AWS_SECRET_KEY"],
        region_name=st.secrets["AWS_REGION"]
    )
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE)

    # Save item to the table
    response = table.put_item(Item=item)
    return response


# dynamodb = save_to_dynamodb()
# Initialize DynamoDB



def milestone_tracker():
    st.header("Child Development & Health Tracker")

    # Define comprehensive milestone categories by age
    milestone_categories = {
        "0-3 months": {
            "Physical": [
                "Raises head and chest when lying on stomach",
                "Stretches legs out and kicks when lying on back",
                "Opens and shuts hands",
                "Brings hands to mouth",
                "Pushes down on legs when feet are on hard surface"
            ],
            "Cognitive": [
                "Watches faces intently",
                "Follows moving objects with eyes",
                "Recognizes familiar objects at a distance",
                "Begins to act bored if activity doesn't change"
            ],
            "Social/Emotional": [
                "Begins to smile at people",
                "Tries to look at parent/caregiver",
                "Calms down when spoken to or picked up",
                "Makes pleasure sounds",
                "Cries differently for different needs"
            ],
            "Language": [
                "Makes cooing sounds",
                "Turns head toward sounds",
                "Cries differently for different needs",
                "Begins to imitate some sounds"
            ]
        },
        "4-6 months": {
            "Physical": [
                "Rolls over in both directions",
                "Begins to sit without support",
                "Supports whole weight on legs",
                "Rocks back and forth",
                "Begins to crawl"
            ],
            "Cognitive": [
                "Knows familiar faces",
                "Likes to play with others",
                "Responds to sounds by making sounds",
                "Brings things to mouth",
                "Shows curiosity and tries to get things out of reach"
            ],
            "Social/Emotional": [
                "Knows familiar faces",
                "Likes to play with others",
                "Responds to other people's emotions",
                "Often seems happy",
                "Likes to look at self in mirror"
            ],
            "Language": [
                "Responds to sounds by making sounds",
                "Strings vowels together when babbling",
                "Responds to own name",
                "Makes sounds to show joy and displeasure",
                "Begins to say consonant sounds"
            ]
        },
        "7-12 months": {
            "Physical": [
                "Gets to sitting position without help",
                "Crawls forward on belly",
                "Pulls up to stand",
                "Walks holding on to furniture",
                "May take a few steps without holding on"
            ],
            "Cognitive": [
                "Explores objects in different ways",
                "Finds hidden objects easily",
                "Looks where pointed",
                "Puts things in a container",
                "Pokes with index finger"
            ],
            "Social/Emotional": [
                "Shy or anxious with strangers",
                "Cries when parent leaves",
                "Has favorite things and people",
                "Shows fear in some situations",
                "Hands you a book to read"
            ],
            "Language": [
                "Responds to simple spoken requests",
                "Uses simple gestures like shaking head for 'no'",
                "Makes a lot of different sounds",
                "Says 'mama' and 'dada'",
                "Tries to imitate words"
            ]
        },
        "1-2 years": {
            "Physical": [
                "Walks alone",
                "Pulls toys while walking",
                "Carries large toys while walking",
                "Begins to run",
                "Climbs onto and down from furniture"
            ],
            "Cognitive": [
                "Knows what ordinary things are for",
                "Points to get others' attention",
                "Shows interest in a doll or stuffed animal",
                "Begins make-believe play",
                "Sorts shapes and colors"
            ],
            "Social/Emotional": [
                "Copies others",
                "Gets excited when with other children",
                "Shows increasing independence",
                "Shows defiant behavior",
                "Plays mainly beside other children"
            ],
            "Language": [
                "Says several single words",
                "Says and shakes head 'no'",
                "Points to show someone what they want",
                "Points to things when named",
                "Knows names of familiar people and body parts"
            ]
        },
        "2-3 years": {
            "Physical": [
                "Climbs well",
                "Runs easily",
                "Pedals a tricycle",
                "Walks up and down stairs",
                "Throws ball overhand"
            ],
            "Cognitive": [
                "Builds towers of more than 6 blocks",
                "Completes sentences and rhymes in familiar books",
                "Plays make-believe with dolls, animals, and people",
                "Does puzzles with 3 or 4 pieces",
                "Understands what two means"
            ],
            "Social/Emotional": [
                "Copies adults and friends",
                "Shows affection for friends without prompting",
                "Takes turns in games",
                "Shows concern for crying friend",
                "Separates easily from parents"
            ],
            "Language": [
                "Follows 2- or 3-step directions",
                "Can name most familiar things",
                "Says words like 'I,' 'me,' 'we,' and 'you'",
                "Talks well enough for strangers to understand",
                "Carries on a conversation using 2-3 sentences"
            ]
        }
    }

    # Create tabs for different tracking features
    tab1, tab2, tab3 = st.tabs(["Milestone Tracking", "Health Tracking", "Progress Dashboard"])

    with tab1:
        st.subheader("Developmental Milestones")

        with st.form("milestone_form"):
            col1, col2 = st.columns(2)

            with col1:
                age_range = st.selectbox("Select Age Range", list(milestone_categories.keys()))
                milestone_date = st.date_input("Date of Observation")

            with col2:
                child_name = st.text_input("Child's Name")
                current_age = st.number_input("Current Age (months)", min_value=0, max_value=36)

            st.write("---")

            # Create columns for different developmental domains
            domains = list(milestone_categories[age_range].keys())
            cols = st.columns(len(domains))

            milestone_status = {}

            for idx, domain in enumerate(domains):
                with cols[idx]:
                    st.markdown(f"**{domain}**")
                    for milestone in milestone_categories[age_range][domain]:
                        status = st.checkbox(milestone, key=f"{domain}_{milestone}")
                        milestone_status[f"{domain}_{milestone}"] = status

            notes = st.text_area("Additional Notes/Observations")

            if st.form_submit_button("Save Milestone Entry"):
                milestone_data = {
                    "ID": str(uuid.uuid4()),
                    "ChildName": child_name,
                    "Age": current_age,
                    "AgeRange": age_range,
                    "Date": str(milestone_date),
                    "Milestones": milestone_status,
                    "Notes": notes,
                    "Username": st.session_state.get('username', ''),
                    "Type": "milestone"
                }
                if save_to_dynamodb(milestone_data):
                    st.success("Milestone entry saved successfully!")
                else:
                    st.error("Failed to save milestone entry. Please try again.")

    with tab2:
        st.subheader("Daily Health Tracking")

        with st.form("health_tracker_form"):
            col1, col2 = st.columns(2)

            with col1:
                health_date = st.date_input("Date", key="health_date")
                temperature = st.number_input("Temperature (°C)", min_value=35, max_value=42, value=37)
                sleep_hours = st.number_input("Sleep Duration (hours)", min_value=0, max_value=24)
                weight = st.number_input("Weight (kg)", min_value=0, max_value=30)
                height = st.number_input("Height (cm)", min_value=0, max_value=150)

            with col2:
                mood = st.select_slider("Mood", options=["😢", "😐", "🙂", "😊", "😄"])
                appetite = st.select_slider("Appetite", options=["Poor", "Fair", "Good", "Excellent"])
                energy_level = st.select_slider("Energy Level", options=["Low", "Moderate", "High"])

                symptoms = st.multiselect(
                    "Any Symptoms?",
                    ["None", "Fever", "Cough", "Runny Nose", "Stomach Ache", "Headache",
                     "Rash", "Diarrhea", "Vomiting", "Loss of Appetite", "Other"]
                )

            health_notes = st.text_area("Additional Health Notes")

            if st.form_submit_button("Save Health Entry"):
                health_data = {
                    "ID": str(uuid.uuid4()),
                    "Date": str(health_date),
                    "Temperature": temperature,
                    "SleepHours": sleep_hours,
                    "Weight": weight,
                    "Height": height,
                    "Mood": mood,
                    "Appetite": appetite,
                    "EnergyLevel": energy_level,
                    "Symptoms": symptoms,
                    "Notes": health_notes,
                    "Username": st.session_state.get('username', ''),
                    "Type": "health_track"
                }
                if save_to_dynamodb(health_data):
                    st.success("Health entry saved successfully!")
                else:
                    st.error("Failed to save health entry. Please try again.")


    with tab3:
        st.subheader("Development Progress Dashboard")

        # Mock data for demonstration - in real app, calculate from database
        col1, col2 = st.columns(2)

        with col1:
            # Milestone completion rates
            domains = ["Physical", "Cognitive", "Social/Emotional", "Language"]
            completion_rates = [75, 80, 65, 70]

            fig1 = go.Figure(data=[
                go.Bar(
                    x=domains,
                    y=completion_rates,
                    marker_color=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']
                )
            ])

            fig1.update_layout(
                title="Development Progress by Domain",
                yaxis_title="Completion Rate (%)",
                showlegend=False
            )

            st.plotly_chart(fig1)

        with col2:
            # Growth tracking
            months = [0, 2, 4, 6, 8, 10, 12]
            weight = [3.5, 5.0, 6.5, 7.5, 8.5, 9.0, 9.5]
            height = [50, 55, 60, 65, 70, 73, 75]

            fig2 = go.Figure()

            fig2.add_trace(go.Scatter(
                x=months,
                y=weight,
                name="Weight (kg)",
                line=dict(color='#FF9999')
            ))

            fig2.add_trace(go.Scatter(
                x=months,
                y=height,
                name="Height (cm)",
                line=dict(color='#66B2FF'),
                yaxis="y2"
            ))

            fig2.update_layout(
                title="Growth Tracking",
                yaxis=dict(title="Weight (kg)", titlefont=dict(color="#FF9999")),
                yaxis2=dict(title="Height (cm)", titlefont=dict(color="#66B2FF"),
                            overlaying="y", side="right")
            )

            st.plotly_chart(fig2)

        # Health metrics summary
        st.write("---")
        st.subheader("Recent Health Summary")

        summary_cols = st.columns(4)
        with summary_cols[0]:
            st.metric("Average Sleep", "10.5 hrs", "+0.5")
        with summary_cols[1]:
            st.metric("Average Temperature", "37.0 °C", "-0.2")
        with summary_cols[2]:
            st.metric("Most Common Mood", "😊", "stable")
        with summary_cols[3]:
            st.metric("Appetite Trend", "Good", "+1")


