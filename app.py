import streamlit as st
import pandas as pd
import re
import os

# 1. إعدادات الصفحة والثيم الاحترافي الفاخر
st.set_page_config(page_title="بوابة الأداء الرقمية", page_icon="🎯", layout="centered")

# إضافة Custom CSS فائق الاحترافية لتنسيق الألوان، الخطوط، وتوسيط اللوجو
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap');
    
    /* ضبط الخلفية العامة والخطوط */
    html, body, [class*="css"], .stMarkdown, p, span, label, input {
        font-family: 'Cairo', sans-serif !important;
        text-align: right !important;
        direction: rtl !important;
    }
    
    /* تهيئة وتوسيط حاوية اللوجو */
    .logo-box {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin: 20px auto 10px auto;
    }
    .logo-box img {
        display: block;
        margin: 0 auto;
    }

    /* تكبير وتنسيق عناوين المدخلات لتكون مريحة للعين */
    label[data-testid="stWidgetLabel"] p {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        margin-bottom: 8px !important;
    }
    
    /* تصميم حقول الإدخال الاحترافي (المودرن) */
    .stTextInput div div input {
        font-size: 20px !important;
        padding: 12px 15px !important;
        height: 54px !important;
        border-radius: 12px !important;
        background-color: #141b27 !important;
        color: #ffffff !important;
        border: 2px solid #232e42 !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput div div input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    }

    /* تصميم بطاقة التارجت الزجاجية الفاخرة */
    .stMetric {
        background: linear-gradient(145deg, #141b27 0%, #0d131f 100%) !important;
        padding: 30px !important;
        border-radius: 20px !important;
        border: 1px solid #232e42 !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4) !important;
        text-align: center !important;
    }
    div[data-testid="stMetricLabel"] > div {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #64748b !important;
        justify-content: center !important;
    }
    div[data-testid="stMetricValue"] {
        color: #3b82f6 !important;
        font-size: 70px !important;
        font-weight: 800 !important;
        letter-spacing: -1px !important;
        margin-top: 15px !important;
    }
    
    /* تصميم الأزرار الفخم والملس */
    .stButton>button {
        width: 100% !important;
        border-radius: 14px !important;
        height: 56px !important;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        color: white !important;
        border: none !important;
        font-size: 19px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.25) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
    }
    
    /* تحسين وتنعيم شريط التقدم */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #60a5fa 0%, #3b82f6 100%) !important;
        height: 14px !important;
        border-radius: 20px !important;
    }
    .stProgress > div > div {
        height: 14px !important;
        background-color: #1e293b !important;
        border-radius: 20px !important;
    }

    /* تحسين مظهر رسائل التنبيه والنجاح */
    .stAlert {
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
    }
    .stAlert p {
        font-size: 18px !important;
        font-weight: 500 !important;
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
    
    # عرض اللوجو متمركزاً ومحاذياً تماماً في المنتصف
    if os.path.exists("logo.png"):
        col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
        with col_l2:
            st.image("logo.png", use_container_width=True)
        
    st.markdown("<h1 style='text-align: center; color: #ffffff; font-weight: 800; font-size: 34px; margin-top: 10px;'>🎯 نظام متابعة الأداء</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 18px; margin-bottom: 30px;'>سجل دخولك الآن لمتابعة المستهدف الحالي</p>", unsafe_allow_html=True)
    
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
    
    # تنسيق راقي جداً لبيانات الموظف واللوجو بجانبه
    col_emp, col_lg = st.columns([4, 1])
    with col_emp:
        st.markdown(f"<h2 style='text-align: right; color: #ffffff; font-weight: 800; font-size: 30px; margin-bottom: 5px;'>👋 أهلاً، {user['Name']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: right; color: #64748b; font-size: 16px; margin: 0;'>الرقم الوظيفي: {user['ID']}</p>", unsafe_allow_html=True)
    with col_lg:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=75)

    st.markdown("<div style='height: 1px; background-color: #232e42; margin: 25px 0;'></div>", unsafe_allow_html=True)
    
    # بطاقة التارجت المحسنة بصرياً
    st.metric(label="نسبة المستهدف المطلوب تحقيقها", value=f"{target_val}%")
    
    # شريط التقدم الفاخر
    st.write("")
    progress_val = min(target_val / 100, 1.0)
    st.progress(progress_val)
    st.write("")
    
    # الرسائل الذكية المبنية على النسبة دون تعديل في النصوص
    if target_val >= 100:
        st.success("🏆 أداء أسطوري! لقد قمت بتقفيل التارجت بالكامل لهذا الشهر.")
        st.balloons()
    elif target_val >= 80:
        st.info("🚀 رائع جداً! أنت في الأمتار الأخيرة، تفصلك خطوات بسيطة.")
    elif target_val >= 50:
        st.warning("💪 مجهود طيب! تجاوزت نصف الطريق، اضغط أكثر لتصل إلى القمة.")
    else:
        st.error("⚠️ بداية تحتاج إلى همّة أعلى! ركز جهودك في الأيام القادمة لتحسين النسبة.")

    st.markdown("<div style='height: 1px; background-color: #232e42; margin: 35px 0;'></div>", unsafe_allow_html=True)
    
    # تعديل بسيط في زر الخروج ليصبح بتصميم متناسق وراقٍ مع الواجهة الداكنة
    if st.button("🏃 خروج بأمان"):
        st.session_state.logged_in = False
        st.rerun()
