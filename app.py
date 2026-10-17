import streamlit as st
import pandas as pd
import time

# Page configuration for immersive dark mode
st.set_page_config(page_title="COMSATS Musical Night", page_icon="🎸", layout="centered")

# Vibrant & Immersive Musical Night UI Style
st.markdown("""
    <style>
    /* Main Immersive Concert Background */
    .stApp {
        background: radial-gradient(circle at top, #180030 0%, #080015 80%);
        background-attachment: fixed;
        color: #ffffff;
    }

    /* Concert Aesthetic Header overlay */
    .hero-container {
        text-align: center;
        padding: 30px 10px;
        background: linear-gradient(180deg, rgba(236, 72, 153, 0.1) 0%, rgba(0,0,0,0) 100%);
        border-radius: 20px;
        margin-bottom: 25px;
        border-bottom: 1px solid rgba(236, 72, 153, 0.2);
    }

    /* Neon Festival Title */
    .festival-title {
        font-family: 'Montserrat', 'Impact', sans-serif;
        font-size: 42px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        background: linear-gradient(45deg, #ff007f, #7f00ff, #00f0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(127, 0, 255, 0.5);
        margin: 5px 0;
    }

    /* Subtitle with a pulsing live/night look */
    .festival-sub {
        font-size: 16px;
        letter-spacing: 4px;
        color: #00f0ff;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .campus-badge {
        font-size: 13px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 4px 15px;
        border-radius: 50px;
        color: #e2e8f0;
        display: inline-block;
    }

    /* Beautiful Glass Cards */
    .glass-panel {
        background: rgba(20, 10, 40, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(127, 0, 255, 0.25);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
    }

    /* Input & Button Customizations */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(127, 0, 255, 0.3) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    div[data-baseweb="input"]:focus-within {
        border-color: #ff007f !important;
        box-shadow: 0 0 10px rgba(255, 0, 127, 0.4) !important;
    }

    /* Verification Success Neon Card */
    .pass-glow-card {
        background: linear-gradient(135deg, rgba(20, 10, 45, 0.9) 0%, rgba(45, 10, 60, 0.9) 100%);
        border: 2px solid #00f0ff;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.4), inset 0 0 15px rgba(127, 0, 255, 0.2);
        padding: 40px 25px;
        border-radius: 22px;
        text-align: center;
        animation: cardPop 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-top: 25px;
    }

    .pass-title {
        font-size: 30px;
        font-weight: 850;
        background: linear-gradient(to right, #00f0ff, #00ff87);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
        margin-bottom: 15px;
        text-shadow: 0 0 15px rgba(0,240,255,0.2);
    }

    .pass-message {
        font-size: 22px;
        line-height: 1.5;
        font-weight: 600;
        color: #ffffff;
    }

    .neon-accent {
        color: #ff007f;
        font-weight: bold;
    }

    /* Reject Red Glow Card */
    .reject-glow-card {
        background: rgba(40, 5, 20, 0.85);
        border: 2px solid #ff0055;
        box-shadow: 0 0 20px rgba(255, 0, 85, 0.3);
        padding: 30px 20px;
        border-radius: 20px;
        text-align: center;
        color: #ffccd5;
        font-size: 18px;
        font-weight: 600;
        margin-top: 25px;
        animation: shake 0.4s ease-in-out;
    }

    /* Dynamic Visualizer Decoration */
    .visualizer {
        display: flex;
        justify-content: center;
        gap: 4px;
        margin: 20px 0 10px 0;
    }
    .bar {
        width: 4px;
        height: 15px;
        background: #ff007f;
        border-radius: 2px;
        animation: bounce 0.8s ease-in-out infinite alternate;
    }
    .bar:nth-child(2) { background: #7f00ff; animation-delay: 0.2s; height: 25px; }
    .bar:nth-child(3) { background: #00f0ff; animation-delay: 0.4s; height: 35px; }
    .bar:nth-child(4) { background: #00ff87; animation-delay: 0.1s; height: 20px; }
    .bar:nth-child(5) { background: #ff007f; animation-delay: 0.5s; height: 30px; }

    /* Animations */
    @keyframes cardPop {
        0% { transform: scale(0.8); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    @keyframes bounce {
        100% { height: 5px; }
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-8px); }
        75% { transform: translateX(8px); }
    }
    </style>
""", unsafe_allow_html=True)

# 1. Festival Title Area
st.markdown("""
    <div class="hero-container">
        <div class="festival-sub">🎵 LIVE EVENT ACCESS 🎵</div>
        <div class="festival-title">COMSATS Musical Night</div>
        <div class="campus-badge">Islamabad, Attock Campus</div>
    </div>
""", unsafe_allow_html=True)

# Visualizer effect
st.markdown("""
    <div class="visualizer">
        <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div>
    </div>
""", unsafe_allow_html=True)

# 2. Upload Screen
st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("📥 Drop Guest / Participant List here (.xlsx)", type=['xlsx', 'xls'])
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        
        # 3. Serial Number verification panel
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#00f0ff; margin-bottom:5px; font-weight:700;'>🔑 ACCESS CHECK</h4>", unsafe_allow_html=True)
        sr_no = st.text_input("Enter 3-Digit Serial Number:", max_chars=3, placeholder="e.g., 007")
        
        # Custom button style via Streamlit
        verify_btn = st.button("🌟 VERIFY & ENTER 🌟", type="primary", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if verify_btn:
            if sr_no.isdigit() and len(sr_no) == 3:
                with st.status("🔍 Checking guest list database...", expanded=False) as status:
                    time.sleep(0.8)  # Immersive delay
                    is_registered = df.astype(str).isin([sr_no]).any().any()
                    status.update(label="Scanning complete!", state="complete", expanded=False)
                    
                if is_registered:
                    st.balloons()
                    st.markdown("""
                        <div class="pass-glow-card">
                            <div class="pass-title">🎟️ ACCESS GRANTED</div>
                            <div class="pass-message">
                                Welcome to the <span class="neon-accent">Musical Night</span> of<br>
                                COMSATS University Islamabad, Attock Campus! 🎶🕺🎸
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class="reject-glow-card">
                            🛑 ACCESS DENIED<br>
                            <span style="font-size:14px; opacity:0.8;">Serial number <b>{0}</b> was not found on the registered guest list.</span>
                        </div>
                    """.format(sr_no), unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please input exactly a 3-digit Serial Number (e.g., 001, 142).")
                
    except Exception as e:
        st.error(f"Failed to read data file: {e}")
else:
    st.markdown("""
        <div style='text-align: center; color: #94a3b8; font-size: 15px; margin-top:20px;'>
            Please upload the attendance / participant list to activate gate verification.
        </div>
    """, unsafe_allow_html=True)
