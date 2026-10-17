import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time

# Page configuration
st.set_page_config(page_title="COMSATS Musical Night", page_icon="🎸", layout="centered")

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'sr_input' not in st.session_state:
    st.session_state.sr_input = ""
if 'last_submitted' not in st.session_state:
    st.session_state.last_submitted = None

# Callback: Fires automatically when user presses ENTER in the input box
def submit_serial():
    val = st.session_state.sr_input.strip()
    if val:
        st.session_state.last_submitted = val
        st.session_state.sr_input = ""  # Immediately clear input box

# Auto-Focus Cursor + Short Fireworks/Clapping & Error Sound Generator
def trigger_sound_and_focus(status=None):
    timestamp = time.time()
    js_code = f"""
    <!-- trigger: {timestamp} -->
    <script>
    (function() {{
        // 1. Keep cursor focused inside the 3-digit input box
        const focusInput = () => {{
            try {{
                const inputs = window.parent.document.querySelectorAll('input[type="text"]');
                if (inputs.length > 0) {{
                    const target = inputs[inputs.length - 1];
                    target.focus();
                }}
            }} catch (e) {{ console.log(e); }}
        }};
        setTimeout(focusInput, 100);
        setTimeout(focusInput, 400);
        setTimeout(focusInput, 800);

        // 2. Play Short Sound Effects (~1.8s max)
        const status = "{status}";
        if (status === "success") {{
            try {{
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                const ctx = new AudioCtx();

                // Fireworks Launch Whistle (0.0s -> 0.35s)
                const whistle = ctx.createOscillator();
                const wGain = ctx.createGain();
                whistle.type = 'sine';
                whistle.frequency.setValueAtTime(350, ctx.currentTime);
                whistle.frequency.exponentialRampToValueAtTime(1400, ctx.currentTime + 0.35);
                wGain.gain.setValueAtTime(0.2, ctx.currentTime);
                wGain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.35);
                whistle.connect(wGain);
                wGain.connect(ctx.destination);
                whistle.start(ctx.currentTime);
                whistle.stop(ctx.currentTime + 0.35);

                // Fireworks Explosion & Clapping Bursts (0.35s -> 1.7s)
                const burstTimes = [0.36, 0.55, 0.75, 0.95, 1.15, 1.35];
                burstTimes.forEach((delay, i) => {{
                    const bufferSize = ctx.sampleRate * 0.22;
                    const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
                    const data = buffer.getChannelData(0);
                    for (let j = 0; j < bufferSize; j++) {{
                        data[j] = (Math.random() * 2 - 1) * Math.exp(-j / (ctx.sampleRate * 0.06));
                    }}
                    const noise = ctx.createBufferSource();
                    noise.buffer = buffer;

                    const filter = ctx.createBiquadFilter();
                    filter.type = i === 0 ? 'lowpass' : 'bandpass';
                    filter.frequency.value = i === 0 ? 600 : 1200 + (i * 150);

                    const nGain = ctx.createGain();
                    nGain.gain.setValueAtTime(i === 0 ? 0.7 : 0.45, ctx.currentTime + delay);
                    nGain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + delay + 0.22);

                    noise.connect(filter);
                    filter.connect(nGain);
                    nGain.connect(ctx.destination);
                    noise.start(ctx.currentTime + delay);
                }});

                // Sparkle Chime Chord
                [523.25, 659.25, 783.99, 1046.5].forEach((freq, idx) => {{
                    const osc = ctx.createOscillator();
                    const g = ctx.createGain();
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(freq, ctx.currentTime + 0.36 + idx * 0.08);
                    g.gain.setValueAtTime(0.25, ctx.currentTime + 0.36 + idx * 0.08);
                    g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 1.2);
                    osc.connect(g);
                    g.connect(ctx.destination);
                    osc.start(ctx.currentTime + 0.36 + idx * 0.08);
                    osc.stop(ctx.currentTime + 1.2);
                }});

                // Stop AudioContext strictly at 1.8 seconds
                setTimeout(() => {{ ctx.close(); }}, 1800);
            }} catch(e) {{ console.error(e); }}
        }} else if (status === "error") {{
            try {{
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                const ctx = new AudioCtx();
                [0, 0.22].forEach((delay) => {{
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(140, ctx.currentTime + delay);
                    osc.frequency.setValueAtTime(95, ctx.currentTime + delay + 0.08);
                    gain.gain.setValueAtTime(0.4, ctx.currentTime + delay);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + delay + 0.18);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(ctx.currentTime + delay);
                    osc.stop(ctx.currentTime + delay + 0.18);
                }});
                setTimeout(() => {{ ctx.close(); }}, 600);
            }} catch(e) {{ console.error(e); }}
        }}
    }})();
    </script>
    """
    components.html(js_code, height=1)

