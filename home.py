import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px



def Home_Page():
    # Create two columns - left for login, right for content
    st.tabs(["Home",])
    col_left, col_right = st.columns([1, 3])
    
    with col_left:
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        user_type = st.selectbox("Login as", ["Parent", "Doctor"])
        
        if st.button("Login"):
            if username and password:  # Add proper authentication logic
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['user_type'] = user_type
                st.rerun()
    # with st.tabs("Home"):
        with col_right:
            st.title("Welcome to KidsCare Pro")
            st.write("KidsCare Pro is a comprehensive platform designed to provide parents with a comprehensive solution for monitoring and managing their children's health.")
            st.write("Our platform offers a range of features to help parents monitor their children's health, including:")
            st.write("- Health Monitoring: Track vital signs, feeding, and sleep patterns to ensure optimal growth and development.")
            st.write("- Medical History: Access medical history and medical records to identify any potential health concerns.")
            st.write("- Health Suggestions: Get personalized health suggestions based on child data to help parents make informed decisions.")
            st.write("- Health Education: Access educational resources to learn more about healthy habits and lifestyle changes.")
            
            # Key Insights Section
            st.subheader("📊 Child Health Insights")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Global Child Health Index", "78%", "+2.1%")
            with col2:
                st.metric("Vaccination Coverage", "92%", "+1.5%")
            with col3:
                st.metric("Child Wellness Score", "85%", "+3.2%")
            
            # Graphs Section
            st.subheader("📈 Health Trends")
            
            # Graph 1: Child Health Metrics
            dates = pd.date_range(start='2023-01-01', end='2024-03-01', freq='M')
            health_scores = np.random.normal(85, 5, size=len(dates))
            wellness_trends = pd.DataFrame({
                'Date': dates,
                'Health Score': health_scores
            })
            
            fig1 = px.line(wellness_trends, x='Date', y='Health Score',
                        title='Average Child Health Scores Trend')
            st.plotly_chart(fig1)
            
            # Graph 2: Age-wise Development Milestones
            age_groups = ['0-1', '1-2', '2-3', '3-4', '4-5']
            milestones = [95, 88, 92, 85, 90]
            
            fig2 = go.Figure(data=[
                go.Bar(x=age_groups, y=milestones,
                    marker_color=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC'])
            ])
            fig2.update_layout(title='Age-wise Development Milestone Achievement (%)')
            st.plotly_chart(fig2)
            
            # Related Articles
            st.subheader("📚 Featured Articles")
            articles = st.columns(2)
            
            with articles[0]:
                st.markdown("""
                * [*Understanding Child Growth Patterns*](https://www.longstreetclinic.com/child-growth-development/)
                Latest research on healthy child development
                * [*Nutrition Guidelines for Children*](https://www.mayoclinic.org/healthy-lifestyle/childrens-health/in-depth/nutrition-for-kids/art-20049335)
                Essential dietary recommendations
                """)
                
            with articles[1]:
                st.markdown("""
                * [*Importance of Early Health Monitoring*](https://danonenutriciaacademy.in/expert-article/importance-of-growth-monitoring/#:~:text=Danone%20Nutricia%20Academy-,Growth%20Monitoring%20of%20all%20children%20at%20periodic%20intervals%20(at%20least,of%20any%20chronic%20systemic%20illness.)
                Why tracking matters in child healthcare
                * [*Digital Health Management Benefits*](https://www.carecloud.com/continuum/digital-health-importance-and-benefits/)
                Modern approaches to child wellness
                """)
            
            # About Us Table
            st.write("""
        ---

        ## Meet Our Dedicated Team 👩‍⚕👨‍⚕

        We are a dynamic group of tech enthusiasts with a shared goal: using AI and technology to make healthcare accessible and effective for all. From data science to medical insights, each of us brings something unique to this mission. Connect with us below!

        | *Team Member* | *Role* | *Bio* | *LinkedIn* |
        | :-------------: | :------: | :-----: | :----------: |
        | *Huzaifah* | Machine Learning Engineer | The brain behind the algorithms, focused on creating reliable and scalable models. | [Connect](https://www.linkedin.com/in/huzaifah-27o3/) |
        | *Maaz* | Full Stack Developer | Builds seamless user interfaces for easy access and interaction with complex medical data. | [Connect](https://www.linkedin.com/in/mohammed-maaz-593042274/) |
        | *Numaan* | Data Scientist | Specializes in making sense of data, from cleaning to insightful analysis. | [Connect](https://www.linkedin.com/in/syed-numaan-22a2b52ab/) |
        | *Qavi* | Medical Consultant | Adds depth with healthcare insights to ensure accuracy and relevance in our models. | [Connect](https://www.linkedin.com/in/qavi-quadri/) |

        ---
        
        ### 💬 Get in Touch
        We're always excited to collaborate or answer questions! Reach out to any of us on LinkedIn, and let's explore the future of healthcare together. 💙
    """)
            
            # FAQ Section
            st.subheader("❓ Frequently Asked Questions")
            with st.expander("What features does KidsCare Pro offer?"):
                st.write("""
                - Comprehensive health tracking
                - Growth monitoring
                - Development milestone tracking
                - Medical history management
                - AI-powered health insights
                """)
                
            with st.expander("How secure is my child's health data?"):
                st.write("""
                We implement industry-standard security measures including:
                - End-to-end encryption
                - Secure cloud storage
                - Regular security audits
                - Compliance with healthcare data regulations
                """)
                
            with st.expander("Can I share data with my child's doctor?"):
                st.write("""
                Yes! KidsCare Pro allows secure data sharing with authorized healthcare providers through our Doctor's Portal feature.
                """)
                
            with st.expander("How do I get started?"):
                st.write("""
                Simply create an account, complete your child's profile, and start tracking their health journey. Our intuitive interface makes it easy to begin!
                """)