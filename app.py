import streamlit as st
import requests
import os
import base64
import streamlit.components.v1 as components

# رابط الـ API المنشور على Render
BACKEND_URL = os.getenv("BACKEND_URL", "https://your-rag-backend.onrender.com/api/chat")

SYSTEM_AVATAR = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
USER_AVATAR = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80"
AD_AVATAR = "https://cdn-icons-png.flaticon.com/512/2997/2997311.png"

ADS_DATA = [
    {"image": "/content/ads/ad1.webp", "url": "https://voyager.mynu.app/restaurant/675af6c4fc92f8671caef3cc", "title": "مطعم فاخر - عروض خاصة"},
    {"image": "/content/ads/ad2.webp", "url": "https://www.facebook.com/najmatalmosulco/", "title": "شركة نجمة الموصل"},
    # ... بقية الإعلانات كما هي
]

@st.cache_data
def get_base64_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            ext = os.path.splitext(image_path)[1].replace(".", "").lower()
            mime_types = {"gif": "image/gif", "webp": "image/webp", "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}
            mime_type = mime_types.get(ext, f"image/{ext}")
            return f"data:{mime_type};base64,{encoded_string}"
        else:
            return "https://picsum.photos/500/200"
    except Exception:
        return "https://picsum.photos/500/200"

def render_ads_carousel():
    # كود الـ Carousel القديم نفسه بدون تعديل
    pass

def query_backend(user_query):
    try:
        # رفع المهلة إلى 90 ثانية لمنح الـ RAG الخطة المجانية وقتاً كافياً
        response = requests.post(
            BACKEND_URL,
            json={"question": user_query},
            headers={"Content-Type": "application/json"},
            timeout=90  
        )
        if response.status_code == 200:
            return response.json().get("answer", "لم يتم العثور على إجابة.")
        else:
            return f"خطأ من الخادم (رمز: {response.status_code})"
    except requests.exceptions.Timeout:
        return "⏳ الخادم يستغرق وقتاً أطول لمعالجة الطلب الأول (تحميل النماذج). يرجى الضغط على إرسال مرة أخرى الآن."
    except Exception as e:
        return f"خطأ في الاتصال: {str(e)}"

def process_rag_response(user_query):
    with st.chat_message("assistant", avatar=SYSTEM_AVATAR):
        with st.spinner("جاري البحث ..."):
            result = query_backend_api(user_query)
            st.markdown(result)
    
    st.session_state.messages.append({'role': 'assistant', 'type': 'text', 'content': result})
    st.session_state.bot_response_count += 1

    if st.session_state.bot_response_count % 3 == 0:
        with st.chat_message("assistant", avatar=AD_AVATAR):
            st.write("📢 **عروض وإعلانات رعاية المنصة:**")
            render_ads_carousel()
        st.session_state.messages.append({'role': 'assistant', 'type': 'carousel'})

def main():
    st.set_page_config(page_title="المجيب الآلي - تربية نينوى وجامعة الموصل", page_icon="🤖", layout="centered")

    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'bot_response_count' not in st.session_state:
        st.session_state.bot_response_count = 0

    st.write("🌟 **إعلانات متميزة:**")
    render_ads_carousel()

    for message in st.session_state.messages:
        if message.get('type') == 'carousel':
            with st.chat_message("assistant", avatar=AD_AVATAR):
                st.write("📢 **عروض وإعلانات رعاية المنصة:**")
                render_ads_carousel()
        else:
            avatar = USER_AVATAR if message['role'] == 'user' else SYSTEM_AVATAR
            st.chat_message(message['role'], avatar=avatar).markdown(message['content'])

    prompt = st.chat_input("اكتب سؤالك هنا...")
    if prompt:
        st.chat_message('user', avatar=USER_AVATAR).markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'type': 'text', 'content': prompt})
        process_rag_response(prompt)

if __name__ == "__main__":
    main()
