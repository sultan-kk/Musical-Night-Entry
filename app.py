import streamlit as st
import pandas as pd
import time

# Page configuration
st.set_page_config(page_title="COMSATS Musical Night", page_icon="🎸", layout="centered")

# Advanced Premium UI (Glassmorphism & Dark Theme)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0f172a;
        background-image: radial-gradient(circle at 50% 0%, #1e293b 0%, #0f172a 70%);
        color: white;
    }
    
    /* Glassmorphism Card for Welcome Message */
    .welcome-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        animation: fadeIn 1s ease-in-out;
        margin-top: 20px;
    }
    
    .welcome-title {
        font-size: 32px;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #f59e0b, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .welcome-subtitle {
        font-size: 22px;
        font-weight: 400;
        color: #e2e8f0;
        line-height: 1.5;
    }
    
    /* Error Message Card */
    .error-card {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: #fca5a5;
        font-size: 18px;
        font-weight: 500;
        margin-top: 20px;
        animation: shake 0.5s;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes shake {
        0% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        50% { transform: translateX(10px); }
        75% { transform: translateX(-10px); }
        100% { transform: translateX(0); }
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("<h1 style='text-align: center; color: #f8fafc; font-weight: 800;'>🎸 Musical Night Portal</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px;'>Secure Entry Verification System</p>", unsafe_allow_html=True)
st.write("---")

# File Upload Section
uploaded_file = st.file_uploader("Upload Participant Excel File (.xlsx)", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        # Read Data
        df = pd.read_excel(uploaded_file)
        
        # Input Section
        st.markdown("<h3 style='color: #e2e8f0;'>Enter Details</h3>", unsafe_allow_html=True)
        sr_no = st.text_input("3-Digit Serial Number (e.g., 001, 145)", max_chars=3)
        
        # Button
        if st.button("Verify Registration", type="primary", use_container_width=True):
            if sr_no.isdigit() and len(sr_no) == 3:
                with st.spinner('Verifying database...'):
                    time.sleep(1) # Chota sa delay premium feel ke liye
                    
                    # Exact string matching in the entire dataframe
                    is_registered = df.astype(str).isin([sr_no]).any().any()
                    
                    if is_registered:
                        st.balloons()
                        st.markdown("""
                            <div class="welcome-card">
                                <div class="welcome-title">✨ Registration Verified!</div>
                                <div class="welcome-subtitle">Welcome to the Musical Night of COMSATS University Islamabad, Attock Campus 🎶</div>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                            <div class="error-card">
                                ❌ Not Registered. This serial number was not found in the official list.
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please enter a valid 3-digit numeric code.")
                
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("👆 Please upload the Excel file to begin verification.")
