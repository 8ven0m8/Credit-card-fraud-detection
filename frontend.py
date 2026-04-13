import streamlit as st
import requests
import json
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Credit Card Fraud Detection",
    page_icon="🛡️",
    layout="wide",
)

# ── Constants ──────────────────────────────────────────────────────────────────
API_URL = "https://credit-card-fraud-detection-2ia2.onrender.com/predict"
MAX_HISTORY = 10

SAMPLE_DATA = {
    "Time": 4462,
    "V1": -2.30334956758553,
    "V2": 1.759247460267,
    "V3": -0.359744743330052,
    "V4": 2.33024305053917,
    "V5": -0.821628328375422,
    "V6": -0.0757875706194599,
    "V7": 0.562319782266954,
    "V8": -0.399146578487216,
    "V9": -0.238253367661746,
    "V10": -1.52541162656194,
    "V11": 2.03291215755072,
    "V12": -6.56012429505962,
    "V13": 0.0229373234890961,
    "V14": -1.47010153611197,
    "V15": -0.698826068579047,
    "V16": -2.28219382856251,
    "V17": -4.78183085597533,
    "V18": -2.61566494476124,
    "V19": -1.33444106667307,
    "V20": -0.430021867171611,
    "V21": -0.294166317554753,
    "V22": -0.932391057274991,
    "V23": 0.172726295799422,
    "V24": -0.0873295379700724,
    "V25": -0.156114264651172,
    "V26": -0.542627889040196,
    "V27": 0.0395659889264757,
    "V28": -0.153028796529788,
    "Amount": 239.93,
}

