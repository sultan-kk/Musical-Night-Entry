import streamlit as st
import pandas as pd
import time

# Page configuration
st.set_page_config(page_title="COMSATS Musical Night", page_icon="🎸", layout="centered")

# Initialize session state for the dataframe
if 'df' not in st.session_state:
    st.session_state.df = None

# Advanced & Futuristic Festival UI Style
st.markdown("""
    <style>
    /* Main Immersive Concert Background */
    .stApp {
        background: radial-gradient(circle at top, #180030 0%, #080015 100%);
        background-attachment: fixed;
        color: #ffffff;
    }

    /* Concert Aesthetic Header overlay */
    .hero-container {
        text-align: center;
        padding: 30px 10px;
        background: linear-gradient(180deg, rgba(236, 72, 153, 0.15) 0%, rgba(0,0,0,0) 100%);
        border-radius: 20px;
        margin-bottom: 25px;
        border-bottom: 1px solid rgba(236, 72, 153, 0.3);
    }

    /* Neon Festival Title */
    .festival-title {
        font-family: 'Montserrat', 'Impact', sans-serif;
        font-size: 45px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 3px;
        background: linear-gradient(45deg, #ff007f, #7f00ff, #00f0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(127, 0, 255, 0.6);
        margin: 5px 0;
    }

    .festival-sub {
        font-size: 16px;
        letter-spacing: 5px;
        color: #00f0ff;
        text-shadow: 0 0 15px rgba(0, 240, 255, 0.6);
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    /* Beautiful Glass Cards */
    .glass-panel {
        background: rgba(20, 10, 40, 0.5);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(127, 0, 255, 0.4);
        padding: 35px 25px;
        border-radius: 25px;
        box-shadow: 0 15px 40px 0 rgba(0, 0, 0, 0.6), inset 0 0 20px rgba(127, 0, 255, 0.1);
        text-align: center;
    }

    /* Customizing the Streamlit Uploader */
    [data-testid="stFileUploadDropzone"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 2px dashed #00f0ff !important;
        border-radius: 15px !important;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        background-color: rgba(0, 240, 255, 0.1) !important;
        border-color: #ff007f !important;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.3);
    }

    /* Advanced PIN-Pad Style Input Box */
    input[type="text"] {
        background-color: rgba(10, 5, 25, 0.8) !important;
        border: 2px solid #7f00ff !important;
        border-radius: 15px !important;
        color: #00f0ff !important;
        font-size: 35px !important;
        font-weight: 900 !important;
        text-align: center !important;
        letter-spacing: 15px !important;
        height: 80px !important;
        box-shadow: inset 0 0 15px rgba(0,0,0,0.8);
        transition: all 0.3s ease;
    }
    input[type="text"]:focus {
        border-color: #00f0ff !important;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.5), inset 0 0 15px rgba(0, 240, 255, 0.2) !important;
        color: #ffffff !important;
    }
    input[type="text"]::placeholder {
        color: rgba(255, 255, 255, 0.2) !important;
        letter-spacing: 5px !important;
        font-size: 20px !important;
    }

    /* Neon Pulsing Button Customization */
    button[kind="primary"] {
        background: linear-gradient(45deg, #ff007f, #7f00ff) !important;
        border: none !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        letter-spacing: 2px !important;
        padding: 15px !important;
        border-radius: 15px !important;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.5) !important;
        animation: pulse 2s infinite !important;
        transition: transform 0.2s ease;
    }
    button[kind="primary"]:hover {
        transform: scale(1.02);
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.8) !important;
    }

    /* Active Database Badge */
    .active-db-badge {
        display: inline-block;
        background: rgba(0, 255, 135, 0.15);
        border: 1px solid #00ff87;
        color: #00ff87;
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 14px;
        font-weight: bold;
        letter-spacing: 1px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 255, 135, 0.3);
    }

    /* Success / Reject Cards */
    .pass-glow-card {
        background: linear-gradient(135deg, rgba(20, 10, 45, 0.95), rgba(45, 10, 60, 0.95));
        border: 2px solid #00f0ff;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.5), inset 0 0 20px rgba(127, 0, 255, 0.3);
        padding: 40px 25px;
        border-radius: 25px;
        text-align: center;
        animation: cardPop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-top: 20px;
    }
    .reject-glow-card {
        background: rgba(40, 5, 20, 0.95);
        border: 2px solid #ff0055;
        box-shadow: 0 0 25px rgba(255, 0, 85, 0.4);
        padding: 30px 20px;
        border-radius: 25px;
        text-align: center;
        color: #ffccd5;
        font-size: 18px;
        font-weight: 600;
        margin-top: 20px;
        animation: shake 0.4s ease-in-out;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 15px rgba(255, 0, 127, 0.4); }
        50% { box-shadow: 0 0 35px rgba(127, 0, 255, 0.8); }
        100% { box-shadow: 0 0 15px rgba(255, 0, 127, 0.4); }
    }
    @keyframes cardPop {
        0% { transform: scale(0.8) translateY(20px); opacity: 0; }
        100% { transform: scale(1) translateY(0); opacity: 1; }
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    </style>
""", unsafe_allow_html=True)

