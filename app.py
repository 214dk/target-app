import streamlit as st
import pandas as pd
import re
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="بوابة الأداء الرقمية", page_icon="🎯", layout="centered")

# هندسة الواجهة برمجياً بشكل جذري وجديد تماماً للعين والموبايل
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إلغاء هيدر وقائمة وماركة ستريمليت الافتراضية تماماً ليكون الموقع خاص بك */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ضبط الخلفية والخطوط بشكل إجباري */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #090d16 !important;
        font-family: 'Cairo', sans-serif !important;
        text-align: right !important;
        direction: rtl !important;
    }
    
    /* توسيط وضبط حاوية اللوجو */
    [data-testid="stHorizontalBlock"] {
        align-items: center !important;
    }
    
    /* تحسين شكل النصوص المساعدة */
    p, span, label {
        font-family: 'Cairo', sans-serif !important;
    }

    /* تكبير وتوضيح عناوين حقول الإدخال */
    label[data-testid="stWidgetLabel"] p {
        font-size: 19px !important;
        font-weight: 700 !important;
        color: #94a3b8 !important;
        margin-bottom: 10px !important;
    }
    
    /* حقول إدخال غاية في الفخامة والانسيابية */
    .stTextInput div div input {
        font-size: 20px !important;
        padding: 15px !important;
        height: 56px !important;
        border-radius: 16px !important;
        background-color: #111827 !important;
        color: #ffffff !important;
        border: 2px solid #1f2937 !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput div div input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.3) !important;
    }

    /* تصميم بطاقة المستهدف بنظام النيون المتوهج الفاخر */
    .stMetric {
        background: linear-gradient(135deg, #111827 0%, #0f172a 100%) !important;
        padding: 35px 20px !important;
        border-radius: 24px !important;
        border: 2px solid #1e3a8a !important;
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.25) !important;
        text-align: center !important;
        margin-top: 20px !important;
    }
    /* النص داخل البطاقة */
    div[data-testid="stMetricLabel"] > div {
        font-size: 21px !important;
        font-weight: 700 !important;
        color: #94a3b8 !important;
        justify-content: center !important;
    }
    /* الرقم المئوي الضخم والواضح جداً */
    div[data-testid="stMetricValue"] {
        color: #60a5fa !important;
        font-size: 75px !important;
        font-weight: 900 !important;
        margin-top: 10px !important;
        text-shadow: 0 0 10px rgba(96, 165, 250, 0.3) !important;
    }
    
    /* تصميم الأزرار كالتطبيقات الذكية */
    .stButton>button {
        width: 100% !important;
        border-radius: 16px !important;
        height: 58px !important;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: white !important;
        border: none !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 24px rgba(37, 99, 235, 0.45) !important;
    }
    
    /* تنعيم شريط التقدم وزيادة سمكه ليظهر بوضوح */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #60a5fa 0%, #2563eb 100%) !important;
        height: 18px !important;
        border-radius: 10px !important;
    }
    .stProgress > div > div {
        height: 18px !important;
        background-color: #1f2937 !important;
        border-radius: 10px !important;
    }

    /* صناديق الرسائل التنبيهية */
    .stAlert {
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        background-color: #111827 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. رابط جوجل شيت الخاص بك
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
        return None

df_employees = load_data_from_sheets(GOOGLE_SHEET_URL)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_data = None

# --- صفحة الدخول الاحترافية ---
if not st.session_state.logged_in:
    st.write("")
    
    # توسيط اللوجو بدقة متناهية
    if os.path.exists("logo.png"):
        col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
        with col_l2:
            st.image("logo.png", use_container_width=True)
        
    st.markdown("<h1 style='text-align: center; color: #ffffff; font-weight: 900; font-size: 36px; margin-top: 15px;'>🎯 نظام متابعة الأداء</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 18px; margin-bottom: 35px;'>سجل دخولك الآن لمتابعة المستهدف الحالي</p>", unsafe_allow_html=True)
    
    with st.container():
        user_id = st.text_input("🆔 الرقم الوظيفي:")
        password = st.text_input("🔑 كلمة المرور:", type="password")
        
        st.write("")
        if st.button("دخول آمن للرصيد"):
            if df_employees is not None:
                user_row = df_employees[(df_employees['ID'] == user_id) & (df_employees['Password'] == password)]
                if not user_row.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_data = user_row.iloc[0]
                    st.rerun()
                else:
                    st.error("❌ عذراً، الرقم الوظيفي أو كلمة المرور غير صحيحة.")

# --- صفحة عرض التارجت للموظف ---
else:
    user = st.session_state.user_data
    target_val = float(user['Target'])
    
    # تنسيق الهيدر العلوي بشكل متناسق جداً للموبايل مع اللوجو جانبياً
    col_emp, col_lg = st.columns([3.5, 1])
    with col_emp:
        st.markdown(f"<h2 style='text-align: right; color: #ffffff; font-weight: 900; font-size: 32px; margin-bottom: 5px; margin-top: 10px;'>👋 أهلاً، {user['Name']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: right; color: #64748b; font-size: 16px; margin: 0;'>الرقم الوظيفي: {user['ID']}</p>", unsafe_allow_html=True)
    with col_lg:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=75)

    st.markdown("<div style='height: 2px; background-color: #1f2937; margin: 25px 0;'></div>", unsafe_allow_html=True)
    
    # بطاقة التارجت النيون الجديدة
    st.metric(label="نسبة المستهدف المطلوب تحقيقها", value=f"{target_val}%")
    
    # شريط التقدم السميك
    st.write("")
    progress_val = min(target_val / 100, 1.0)
    st.progress(progress_val)
    st.write("")
    
    # رسائل التوجيه والتحفيز (بدون تغيير أي نص)
    if target_val >= 100:
        st.success("🏆 أداء أسطوري! لقد قمت بتقفيل التارجت بالكامل لهذا الشهر.")
        st.balloons()
    elif target_val >= 80:
        st.info("🚀 رائع جداً! أنت في الأمتار الأخيرة، تفصلك خطوات بسيطة.")
    elif target_val >= 50:
        st.warning("💪 مجهود طيب! تجاوزت نصف الطريق، اضغط أكثر لتصل إلى القمة.")
    else:
        st.error("⚠️ بداية تحتاج إلى همّة أعلى! ركز جهودك في الأيام القادمة لتحسين النسبة.")

    st.markdown("<div style='height: 2px; background-color: #1f2937; margin: 35px 0;'></div>", unsafe_allow_html=True)
    
    if st.button("🏃 خروج بأمان"):
        st.session_state.logged_in = False
        st.rerun()
