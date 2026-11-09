import streamlit as st
import time
from google import genai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 1. إعداد ذكاء Gemini
GEMINI_KEY = "AQ.Ab8RN6KzxdWErsyX-a7PB3gVKvxhDI31Z5fRQUBu_nqRIctzzg"
client = genai.Client(api_key=GEMINI_KEY)

# رابط صفحة تسجيل الدخول الرسمية لمنصة SPRIX
PLATFORM_URL = "https://sprix.com"

st.set_page_config(page_title="منصة الحل التلقائي العالمية", page_icon="🤖", layout="centered")

st.title("🤖 منصة الحل التلقائي العالمية - SPRIX")
st.write("اكتب بيانات حسابك بالأسفل، وسيقوم السيرفر بالدخول تلقائياً وحل كافة الاختبارات بناءً على نموذج الإجابات الذكي!")

# خانات إدخال البيانات لأي طالب في العالم
student_id = st.text_input("👤 معرف تسجيل الدخول (كود الطالب):", placeholder="اكتب كودك هنا...")
student_pass = st.text_input("🔑 كلمة المرور الخاصة بالمنصة:", type="password", placeholder="اكتب كلمة مرورك هنا...")

if st.button("🚀 ابدأ الحل التلقائي الفوري", use_container_width=True):
    if not student_id or not student_pass:
        st.error("من فضلك، أدخل كود الطالب وكلمة المرور أولاً!")
    else:
        status_box = st.info("🌐 جاري تشغيل المتصفح السحابي والتوجه للمنصة...")
        
        # إعدادات المتصفح المخفي (Headless) ليعمل بذكاء وسرعة على السيرفر العالمي
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        try:
            driver.get(PLATFORM_URL)
            time.sleep(5) 
            
            status_box.info(f"🔐 جاري تسجيل الدخول للحساب رقم ({student_id}) تلقائياً...")
            driver.find_element(By.ID, "login-id").send_keys(student_id)
            driver.find_element(By.ID, "password").send_keys(student_pass)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(6) 
            
            status_box.info("🔓 تم الدخول بنجاح! جاري التوجه لصفحة الأسئلة وحلها تلقائياً...")
            
            question_text = driver.find_element(By.TAG_NAME, "body").text 
            
            prompt = f"أنت خبير ثقافة مالية. اقرأ السؤال المتاح في الصفحة واختر الإجابة الصحيحة المطابقة لمنهج SPRIX بدقة: \n{question_text}"
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            ai_answer = response.text.strip()
            
            status_box.success(f"🎯 اختار الذكاء الاصطناعي بنجاح: {ai_answer}")
            st.balloons()
            
        except Exception as e:
            status_box.error(f"❌ حدث توقف أثناء الحل التلقائي: {str(e)}")
        finally:
            driver.quit()