# ── Session state init ─────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "json_input" not in st.session_state:
    st.session_state.json_input = json.dumps(SAMPLE_DATA, indent=2)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        /* ── Global ── */
        [data-testid="stAppViewContainer"] {
            background: #0d1117;
        }
        [data-testid="stSidebar"] {
            background: #161b22;
            border-right: 1px solid #30363d;
        }

        /* ── Header banner ── */
        .header-banner {
            background: linear-gradient(135deg, #1a1f2e 0%, #16213e 50%, #0f3460 100%);
            border: 1px solid #30363d;
            border-radius: 16px;
            padding: 2rem 2.5rem;
            margin-bottom: 1.8rem;
            display: flex;
            align-items: center;
            gap: 1.2rem;
        }
        .header-icon { font-size: 3rem; line-height: 1; }
        .header-title {
            font-size: 2rem;
            font-weight: 700;
            color: #e6edf3;
            margin: 0;
            letter-spacing: -0.5px;
        }
        .header-sub {
            font-size: 0.9rem;
            color: #8b949e;
            margin: 0.3rem 0 0;
        }

        /* ── Section cards ── */
        .section-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.2rem;
        }
        .section-label {
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            color: #8b949e;
            margin-bottom: 0.8rem;
        }

        /* ── Result boxes ── */
        .result-fraud {
            background: linear-gradient(135deg, #2d1b1b, #3d1a1a);
            border: 2px solid #f85149;
            border-radius: 12px;
            padding: 1.5rem 2rem;
            text-align: center;
        }
        .result-safe {
            background: linear-gradient(135deg, #1b2d1b, #1a3d1a);
            border: 2px solid #3fb950;
            border-radius: 12px;
            padding: 1.5rem 2rem;
            text-align: center;
        }
        .result-icon  { font-size: 2.8rem; margin-bottom: 0.4rem; }
        .result-title-fraud { font-size: 1.5rem; font-weight: 700; color: #f85149; margin: 0; }
        .result-title-safe  { font-size: 1.5rem; font-weight: 700; color: #3fb950; margin: 0; }
        .result-sub   { font-size: 0.88rem; color: #8b949e; margin-top: 0.3rem; }

        /* ── History items ── */
        .hist-item {
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.7rem;
        }
        .hist-fraud { border-left: 3px solid #f85149; }
        .hist-safe  { border-left: 3px solid #3fb950; }
        .hist-ts    { font-size: 0.72rem; color: #8b949e; margin-bottom: 0.3rem; }
        .hist-badge-fraud {
            display: inline-block;
            background: rgba(248,81,73,.18);
            color: #f85149;
            border: 1px solid #f85149;
            border-radius: 20px;
            padding: 2px 10px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .hist-badge-safe {
            display: inline-block;
            background: rgba(63,185,80,.18);
            color: #3fb950;
            border: 1px solid #3fb950;
            border-radius: 20px;
            padding: 2px 10px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        /* ── Buttons ── */
        div[data-testid="stButton"] > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all .2s;
        }
        div[data-testid="stButton"] > button:first-child {
            background: linear-gradient(135deg, #1f6feb, #388bfd);
            border: none;
            color: #ffffff;
        }
        div[data-testid="stButton"] > button:first-child:hover {
            background: linear-gradient(135deg, #388bfd, #58a6ff);
            transform: translateY(-1px);
        }

        /* ── Text area ── */
        textarea {
            background-color: #0d1117 !important;
            color: #e6edf3 !important;
            border: 1px solid #30363d !important;
            border-radius: 8px !important;
            font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
            font-size: 0.82rem !important;
        }
        textarea:focus {
            border-color: #1f6feb !important;
            box-shadow: 0 0 0 3px rgba(31,111,235,.25) !important;
        }

        /* ── Sidebar header ── */
        .sidebar-header {
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            color: #8b949e;
            padding-bottom: 0.6rem;
            border-bottom: 1px solid #30363d;
            margin-bottom: 1rem;
        }
        .sidebar-empty {
            color: #484f58;
            font-size: 0.85rem;
            text-align: center;
            padding: 2rem 0;
        }

        /* ── Metric pills ── */
        .meta-row {
            display: flex;
            gap: 0.6rem;
            flex-wrap: wrap;
            margin-top: 0.6rem;
        }
        .meta-pill {
            background: #21262d;
            border: 1px solid #30363d;
            border-radius: 20px;
            padding: 3px 12px;
            font-size: 0.75rem;
            color: #8b949e;
        }
        .meta-pill span { color: #e6edf3; font-weight: 600; }

        /* ── Streamlit overrides ── */
        .stTextArea label { color: #8b949e !important; font-size: 0.85rem !important; }
        [data-testid="stExpander"] {
            background: #0d1117;
            border: 1px solid #21262d;
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Helpers ────────────────────────────────────────────────────────────────────

def call_api(payload: dict) -> dict:
    resp = requests.post(API_URL, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def add_to_history(input_json: dict, result: dict):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "input": input_json,
        "result": result,
    }
    st.session_state.history.insert(0, entry)
    st.session_state.history = st.session_state.history[:MAX_HISTORY]


def is_fraud(result: dict) -> bool:
    for key in ("prediction", "fraud", "is_fraud", "label", "result"):
        if key in result:
            val = result[key]
            if isinstance(val, bool):
                return val
            if isinstance(val, (int, float)):
                return int(val) == 1
            if isinstance(val, str):
                return val.lower() in ("fraud", "1", "true", "yes")
    return False


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-header">📋 Prediction History</div>', unsafe_allow_html=True)

    col_count, col_clear = st.columns([2, 1])
    with col_count:
        count = len(st.session_state.history)
        st.markdown(
            f'<span style="color:#8b949e;font-size:.82rem;">'
            f'{"<b style=\'color:#e6edf3\'>" + str(count) + "</b> " if count else "No "}'
            f'{"entries" if count != 1 else "entry"} (max {MAX_HISTORY})</span>',
            unsafe_allow_html=True,
        )
    with col_clear:
        if st.button("🗑️ Clear", key="clear_hist", use_container_width=True):
            st.session_state.history = []
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown(
            '<div class="hist-empty" style="color:#484f58;font-size:.85rem;text-align:center;padding:2rem 0;">'
            "No predictions yet.<br>Run a prediction to see history here."
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        for i, entry in enumerate(st.session_state.history):
            fraud = is_fraud(entry["result"])
            cls = "hist-fraud" if fraud else "hist-safe"
            badge = (
                '<span class="hist-badge-fraud">⚠ FRAUD</span>'
                if fraud
                else '<span class="hist-badge-safe">✓ SAFE</span>'
            )
            amount = entry["input"].get("Amount", "N/A")
            time_val = entry["input"].get("Time", "N/A")

            st.markdown(
                f"""
                <div class="hist-item {cls}">
                    <div class="hist-ts">🕐 {entry['timestamp']}</div>
                    {badge}
                    <div class="meta-row">
                        <div class="meta-pill">Amount <span>${amount}</span></div>
                        <div class="meta-pill">Time <span>{time_val}s</span></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.expander(f"View JSON #{i + 1}", expanded=False):
                st.json(entry["input"])

# ── Main area ──────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="header-banner">
        <div class="header-icon">🛡️</div>
        <div>
            <p class="header-title">Credit Card Fraud Detection</p>
            <p class="header-sub">ML-powered real-time transaction analysis · PCA-transformed features (V1–V28)</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Two-column layout ──────────────────────────────────────────────────────────
left_col, right_col = st.columns([1.1, 0.9], gap="large")

with left_col:
    st.markdown('<div class="section-label">Transaction Data (JSON)</div>', unsafe_allow_html=True)

    col_sample, col_fmt = st.columns([1, 1])
    with col_sample:
        if st.button("📋 Use Sample Data", use_container_width=True):
            st.session_state.json_input = json.dumps(SAMPLE_DATA, indent=2)
            st.rerun()
    with col_fmt:
        if st.button("✨ Format JSON", use_container_width=True):
            try:
                parsed = json.loads(st.session_state.json_input)
                st.session_state.json_input = json.dumps(parsed, indent=2)
                st.rerun()
            except json.JSONDecodeError:
                st.error("Cannot format — invalid JSON.")

    st.session_state.json_input = st.text_area(
        label="transaction_json",
        value=st.session_state.json_input,
        height=420,
        label_visibility="collapsed",
        placeholder="Paste your transaction JSON here…",
        key="json_textarea",
    )

    predict_btn = st.button("🔍 Predict", use_container_width=True, type="primary")

    # ── Field summary ──────────────────────────────────────────────────────────
    try:
        preview = json.loads(st.session_state.json_input)
        n_fields = len(preview)
        amount = preview.get("Amount", "—")
        time_val = preview.get("Time", "—")
        v_count = sum(1 for k in preview if k.startswith("V"))
        st.markdown(
            f"""
            <div style="margin-top:.8rem;">
                <div class="meta-row">
                    <div class="meta-pill">Fields <span>{n_fields}</span></div>
                    <div class="meta-pill">Amount <span>${amount}</span></div>
                    <div class="meta-pill">Time <span>{time_val}s</span></div>
                    <div class="meta-pill">PCA features <span>{v_count}</span></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except Exception:
        pass

with right_col:
    st.markdown('<div class="section-label">Prediction Result</div>', unsafe_allow_html=True)

    if predict_btn:
        # Validate JSON
        try:
            payload = json.loads(st.session_state.json_input)
        except json.JSONDecodeError as e:
            st.error(f"❌ **Invalid JSON:** {e}")
            st.stop()

        # Call API
        with st.spinner("Analysing transaction…"):
            try:
                result = call_api(payload)
            except requests.exceptions.ConnectionError:
                st.error("🔌 **Connection error:** Could not reach the API. Check your internet connection.")
                st.stop()
            except requests.exceptions.Timeout:
                st.error("⏱️ **Timeout:** The API took too long to respond. Please try again.")
                st.stop()
            except requests.exceptions.HTTPError as e:
                st.error(f"🚫 **HTTP error {e.response.status_code}:** {e.response.text}")
                st.stop()
            except Exception as e:
                st.error(f"⚠️ **Unexpected error:** {e}")
                st.stop()

        # Save history
        add_to_history(payload, result)

        fraud = is_fraud(result)

        if fraud:
            st.markdown(
                """
                <div class="result-fraud">
                    <div class="result-icon">🚨</div>
                    <p class="result-title-fraud">FRAUDULENT TRANSACTION</p>
                    <p class="result-sub">This transaction has been flagged as potentially fraudulent.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="result-safe">
                    <div class="result-icon">✅</div>
                    <p class="result-title-safe">LEGITIMATE TRANSACTION</p>
                    <p class="result-sub">No fraudulent patterns detected in this transaction.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Raw API response
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🔎 Raw API Response", expanded=True):
            st.json(result)

    else:
        # Placeholder state
        st.markdown(
            """
            <div style="
                background:#161b22;
                border:2px dashed #30363d;
                border-radius:12px;
                padding:3rem 2rem;
                text-align:center;
                color:#484f58;
            ">
                <div style="font-size:3rem;margin-bottom:.8rem;">🔍</div>
                <div style="font-size:1rem;font-weight:600;color:#8b949e;">Awaiting Prediction</div>
                <div style="font-size:.85rem;margin-top:.4rem;">
                    Enter transaction data and click <b style="color:#e6edf3;">Predict</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── How it works ──────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("ℹ️ How it works", expanded=False):
        st.markdown(
            """
            **Input fields**
            - `Time` — Seconds elapsed since the first transaction in the dataset
            - `V1–V28` — PCA-transformed features (anonymised for privacy)
            - `Amount` — Transaction amount in USD

            **Model**
            The backend runs a trained ML classifier on the feature vector and returns a binary prediction.

            **API endpoint**
            `POST https://credit-card-fraud-detection-2ia2.onrender.com/predict`
            """,
        )
