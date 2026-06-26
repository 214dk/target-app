import streamlit as st
import pandas as pd
import re

# 1. إعدادات الصفحة والثيم الاحترافي
st.set_page_config(page_title="بوابة التارجت 2.0", page_icon="🎯", layout="centered")

# إضافة Custom CSS لتغيير شكل الموقع بالكامل
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: rtl;
    }
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 15px;
        border-bottom: 4px solid #3b82f6;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stMetricValue"] {
        color: #60a5fa !important;
        font-size: 50px !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #3b82f6;
        color: white;
        border: none;
        font-weight: bold;
    }
    .stProgress > div > div > div > div {
        background-color: #60a5fa;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. رابط جوجل شيت
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/100B4icHqJA1oO2Zdu0KDHPn2ocXtkzUk/edit?usp=sharing&ouid=117906873751491807989&rtpof=true&sd=true"

def load_data_from_sheets(url):
    try:
        match = re.search(r"/d/([^/]+)", url)
        if match:
            sheet_id = match.group(1)
            direct_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
        else:
            direct_url = url
        df = pd.read_excel(direct_url)
        df['ID'] = df['ID'].astype(str)
        df['Password'] = df['Password'].astype(str)
        return df
    except Exception:
        st.error("❌ فشل الاتصال بالبيانات.. تأكد من صلاحية الرابط.")
        return None

df_employees = load_data_from_sheets(GOOGLE_SHEET_URL)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_data = None

# --- صفحة الدخول ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #60a5fa;'>🎯 بوابة التارجت الذكية</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>أهلاً بك في نظام متابعة الأداء المطور</p>", unsafe_allow_html=True)
    
    with st.container():
        user_id = st.text_input("🆔 الرقم الوظيفي:")
        password = st.text_input("🔑 كلمة المرور:", type="password")
        
        if st.button("تسجيل الدخول"):
            if df_employees is not None:
                user_row = df_employees[(df_employees['ID'] == user_id) & (df_employees['Password'] == password)]
                if not user_row.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_data = user_row.iloc[0]
                    st.rerun()
                else:
                    st.error("❌ البيانات غير صحيحة")

# --- صفحة العرض ---
else:
    user = st.session_state.user_data
    target_val = float(user['Target'])
    
    # هيدر الصفحة
    st.markdown(f"<h2 style='text-align: right; color: #f8fafc;'>👋 مرحباً، {user['Name']}</h2>", unsafe_allow_html=True)
    
    # بطاقة التارجت
    st.markdown("---")
    st.metric(label="نسبة المستهدف المطلوب تحقيقها", value=f"{target_val}%")
    
    # شريط التقدم (Progress Bar)
    st.write("")
    progress_val = min(target_val / 100, 1.0) # عشان ميعملش خطأ لو النسبة فوق 100
    st.progress(progress_val)
    
    # رسالة تحفيزية ذكية
    if target_val >= 100:
        st.success("🏆 بطل! لقد حققت كامل التارجت بنجاح باهر.")
        st.balloons()
    elif target_val >= 80:
        st.info("🚀 رائع! أنت على وشك الوصول، استمر في الضغط.")
    elif target_val >= 50:
        st.warning("💪 مجهود جيد، النصف الثاني من الشهر يحتاج همة أكبر.")
    else:
        st.error("⚠️ نحتاج لتركيز أكبر في الفترة القادمة لتحسين النسبة.")

    st.markdown("---")
    if st.button("🏃 تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
