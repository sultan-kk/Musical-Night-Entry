import streamlit as st
import pandas as pd
import time

# Page configuration
st.set_page_config(page_title="COMSATS Musical Night", page_icon="🎸", layout="centered")

# Initialize session state for the dataframe
if 'df' not in st.session_state:
    st.session_state.df = None

# Audio Player Function (Autoplay Sound Effects)
def play_sound(status):
    if status == "success":
        # Crowd Cheering Sound
        sound_url = "https://upload.wikimedia.org/wikipedia/commons/3/34/Sound_Effect_-_Crowd_Cheering.ogg"
        audio_type = "audio/ogg"
    else:
        # Error Buzzer Sound
        sound_url = "https://upload.wikimedia.org/wikipedia/commons/d/d4/Buzzer.ogg"
        audio_type = "audio/ogg"
        
    audio_html = f"""
        <audio autoplay style="display:none;">
            <source src="{sound_url}" type="{audio_type}">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# Advanced UI with Background Image & Custom CSS
st.markdown("""
    <style>
    /* Concert Background Image with Dark Overlay */
    .stApp {
        background: linear-gradient(rgba(10, 5, 25, 0.85), rgba(15, 5, 30, 0.95)), 
                    url('https://images.unsplash.com/photo-1470229722913-7c092b2472d5?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #ffffff;
    }

    /* Concert Aesthetic Header overlay */
    .hero-container {
        text-align: center;
        padding: 30px 10px;
        background: linear-gradient(180deg, rgba(236, 72, 153, 0.2) 0%, rgba(0,0,0,0) 100%);
        border-radius: 20px;
        margin-bottom: 25px;
        border-bottom: 1px solid rgba(236, 72, 153, 0.4);
        backdrop-filter: blur(5px);
    }

    .festival-title {
        font-family: 'Montserrat', 'Impact', sans-serif;
        font-size: 45px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 3px;
        background: linear-gradient(45deg, #ff007f, #7f00ff, #00f0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(127, 0, 255, 0.8);
        margin: 5px 0;
    }

    .festival-sub {
        font-size: 16px;
        letter-spacing: 5px;
        color: #00f0ff;
        text-shadow: 0 0 15px rgba(0, 240, 255, 0.8);
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    /* Beautiful Glass Cards */
    .glass-panel {
        background: rgba(10, 5, 25, 0.6);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 240, 255, 0.3);
        padding: 35px 25px;
        border-radius: 25px;
        box-shadow: 0 15px 40px 0 rgba(0, 0, 0, 0.8), inset 0 0 20px rgba(127, 0, 255, 0.2);
        text-align: center;
    }

    /* -------------------------------------------
       FUTURISTIC FILE UPLOADER CUSTOMIZATION 
       ------------------------------------------- */
    [data-testid="stFileUploadDropzone"] {
        background: rgba(0, 0, 0, 0.5) !important;
        border: 2px dashed #00f0ff !important;
        border-radius: 20px !important;
        padding: 40px !important;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    [data-testid="stFileUploadDropzone"]:hover {
        background: rgba(0, 240, 255, 0.1) !important;
        border: 2px solid #ff007f !important;
        box-shadow: 0 0 30px rgba(255, 0, 127, 0.5), inset 0 0 20px rgba(0, 240, 255, 0.2) !important;
    }

    [data-testid="stFileUploadDropzone"] > div > div > span,
    [data-testid="stFileUploadDropzone"] > div > div > small,
    [data-testid="stFileUploadDropzone"] > div > div > div > svg {
        display: none !important;
    }

    [data-testid="stFileUploadDropzone"] > div > div::before {
        content: "⚠️ SECURE UPLOAD: GUEST DATABASE (.XLSX) ⚠️";
        display: block;
        color: #00f0ff;
        font-size: 18px;
        font-weight: 800;
        letter-spacing: 2px;
        text-align: center;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.8);
        margin-bottom: 25px;
        animation: pulseText 2s infinite;
    }

    [data-testid="stFileUploadDropzone"] button {
        background: linear-gradient(90deg, #ff007f, #7f00ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 900 !important;
        letter-spacing: 1px !important;
        padding: 10px 30px !important;
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.6) !important;
        transition: transform 0.2s ease !important;
    }
    
    [data-testid="stFileUploadDropzone"] button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 25px rgba(127, 0, 255, 0.9) !important;
    }

    /* Advanced PIN-Pad Style Input Box */
    input[type="text"] {
        background-color: rgba(0, 0, 0, 0.7) !important;
        border: 2px solid #7f00ff !important;
        border-radius: 15px !important;
        color: #00f0ff !important;
        font-size: 40px !important;
        font-weight: 900 !important;
        text-align: center !important;
        letter-spacing: 20px !important;
        height: 85px !important;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.9);
        transition: all 0.3s ease;
    }
    input[type="text"]:focus {
        border-color: #00f0ff !important;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.6), inset 0 0 20px rgba(0, 240, 255, 0.3) !important;
        color: #ffffff !important;
    }
    input[type="text"]::placeholder {
        color: rgba(255, 255, 255, 0.15) !important;
        letter-spacing: 5px !important;
        font-size: 20px !important;
    }

    /* Neon Pulsing Button Customization */
    button[kind="primary"] {
        background: linear-gradient(45deg, #ff007f, #7f00ff) !important;
        border: none !important;
        color: white !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        letter-spacing: 3px !important;
        padding: 15px !important;
        border-radius: 15px !important;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.6) !important;
        animation: pulse 2s infinite !important;
        transition: transform 0.2s ease;
    }
    button[kind="primary"]:hover {
        transform: scale(1.02);
        box-shadow: 0 0 35px rgba(0, 240, 255, 0.9) !important;
    }

    /* Active Database Badge */
    .active-db-badge {
        display: inline-block;
        background: rgba(0, 255, 135, 0.2);
        border: 1px solid #00ff87;
        color: #00ff87;
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 14px;
        font-weight: bold;
        letter-spacing: 1px;
        margin-bottom: 20px;
        box-shadow: 0 0 20px rgba(0, 255, 135, 0.4);
    }

    /* Success / Reject Cards */
    .pass-glow-card {
        background: linear-gradient(135deg, rgba(20, 10, 45, 0.95), rgba(45, 10, 60, 0.95));
        border: 2px solid #00ff87;
        box-shadow: 0 0 40px rgba(0, 255, 135, 0.5), inset 0 0 20px rgba(0, 255, 135, 0.2);
        padding: 40px 25px;
        border-radius: 25px;
        text-align: center;
        animation: cardPop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-top: 20px;
    }
    .reject-glow-card {
        background: rgba(40, 5, 20, 0.95);
        border: 2px solid #ff0055;
        box-shadow: 0 0 35px rgba(255, 0, 85, 0.6);
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
    @keyframes pulseText {
        0% { opacity: 0.7; }
        50% { opacity: 1; text-shadow: 0 0 25px rgba(0, 240, 255, 1); }
        100% { opacity: 0.7; }
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

# 2. Logic: Show Custom Uploader OR Show Entry System
if st.session_state.df is None:
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=['xlsx', 'xls'])
    if uploaded_file is not None:
        try:
            with st.spinner("Encrypting and loading database..."):
                time.sleep(1) # Fake delay for tech feel
                st.session_state.df = pd.read_excel(uploaded_file)
                st.rerun() 
        except Exception as e:
            st.error(f"Error loading database: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # 3. Serial Number Entry System (Active Mode)
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    
    # Database Active Badge & Reset Button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<div class='active-db-badge'>🟢 GUEST DATABASE SECURE & ACTIVE</div>", unsafe_allow_html=True)
    with col2:
        if st.button("🔄 Reset"):
            st.session_state.df = None
            st.rerun()

    st.markdown("<h4 style='color:#e2e8f0; margin-bottom: 20px; font-weight:600; text-transform:uppercase;'>Enter Ticket Serial Code</h4>", unsafe_allow_html=True)
    
    # Giant PIN-pad style input
    sr_no = st.text_input("", max_chars=3, placeholder="___")
    
    st.write("") # Spacing
    verify_btn = st.button("⚡ AUTHENTICATE ENTRY ⚡", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if verify_btn:
        if sr_no.isdigit() and len(sr_no) == 3:
            with st.status("📡 Scanning secure database...", expanded=False) as status:
                time.sleep(1.2) # Immersive scanning effect
                is_registered = st.session_state.df.astype(str).isin([sr_no]).any().any()
                status.update(label="Scan complete!", state="complete", expanded=False)
                
            if is_registered:
                play_sound("success") # Play crowd cheer
                st.balloons()
                st.markdown("""
                    <div class="pass-glow-card">
                        <h2 style='color:#00ff87; margin-bottom:10px; font-size: 35px; text-shadow: 0 0 20px rgba(0,255,135,0.6);'>✅ ACCESS GRANTED</h2>
                        <div style='font-size: 24px; color: #ffffff; font-weight: 500; line-height:1.6;'>
                            Welcome to the <span style='color:#00f0ff; font-weight:bold;'>Musical Night</span> of<br>
                            COMSATS University Islamabad, Attock Campus! 🎶🕺
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                play_sound("error") # Play error buzzer
                st.markdown("""
                    <div class="reject-glow-card">
                        <h2 style='color:#ff0055; margin-bottom:5px; text-shadow: 0 0 20px rgba(255,0,85,0.6);'>🛑 ACCESS DENIED</h2><br>
                        <span style="font-size:18px; color:#ffb3c1;">Serial Code <b>{0}</b> is invalid or not in the guest list.</span>
                    </div>
                """.format(sr_no), unsafe_allow_html=True)
        else:
            st.warning("⚠️ Invalid Code Format. Enter exactly 3 digits.")