# Bright & Visible Concert Stage Background + Clean Sharp Typography
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&display=swap');

    /* Bright Live Concert Crowd & Stage Lasers Background */
    .stApp, [data-testid="stAppViewContainer"] {
        background: 
            radial-gradient(circle at 20% 15%, rgba(255, 0, 127, 0.35) 0%, rgba(0, 0, 0, 0) 40%),
            radial-gradient(circle at 80% 15%, rgba(0, 240, 255, 0.35) 0%, rgba(0, 0, 0, 0) 40%),
            linear-gradient(180deg, rgba(12, 4, 28, 0.50) 0%, rgba(10, 3, 24, 0.72) 100%),
            url('https://images.unsplash.com/photo-1514525253161-7a46d19cd819?q=80&w=1920&auto=format&fit=crop') !important;
        background-size: cover !important;
        background-position: center center !important;
        background-attachment: fixed !important;
        color: #ffffff !important;
        font-family: 'Poppins', sans-serif !important;
    }

    [data-testid="stHeader"] {
        background: rgba(10, 3, 24, 0.4) !important;
    }

    /* Concert Header Banner */
    .hero-container {
        text-align: center;
        padding: 30px 24px;
        background: rgba(12, 4, 28, 0.88);
        border: 2px solid #ff007f;
        border-radius: 22px;
        margin-bottom: 20px;
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.8), 0 0 25px rgba(255, 0, 127, 0.35);
        backdrop-filter: blur(12px);
    }

    .festival-sub {
        font-family: 'Poppins', sans-serif;
        font-size: 14px;
        letter-spacing: 5px;
        color: #00f0ff;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    /* Crisp, High-Contrast Title */
    .festival-title {
        font-family: 'Poppins', 'Segoe UI', sans-serif;
        font-size: 38px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 3px;
        word-spacing: 6px;
        color: #ffffff;
        text-shadow: 0 3px 8px rgba(0, 0, 0, 0.95), 0 0 14px rgba(0, 240, 255, 0.55);
        margin: 8px 0 12px 0;
        line-height: 1.25;
    }

    .title-highlight {
        color: #ff2a9d;
        text-shadow: 0 3px 8px rgba(0, 0, 0, 0.95), 0 0 16px rgba(255, 42, 157, 0.65);
    }

    .campus-tag {
        display: inline-block;
        margin-top: 6px;
        padding: 6px 20px;
        background: rgba(0, 240, 255, 0.15);
        border: 1px solid #00f0ff;
        border-radius: 30px;
        color: #ffffff;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
    }

    /* Style Streamlit Native Bordered Container as VIP Glass Panel */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(14, 5, 32, 0.85) !important;
        backdrop-filter: blur(14px) !important;
        border: 2px solid #00f0ff !important;
        border-radius: 24px !important;
        padding: 25px !important;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.85), 0 0 25px rgba(0, 240, 255, 0.35) !important;
    }

    /* Futuristic File Uploader Styling */
    [data-testid="stFileUploadDropzone"] {
        background: rgba(25, 8, 55, 0.85) !important;
        border: 2px dashed #ff007f !important;
        border-radius: 18px !important;
        padding: 30px !important;
        box-shadow: inset 0 0 20px rgba(255, 0, 127, 0.25) !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stFileUploadDropzone"]:hover {
        border: 2px solid #00f0ff !important;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.6) !important;
    }

    [data-testid="stFileUploadDropzone"] button {
        background: linear-gradient(90deg, #ff007f, #7f00ff) !important;
        color: #ffffff !important;
        border: 1px solid #00f0ff !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        padding: 8px 24px !important;
    }

    /* VIP PIN-Pad Input Box */
    input[type="text"] {
        background-color: rgba(5, 2, 15, 0.9) !important;
        border: 2px solid #ff007f !important;
        border-radius: 16px !important;
        color: #00f0ff !important;
        font-size: 42px !important;
        font-weight: 900 !important;
        text-align: center !important;
        letter-spacing: 18px !important;
        height: 85px !important;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.4) !important;
    }

    input[type="text"]:focus {
        border-color: #00f0ff !important;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.8) !important;
        color: #ffffff !important;
    }

    /* Neon Pulsing Button */
    button[kind="primary"] {
        background: linear-gradient(45deg, #ff007f, #7f00ff, #00f0ff) !important;
        border: none !important;
        color: #ffffff !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        letter-spacing: 2.5px !important;
        padding: 16px !important;
        border-radius: 15px !important;
        box-shadow: 0 0 25px rgba(255, 0, 127, 0.7) !important;
    }

    /* Active Database Badge */
    .active-db-badge {
        display: inline-block;
        background: rgba(0, 255, 135, 0.2);
        border: 1px solid #00ff87;
        color: #00ff87;
        padding: 8px 18px;
        border-radius: 50px;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1px;
        box-shadow: 0 0 15px rgba(0, 255, 135, 0.4);
    }

    /* Granted & Denied Cards */
    .pass-glow-card {
        background: rgba(10, 35, 30, 0.92);
        border: 2px solid #00ff87;
        box-shadow: 0 0 40px rgba(0, 255, 135, 0.6);
        padding: 35px 25px;
        border-radius: 22px;
        text-align: center;
        margin-top: 20px;
    }

    .reject-glow-card {
        background: rgba(45, 5, 20, 0.92);
        border: 2px solid #ff0055;
        box-shadow: 0 0 40px rgba(255, 0, 85, 0.6);
        padding: 30px 20px;
        border-radius: 22px;
        text-align: center;
        color: #ffe0e6;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 1. Concert Hero Banner
st.markdown("""
    <div class="hero-container">
        <div class="festival-sub">🎵 LIVE CONCERT GATEWAY 🎵</div>
        <div class="festival-title">🎸 COMSATS <span class="title-highlight">MUSICAL NIGHT</span></div>
        <div class="campus-tag">ISLAMABAD • ATTOCK CAMPUS</div>
    </div>
""", unsafe_allow_html=True)

# 2. Main Gate Container
with st.container(border=True):
    if st.session_state.df is None:
        st.markdown("<h3 style='text-align:center; color:#00f0ff; margin-bottom:5px; font-weight:700;'>📂 UPLOAD GUEST LIST DATABASE</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#cbd5e1; font-size:14px;'>Select the official Excel sheet (.xlsx) to unlock the VIP verification terminal</p>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Upload Participant Excel File", type=['xlsx', 'xls'], label_visibility="collapsed")
        if uploaded_file is not None:
            try:
                with st.spinner("Loading concert guest database..."):
                    time.sleep(0.6)
                    st.session_state.df = pd.read_excel(uploaded_file)
                    st.rerun()
            except Exception as e:
                st.error(f"Error loading file: {e}")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("<div class='active-db-badge'>🟢 GUEST DATABASE ACTIVE</div>", unsafe_allow_html=True)
        with col2:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.df = None
                st.session_state.last_submitted = None
                st.rerun()

        st.markdown("<h3 style='text-align:center; color:#ffffff; margin-top:15px; font-weight:700;'>🎟️ ENTER 3-DIGIT SERIAL NO</h3>", unsafe_allow_html=True)
        
        # Pressing Enter triggers submit_serial() and clears the box automatically
        st.text_input(
            "Serial Code",
            max_chars=3,
            placeholder="001",
            label_visibility="collapsed",
            key="sr_input",
            on_change=submit_serial
        )
        st.write("")
        if st.button("⚡ AUTHENTICATE ENTRY ⚡", type="primary", use_container_width=True):
            submit_serial()

        # Process the submitted serial number
        if st.session_state.last_submitted is not None:
            sr_no = st.session_state.last_submitted
            st.session_state.last_submitted = None  # Reset after reading

            if sr_no.isdigit() and len(sr_no) == 3:
                with st.status(f"📡 Scanning Serial No: {sr_no}...", expanded=False) as status:
                    time.sleep(0.4)
                    clean_df = st.session_state.df.astype(str).apply(lambda x: x.str.strip().str.zfill(3))
                    raw_df = st.session_state.df.astype(str).apply(lambda x: x.str.strip())
                    is_registered = clean_df.isin([sr_no]).any().any() or raw_df.isin([sr_no, str(int(sr_no))]).any().any()
                    status.update(label=f"Scan complete for #{sr_no}!", state="complete", expanded=False)

                if is_registered:
                    trigger_sound_and_focus("success")
                    st.balloons()
                    st.markdown(f"""
                        <div class="pass-glow-card">
                            <h2 style='color:#00ff87; margin-bottom:10px; font-size:34px; font-weight:800;'>✅ REGISTERED! (#{sr_no})</h2>
                            <div style='font-size:23px; color:#ffffff; font-weight:600; line-height:1.5;'>
                                Welcome to the <span style='color:#00f0ff;'>Musical Night</span> of<br>
                                COMSATS University Islamabad, Attock Campus 🎶🕺🎸
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    trigger_sound_and_focus("error")
                    st.markdown(f"""
                        <div class="reject-glow-card">
                            <h2 style='color:#ff0055; margin-bottom:8px; font-size:30px; font-weight:800;'>🛑 ACCESS DENIED</h2>
                            <div style='font-size:18px;'>Serial Number <b>{sr_no}</b> is not registered in the guest list.</div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                trigger_sound_and_focus("error")
                st.warning("⚠️ Please enter a valid 3-digit number (e.g., 001, 100).")
        else:
            # Keep cursor focused on initial load
            trigger_sound_and_focus(None)
