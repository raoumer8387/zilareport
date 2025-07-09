import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 🌐 Inject custom CSS for white background, RTL, and Urdu font
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/earlyaccess/notonastaliqurdu.css');

        html, body, .stApp, .block-container, .main, [class^="css"] {
            font-family: 'Noto Nastaliq Urdu', serif !important;
            direction: rtl;
            text-align: right;
            background-color: white !important;
            color: black !important;
            font-size: 22px !important;
        }

        /* ✅ Text & Number Inputs */
        input[type="text"],
        input[type="number"],
        input[type="password"],
        textarea,
        .stTextArea > div > textarea {
            background-color: white !important;
            color: black !important;
            border: 1px solid black !important;
            border-radius: 5px !important;
            padding: 8px !important;
            font-size: 20px !important;
            margin-top: 0px !important; /* Reduce top margin */
        }

        /* ✅ Select boxes */
        .stSelectbox div[data-baseweb="select"],
        .stMultiSelect div[data-baseweb="select"],
        div[role="combobox"] {
            background-color: white !important;
            color: black !important;
            border: 1px solid black !important;
            border-radius: 5px !important;
            font-size: 20px !important;
        }

        /* ✅ Buttons */
        .stButton button {
            background-color: #1a73e8 !important;
            color: white !important;
            font-size: 18px !important;
            border-radius: 5px !important;
        }

        /* ✅ Sidebar */
        [data-testid="stSidebar"] {
            background-color: white !important;
            color: black !important;
            font-size: 20px !important;
        }

        /* ✅ Custom container for label and input */
        .input-container {
            margin-bottom: 5px !important; /* Reduce space between containers */
        }

        .input-container label {
            font-weight: bold;
            margin-bottom: 2px !important; /* Minimal space below label */
            display: block;
        }

        .input-container input {
            width: 100%;
            box-sizing: border-box;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 📥 Load login credentials
try:
    users_df = pd.read_excel("users.xlsx")
except FileNotFoundError:
    st.error("یوزر ڈیٹا فائل نہیں ملی۔")
    st.stop()

try:
    report_df = pd.read_excel("report_data.xlsx")
except FileNotFoundError:
    st.error("رپورٹ ڈیٹا فائل نہیں ملی۔")
    st.stop()

# 🔐 Session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ''
    st.session_state.zila = ''

# 🔐 Login form
def login():
    st.title("امیروں کے لیے لاگ ان")

    username = st.text_input("یوزر نیم")
    password = st.text_input("پاس ورڈ", type="password")
    if st.button("لاگ ان"):
        user = users_df[(users_df['username'] == username) & (users_df['password'] == password)]
        if not user.empty:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.zila = user.iloc[0]['zila']
            st.rerun()
        else:
            st.error("غلط یوزر نیم یا پاس ورڈ")

# 📋 Report form
def report_form():
    st.title(f"رپورٹ برائے {st.session_state.zila}")

    # 🔴 Logout Button
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("لاگ آؤٹ"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.zila = ""
            st.rerun()

    zila = st.session_state.zila

    # 📅 Previous Month Info
    this_month = datetime.today().replace(day=1)
    last_month = (this_month - timedelta(days=1)).strftime('%Y-%m')

    prev = report_df[(report_df['zila'] == zila) & (report_df['month'] == last_month)]

    prev_arkaan = int(prev['arkaan'].values[0]) if not prev.empty else 0
    prev_members = int(prev['members'].values[0]) if not prev.empty else 0

    # ارکان
    st.markdown(f"<b>پچھلے مہینے کے ارکان:</b> {prev_arkaan}", unsafe_allow_html=True)
    arkaan_col1, arkaan_col2 = st.columns([2, 3])
    with arkaan_col1:
        st.markdown("اس مہینے کے ارکان درج کریں:")
    with arkaan_col2:
        new_arkaan = st.number_input("", min_value=0, key="arkaan", label_visibility="collapsed")

# ممبرز
    st.markdown(f"<b>پچھلے مہینے کے ممبرز:</b> {prev_members}", unsafe_allow_html=True)
    member_col1, member_col2 = st.columns([2, 3])
    with member_col1:
        st.markdown("اس مہینے کے ممبرز درج کریں:")
    with member_col2:
        new_members = st.number_input("", min_value=0, key="members", label_visibility="collapsed")


    if st.button("رپورٹ جمع کروائیں"):
        new_entry = {
            'zila': zila,
            'month': this_month.strftime('%Y-%m'),
            'arkaan': new_arkaan,
            'members': new_members
        }
        report_df.loc[len(report_df)] = new_entry
        try:
            report_df.to_excel("report_data.xlsx", index=False)
            st.success("رپورٹ کامیابی سے جمع ہو گئی ہے!")
        except Exception as e:
            st.error(f"رپورٹ جمع کرنے میں خرابی: {e}")

# 🧠 Run App Logic
if st.session_state.logged_in:
    report_form()
else:
    login()