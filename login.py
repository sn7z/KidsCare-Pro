import streamlit as st
import time
import hmac
import hashlib
import base64
import boto3

# AWS Configuration
AWS_REGION = st.secrets["AWS_REGION"]
USER_POOL_ID = st.secrets["USER_POOL_ID"]
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
AWS_ACCESS_KEY = st.secrets["AWS_ACCESS_KEY"]
AWS_SECRET_KEY = st.secrets["AWS_SECRET_KEY"]

# Initialize AWS Cognito client
cognito_client = boto3.client(
    'cognito-idp',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def generate_secret_hash(username):
    """Generate Cognito secret hash."""
    message = username + CLIENT_ID
    dig = hmac.new(
        key=bytes(CLIENT_SECRET, 'utf-8'),
        msg=bytes(message, 'utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()

def authenticate_user(username, password):
    """Authenticate user with Cognito."""
    try:
        secret_hash = generate_secret_hash(username)
        response = cognito_client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
                'SECRET_HASH': secret_hash
            }
        )
        return True, response['AuthenticationResult']['AccessToken']
    except cognito_client.exceptions.UserNotConfirmedException:
        return False, 'UserNotConfirmed'
    except cognito_client.exceptions.NotAuthorizedException:
        return False, 'InvalidCredentials'
    except Exception as e:
        return False, str(e)

def register_user(username, password, email):
    """Register user with Cognito."""
    try:
        secret_hash = generate_secret_hash(username)
        cognito_client.sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            Password=password,
            SecretHash=secret_hash,
            UserAttributes=[{'Name': 'email', 'Value': email}]
        )
        return True, None
    except cognito_client.exceptions.UsernameExistsException:
        return False, "Username already exists"
    except Exception as e:
        return False, str(e)

def verify_confirmation_code(username, confirmation_code):
    """Verify the confirmation code sent to user's email."""
    try:
        secret_hash = generate_secret_hash(username)
        cognito_client.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            ConfirmationCode=confirmation_code,
            SecretHash=secret_hash
        )
        return True, None
    except cognito_client.exceptions.CodeMismatchException:
        return False, "Invalid verification code"
    except cognito_client.exceptions.ExpiredCodeException:
        return False, "Verification code has expired"
    except Exception as e:
        return False, str(e)

def resend_confirmation_code(username):
    """Resend confirmation code to user's email."""
    try:
        secret_hash = generate_secret_hash(username)
        cognito_client.resend_confirmation_code(
            ClientId=CLIENT_ID,
            Username=username,
            SecretHash=secret_hash
        )
        return True, None
    except Exception as e:
        return False, str(e)

def login_page():
    """Render login and registration options."""
    st.title("🏥 MedTech Pro - Login")
    
    # Initialize session state variables if they don't exist
    if 'registration_complete' not in st.session_state:
        st.session_state.registration_complete = False
    if 'pending_verification_username' not in st.session_state:
        st.session_state.pending_verification_username = None
    
    tab1, tab2, tab3 = st.tabs(["Login", "Register", "Verify Account"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                if username and password:
                    success, result = authenticate_user(username, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("Login successful!")
                        time.sleep(1)
                        st.experimental_rerun()
                    elif result == 'UserNotConfirmed':
                        st.warning("Please verify your email before logging in.")
                        st.session_state.pending_verification_username = username
                        st.session_state.registration_complete = True
                    else:
                        st.error("Invalid credentials")
                else:
                    st.error("Please enter both username and password.")

    with tab2:
        with st.form("registration_form"):
            username = st.text_input("Username*")
            password = st.text_input(
                "Password*", 
                type="password", 
                help="Must be at least 8 characters with numbers and special characters"
            )
            email = st.text_input("Email*")
            submitted = st.form_submit_button("Register")

            if submitted:
                if username and password and email:
                    success, error = register_user(username, password, email)
                    if success:
                        st.success("Registration successful! Please check your email for verification code.")
                        st.session_state.registration_complete = True
                        st.session_state.pending_verification_username = username
                    else:
                        st.error(f"Registration failed: {error}")
                else:
                    st.error("Please fill in all fields.")

    with tab3:
        with st.form("verification_form"):
            if st.session_state.registration_complete:
                st.info("Please enter the verification code sent to your email.")
                verification_username = st.text_input(
                    "Username",
                    value=st.session_state.pending_verification_username if st.session_state.pending_verification_username else "",
                    disabled=bool(st.session_state.pending_verification_username)
                )
                verification_code = st.text_input("Verification Code")
                
                col1, col2 = st.columns(2)
                with col1:
                    verify_submitted = st.form_submit_button("Verify Account")
                with col2:
                    resend_submitted = st.form_submit_button("Resend Code")

                if verify_submitted and verification_code:
                    success, error = verify_confirmation_code(verification_username, verification_code)
                    if success:
                        st.success("Account verified successfully! You can now login.")
                        st.session_state.registration_complete = False
                        st.session_state.pending_verification_username = None
                    else:
                        st.error(f"Verification failed: {error}")

                if resend_submitted:
                    success, error = resend_confirmation_code(verification_username)
                    if success:
                        st.success("Verification code resent! Please check your email.")
                    else:
                        st.error(f"Failed to resend code: {error}")
            else:
                st.info("Please register or login first.")

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Main app logic
if not st.session_state.authenticated:
    login_page()
else:
    st.write(f"Welcome, {st.session_state.username}!")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.experimental_rerun()
