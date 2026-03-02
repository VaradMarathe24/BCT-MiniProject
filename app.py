import streamlit as st
import json
from blockchain import Blockchain
from team_rules import validate_team

# --- MUST be first command ---
st.set_page_config(
    page_title="Fantasy Cricket Blockchain",
    page_icon="🏏",
    layout="wide"
)

# --- Custom CSS for PURE WHITE background + modern UI ---
st.markdown("""
    <style>
    /* Pure white background everywhere */
    .stApp {
        background-color: white !important;
    }
    [data-testid="stSidebar"] {
        background-color: white !important;
    }

    /* Ensure all text is dark for readability */
    .stMarkdown, .stText, p, div, span, h1, h2, h3, h4, h5, h6, label {
        color: #000000 !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] .st-success, [data-testid="stSidebar"] .stButton button {
        color: #1f77b4 !important;
    }

    /* Button enhancements */
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        width: 100%;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0d5ca1;
        color: white;
    }

    /* Player card styling */
    .player-card {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 12px;
        margin: 8px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .player-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* Credits bar */
    .credits-bar {
        height: 20px;
        background: #e9ecef;
        border-radius: 10px;
        margin: 10px 0;
        overflow: hidden;
    }
    .credits-fill {
        height: 100%;
        background: linear-gradient(to right, #28a745, #ffc107, #dc3545);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 8px;
        color: white;
        font-size: 0.8rem;
        font-weight: bold;
    }

    /* Section dividers */
    .section-divider {
        margin: 1.5rem 0;
        border: none;
        border-top: 1px solid #eee;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load Data ---
with open("players.json") as f:
    players = json.load(f)

blockchain = Blockchain()

# --- Demo Credentials ---
USER_CREDENTIALS = {
    "admin": "admin123",
    "user1": "pass1",
    "user2": "pass2"
}

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

def login(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None

# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#1f77b4;'>🏏 Fantasy Cricket Blockchain</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:gray;'>Secure • Immutable • Fair</p>", unsafe_allow_html=True)
        st.divider()

        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔑 Password", type="password", placeholder="••••••••")

        if st.button("🔓 Login", use_container_width=True, type="primary"):
            if login(username, password):
                st.success(f"✅ Welcome, **{username}**!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Try `user1` / `pass1`.")

        st.info("💡 Demo accounts: `user1`/`pass1`, `admin`/`admin123`")

# --- MAIN APP ---
else:
    # Sidebar
    with st.sidebar:
        st.image("https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/325/cricket-game_1f3cf.png", width=50)
        st.title("🏏 Fantasy Cricket")
        st.markdown(f"**User:** `{st.session_state.username}`")
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
        st.caption("🔒 All submissions are immutable")

    # Main Title
    st.markdown("<h1 style='color:#1f77b4;'>🏏 Build & Validate Your Dream Team</h1>", unsafe_allow_html=True)
    st.markdown("> ✨ Create a valid 11-player team within 100 credits. Once submitted, it’s recorded forever on the blockchain.")

    tab1, tab2 = st.tabs(["🎯 Create Team", "🔗 Blockchain Ledger"])

    # --- TAB 1: Create Team ---
    with tab1:
        st.subheader("🧑‍🤝‍🧑 Select Your Players")
        selected_names = st.multiselect(
            "Search or select up to 11 players:",
            options=[p["name"] for p in players],
            max_selections=11
        )

        selected_players = [p for p in players if p["name"] in selected_names]
        total_credits = sum(p["credit"] for p in selected_players)
        credit_pct = min(total_credits, 100)  # cap at 100 for visual

        # --- Credits Meter ---
        st.markdown("### 💰 Budget: 100 Credits")
        st.markdown(f"<div class='credits-bar'><div class='credits-fill' style='width:{min(credit_pct, 100)}%'>{total_credits}/100</div></div>", unsafe_allow_html=True)

        if total_credits > 100:
            st.warning("⚠️ You’ve exceeded the 100-credit limit!")

        # --- Selected Team Preview ---
        if selected_players:
            st.markdown("### 📋 Your Team Preview")
            cols = st.columns(3)
            for idx, player in enumerate(selected_players):
                with cols[idx % 3]:
                    role_icon = {"Batsman": "🏏", "Bowler": "⚾", "All-rounder": "🛡️", "Wicketkeeper": "🧤"}.get(player.get("role", ""), "👤")
                    st.markdown(f"""
                    <div class="player-card">
                        <b>{player['name']}</b><br>
                        {role_icon} {player.get('role', 'Player')}<br>
                        🌍 {player['team']}<br>
                        💰 {player['credit']} credits
                    </div>
                    """, unsafe_allow_html=True)

        # --- Submit Button ---
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        if st.button("🚀 Submit Team to Blockchain", use_container_width=True, disabled=len(selected_players) != 11 or total_credits > 100):
            team = selected_players
            valid, msg = validate_team(team)

            if not valid:
                st.error(f"❌ Team validation failed: {msg}")
            elif total_credits > 100:
                st.error("❌ Total credits exceed 100!")
            else:
                data = {
                    "team": selected_names,
                    "user": st.session_state.username,
                    "credits_used": total_credits
                }
                last_block = blockchain.get_last_block()
                block = blockchain.create_block(data, last_block["hash"])
                st.success("✅ Team successfully recorded on the blockchain!")
                with st.expander("📄 View Block Details"):
                    st.json(block)

    # --- TAB 2: Blockchain Ledger ---
    with tab2:
        st.subheader("📜 Immutable Transaction Ledger")
        try:
            with open("blockchain_data.json") as f:
                chain = json.load(f)
            if chain:
                st.json(chain)
            else:
                st.info("📭 No teams submitted yet.")
        except FileNotFoundError:
            st.info("📭 Blockchain ledger is empty.")

        st.divider()
        if st.button("🔍 Verify Blockchain Integrity", use_container_width=True):
            with st.spinner("Verifying cryptographic hashes..."):
                is_valid = blockchain.verify_chain()
                if is_valid:
                    st.success("✅ Blockchain is valid — no tampering detected!")
                else:
                    st.error("⚠️ ⚠️ Integrity check failed! The ledger may have been altered.")