# 1. Header Section
st.markdown("""
    <div class="hero-container">
        <div class="festival-sub">🎵 VIP GATEWAY 🎵</div>
        <div class="festival-title">COMSATS Musical Night</div>
    </div>
""", unsafe_allow_html=True)

# 2. Logic: Show Uploader OR Show Entry System
if st.session_state.df is None:
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#00f0ff; font-weight:800;'>INITIATE SYSTEM</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;'>Upload the official guest list (.xlsx) to activate the security gate.</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=['xlsx', 'xls'])
    if uploaded_file is not None:
        try:
            with st.spinner("Encrypting and loading database..."):
                time.sleep(1) # Fake delay for tech feel
                st.session_state.df = pd.read_excel(uploaded_file)
                st.rerun() # Instantly hide uploader and show the pin pad
        except Exception as e:
            st.error(f"Error loading database: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # 3. Serial Number Entry System (Active Mode)
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    
    # Database Active Badge & Reset Button in columns
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<div class='active-db-badge'>🟢 GUEST DATABASE SECURE & ACTIVE</div>", unsafe_allow_html=True)
    with col2:
        if st.button("🔄 Reset"):
            st.session_state.df = None
            st.rerun()

    st.markdown("<h4 style='color:#e2e8f0; margin-bottom: 20px; font-weight:600;'>ENTER TICKET SERIAL CODE</h4>", unsafe_allow_html=True)
    
    # Giant PIN-pad style input
    sr_no = st.text_input("", max_chars=3, placeholder="___", help="Type the 3-digit number written on the ticket.")
    
    st.write("") # Spacing
    verify_btn = st.button("⚡ AUTHENTICATE ENTRY ⚡", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if verify_btn:
        if sr_no.isdigit() and len(sr_no) == 3:
            with st.status("📡 Scanning secure database...", expanded=False) as status:
                time.sleep(1) # Immersive scanning effect
                is_registered = st.session_state.df.astype(str).isin([sr_no]).any().any()
                status.update(label="Scan complete!", state="complete", expanded=False)
                
            if is_registered:
                st.balloons()
                st.markdown("""
                    <div class="pass-glow-card">
                        <h2 style='color:#00ff87; margin-bottom:5px;'>✅ ACCESS GRANTED</h2>
                        <div style='font-size: 22px; color: #ffffff; font-weight: 500; line-height:1.6;'>
                            Welcome to the <span style='color:#00f0ff; font-weight:bold;'>Musical Night</span> of<br>
                            COMSATS University Islamabad, Attock Campus! 🎶🕺
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="reject-glow-card">
                        🛑 ACCESS DENIED<br><br>
                        <span style="font-size:15px; color:#ffb3c1;">Serial Code <b>{0}</b> is invalid or not in the guest list.</span>
                    </div>
                """.format(sr_no), unsafe_allow_html=True)
        else:
            st.warning("⚠️ Invalid Code Format. Enter exactly 3 digits.")
