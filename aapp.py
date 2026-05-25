import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import random

# 🎨 ऐप सेटिंग्स (इसे मोबाइल ऐप जैसा दिखाने के लिए सेंटर्ड और टाइट रखा है)
st.set_page_config(
    page_title="Shree Vyapaar", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# 🖌️ प्रीमियम मोबाइल ऐप UI - वेबसाइट वाला लुक पूरी तरह खत्म
st.markdown("""
<style>
    /* पूरे बैकग्राउंड को डार्क और प्रीमियम लुक देना */
    [data-testid="stAppViewContainer"] {
        background: #0f172a;
        font-family: 'Inter', sans-serif;
    }
    
    /* मोबाइल ऐप कंटेनर (जो इसे वेबसाइट के बजाय ऐप बनाएगा) */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        max-width: 450px !important; /* मोबाइल स्क्रीन साइज */
    }
    
    /* ऐप का मुख्य लोगो और हेडर कार्ड */
    .app-logo-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 20px;
        border-radius: 24px;
        text-align: center;
        border: 2px solid #22c55e;
        box-shadow: 0 10px 25px rgba(34, 197, 94, 0.2);
        margin-bottom: 20px;
    }
    
    /* इनपुट फॉर्म को ऐप का लुक देना */
    div[data-testid="stForm"] {
        background: #1e293b !important;
        border-radius: 24px !important;
        padding: 20px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
    }
    
    /* मोबाइल इनपुट बॉक्स स्टाइलिंग */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 14px !important;
        padding: 12px !important;
        font-size: 16px !important;
    }
    .stTextInput input:focus {
        border-color: #22c55e !important;
    }
    
    /* चमचमाता हुआ सुपरफास्ट बटन */
    div.stButton > button {
        width: 100%;
        border-radius: 16px;
        height: 54px;
        font-size: 18px;
        font-weight: 700;
        background: linear-gradient(90deg, #15803d, #22c55e) !important;
        color: white !important;
        border: none;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4);
        transition: 0.3s;
        text-transform: uppercase;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(34, 197, 94, 0.6);
    }
    
    /* 🧾 असली थर्मल डिजिटल बिल (रसीद काउंटर लुक) */
    .digital-bill {
        background: #ffffff;
        color: #1e293b;
        padding: 25px 20px;
        border-radius: 4px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        font-family: 'Courier New', Courier, monospace;
        margin-top: 25px;
        position: relative;
        border-top: 8px solid #22c55e;
    }
    /* बिल के नीचे कटी हुई रसीद जैसा ज़िग-ज़ैग लुक */
    .digital-bill::after {
        content: "";
        position: absolute;
        bottom: -10px;
        left: 0;
        width: 100%;
        height: 100px;
        background-image: linear-gradient(-45deg, #0f172a 5px, transparent 0), linear-gradient(45deg, #0f172a 5px, transparent 0);
        background-size: 10px 10px;
    }
    
    label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        margin-bottom: 6px !important;
    }
</style>
""", unsafe_allow_html=True)

# 🔱 ऐप का सुंदर लोगो और हेडर (मोबाइल स्टाइल)
st.markdown("""
<div class="app-logo-card">
    <span style="font-size: 42px;">💼</span>
    <h2 style="margin: 5px 0 0 0; color: #ffffff; font-weight: 800; letter-spacing: 0.5px;">श्री व्यापार</h2>
    <p style="margin: 0; color: #22c55e; font-size: 14px; font-weight: 600; text-transform: uppercase;">Smart Billing Solution</p>
</div>
""", unsafe_allow_html=True)

# ☁️ लाइव क्लाउड डेटाबेस कनेक्शन 
BILL_COLS = ['date', 'bill_no', 'buyer_name', 'seller_name', 'item_details', 'total_amount', 'paid_amount', 'balance_amount']

@st.cache_data(ttl=0)
def load_vyapaar_data():
    blank_df = pd.DataFrame(columns=BILL_COLS)
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        try:
            df = pd.DataFrame(conn.read(worksheet="VyapaarBills"))
            for col in BILL_COLS:
                if col not in df.columns: df[col] = None
            return conn, df
        except: return conn, blank_df
    except: return None, blank_df

conn, bills_df = load_vyapaar_data()

# 📝 मोबाइल बिलिंग एंट्री फॉर्म
with st.form("vyapaar_form", clear_on_submit=False):
    st.markdown("<p style='color:#ffffff; font-size:18px; font-weight:700; margin-top:0;'>📝 न्यू इनवॉइस एंट्री</p>", unsafe_allow_html=True)
    
    buyer = st.text_input("👤 क्रेता (ग्राहक) का नाम")
    seller = st.text_input("👤 विक्रेता (व्यापारी) का नाम")
    items = st.text_area("🌾 सौदा/सामान/जमीन का विवरण", placeholder="विवरण यहाँ लिखें...")
    
    total_amt = st.number_input("💵 कुल रकम (₹)", min_value=0.0, step=500.0)
    paid_amt = st.number_input("💵 नगद भुगतान प्राप्त (₹)", min_value=0.0, step=500.0)
    
    st.write("")
    submit_btn = st.form_submit_button("⚡ सेव करें और डिजिटल बिल निकालें")

# 🧾 डेटा प्रोसेसिंग और सुंदर डिजिटल बिल जेनरेशन
if submit_btn:
    if not buyer or not seller or not items:
        st.error("❌ कृपया सभी जरूरी नाम और विवरण भरें!")
    else:
        balance_amt = total_amt - paid_amt
        current_date = datetime.now().strftime("%d-%m-%Y %I:%M %p")
        bill_number = "SV" + str(random.randint(100050, 999999))
        
        # क्लाउड (Google Sheets) में डेटा सुरक्षित सहेजना
        new_row = pd.DataFrame([{
            "date": current_date, "bill_no": bill_number, "buyer_name": buyer, 
            "seller_name": seller, "item_details": items, "total_amount": total_amt, 
            "paid_amount": paid_amt, "balance_amount": balance_amt
        }])
        
        if conn is not None:
            try:
                updated_df = pd.concat([bills_df, new_row], ignore_index=True)
                conn.update(worksheet="VyapaarBills", data=updated_df)
                st.toast("✅ क्लाउड में सुरक्षित सहेजा गया!", icon="☁️")
            except:
                pass
                
        # 🧾 असली रसीद जैसा दिखने वाला डिजिटल बिल
        st.markdown(f"""
        <div class="digital-bill">
            <div style="text-align: center; margin-bottom: 15px;">
                <h3 style="margin: 0; color: #000000; font-weight: bold; font-size: 20px;">** श्री व्यापार **</h3>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #475569;">डिजिटल इनवॉइस / पावती रसीद</p>
            </div>
            <p style="font-size: 12px; margin: 0;"><b>तारीख:</b> {current_date}</p>
            <p style="font-size: 12px; margin: 3px 0 10px 0;"><b>रसीद नंबर:</b> {bill_number}</p>
            <div style="border-top: 1px dashed #000000; margin: 10px 0;"></div>
            
            <p style="margin: 6px 0;"><b>🤝 क्रेता:</b> {buyer}</p>
            <p style="margin: 6px 0;"><b>👤 विक्रेता:</b> {seller}</p>
            <p style="margin: 6px 0;"><b>📦 विवरण:</b> {items}</p>
            
            <div style="border-top: 1px dashed #000000; margin: 10px 0;"></div>
            
            <table style="width:100%; font-size: 14px; font-weight: bold; margin-top: 10px;">
                <tr>
                    <td style="padding: 3px 0;">कुल सौदा मूल्य:</td>
                    <td style="text-align: right;">₹{total_amt:,.2f}</td>
                </tr>
                <tr style="color: #16a34a;">
                    <td style="padding: 3px 0;">प्राप्त राशि (+):</td>
                    <td style="text-align: right;">₹{paid_amt:,.2f}</td>
                </tr>
                <tr style="color: #dc2626; border-top: 1px solid #000000;">
                    <td style="padding: 5px 0; font-size: 15px;">बकाया राशि (🔴):</td>
                    <td style="text-align: right; font-size: 15px;">₹{balance_amt:,.2f}</td>
                </tr>
            </table>
            
            <div style="border-top: 1px dashed #000000; margin: 15px 0 10px 0;"></div>
            <p style="text-align: center; font-size: 11px; margin: 0; font-weight: bold; color: #475569;">🙏 व्यापार में जुड़ने के लिए धन्यवाद 🙏</p>
        </div>
        <br><br>
        """, unsafe_allow_html=True)
        st.caption("📱 बिल आ गया है भाई साहब! इसका स्क्रीनशॉट खींचकर आप अपने कस्टमर को सीधे व्हाट्सएप पर भेज सकते हैं।")
