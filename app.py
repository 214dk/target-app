import streamlit as st
import pandas as pd
import re

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="بوابة التارجت للموظفين", page_icon="🎯", layout="centered")

# 2. رابط جوجل شيت الخاص بك
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/100B4icHqJA1oO2Zdu0KDHPn2ocXtkzUk/edit?usp=sharing&ouid=117906873751491807989&rtpof=true&sd=true"

# 3. دالة قراءة البيانات من الرابط أونلاين
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
    except Exception as e:
        st.error("❌ خطأ: فشل الاتصال بجوجل شيت. تأكد من أن صلاحية المشاركة مفتوحة للعامة.")
        return None

df_employees = load_data_from_sheets(GOOGLE_SHEET_URL)

# 4. إدارة جلسة العمل
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_data = None

# ----------------- صفحة تسجيل الدخول -----------------
if not st.session_state.logged_in:
    st.title("🔐 بوابة الموظفين الإلكترونية")
    st.write("الرجاء إدخال الرقم الوظيفي وكلمة المرور لمعرفة التارجت الخاص بك.")
    
    user_id = st.text_input("🆔 الرقم الوظيفي (ID):")
    password = st.text_input("🔑 كلمة المرور:", type="password")
    
    if st.button("تسجيل الدخول", use_container_width=True):
        if df_employees is not None:
            user_row = df_employees[(df_employees['ID'] == user_id) & (df_employees['Password'] == password)]
            
            if not user_row.empty:
                st.session_state.logged_in = True
                st.session_state.user_data = user_row.iloc[0]
                st.rerun()
            else:
                st.error("❌ الرقم الوظيفي أو كلمة المرور غير صحيحة!")

# ----------------- صفحة عرض التارجت -----------------
else:
    user = st.session_state.user_data
    
    # شريط علوي للترحيب وزر خروج
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.title(f"👋 مرحباً، {user['Name']}")
    with col_logout:
        st.write("") 
        if st.button("🏃 خروج", type="secondary"):
            st.session_state.logged_in = False
            st.session_state.user_data = None
            st.rerun()
            
    st.markdown(f"**الرقم الوظيفي:** {user['ID']}")
    st.markdown("---")
    
    st.subheader("🎯 التارجت الخاص بك للفترة الحالية:")
    
    # تصحيح السطر المسبب للمشكلة بالكامل
    target_value = float(user['Target'])
    
    # عرض النسبة المئوية والجملة المعدلة
    st.metric(label="النسبه المحققه", value=f"{target_value}%")
    
    st.info("💡 نصيحة: تذكر أن تحقيق التارجت يسهم في رفع تقييمك السنوي والحصول على الحوافز والمكافآت.")