import streamlit as st
import os
import requests
import streamlit.components.v1 as components

# رابط الباك إند على Render
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

SYSTEM_AVATAR = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
USER_AVATAR = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80"
AD_AVATAR = "https://cdn-icons-png.flaticon.com/512/2997/2997311.png"

# ملاحظة: يجب استبدال الروابط أدناه بالروابط المباشرة (Direct Links) من ImgBB والتي تبدأ عادة بـ https://i.ibb.co/
ADS_DATA = [
    {"image": "https://i.ibb.co/mFPQP30c/ad1.webp", "url": "https://voyager.mynu.app/restaurant/675af6c4fc92f8671caef3cc", "title": "مطعم فاخر - عروض خاصة"},
    {"image": "https://i.ibb.co/BHpCVXw6/ad2.webp", "url": "https://www.facebook.com/najmatalmosulco/", "title": "شركة نجمة الموصل"},
    {"image": "https://i.ibb.co/wFZ8Y205/ad3.webp", "url": "https://baly.iq/taxi/", "title": "تطبيق بلي - توصيل سريع"},
    {"image": "https://i.ibb.co/hFdR7xP1/ad4.webp", "url": "https://www.iq.zain.com/ar", "title": "زين العراق - أحدث العروض"},
    {"image": "https://i.ibb.co/TBQZh7mm/ad5.webp", "url": "https://www.facebook.com/profile.php?id=100063940127604", "title": "إعلان راعي المنصة"},
    {"image": "https://i.ibb.co/FkkqgTp0/ad6.webp", "url": "https://www.facebook.com/larsafoundation/", "title": "مؤسسة لارسا"},
    {"image": "https://i.ibb.co/GvYcqGz2/ad7.webp", "url": "https://www.facebook.com/barqmouslba/", "title": "برق الموصل"},
    {"image": "https://i.ibb.co/GQ5rhcrm/ad8.webp", "url": "https://www.facebook.com/p/%D9%85%D8%AC%D9%85%D8%B9-%D8%B3%D9%8A%D8%AF-%D8%A7%D9%84%D8%A7%D8%B3%D8%B9%D8%A7%D8%B1-3-%D9%81%D8%B1%D8%B9-%D8%A7%D9%84%D9%85%D8%AC%D9%85%D8%B9%D8%A9-100066359418433/?locale=ku_TR", "title": "مجمع سيد الاسعار"},
    {"image": "https://i.ibb.co/Jjby0JYZ/ad9.webp", "url": "https://www.facebook.com/anaskashmola/", "title": "خدمات إعلانية متميزة"},
    {"image": "https://i.ibb.co/FqCZ3Sch/ad10.webp", "url": "https://alnoor.edu.iq/ar/", "title": "جامعة النور الأهلية"}
]

def render_ads_carousel():
    slides_html = ""
    for ad in ADS_DATA:
        # استخدام رابط الصورة المباشر فوراً دون الحاجة للـ Base64
        slides_html += f"""
        <div class="swiper-slide">
            <a href="{ad['url']}" target="_blank" class="ad-card-link">
                <div class="ad-card">
                    <img src="{ad['image']}" alt="{ad['title']}" />
                </div>
            </a>
        </div>
        """

    carousel_html = f"""
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
        <style>
            body {{ margin: 0; font-family: system-ui, -apple-system, sans-serif; background: transparent; }}
            .swiper {{ width: 100%; padding: 10px 5px 30px 5px; }}
            .swiper-slide {{ width: 240px; }}
            .ad-card-link {{ text-decoration: none; display: block; }}
            .ad-card {{ width: 100%; height: 140px; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.08); transition: transform 0.2s ease, box-shadow 0.2s ease; background: #f1f5f9; }}
            .ad-card:hover {{ transform: translateY(-4px) scale(1.02); box-shadow: 0 8px 20px rgba(0,0,0,0.15); }}
            .ad-card img {{ width: 100%; height: 100%; object-fit: cover; object-position: center; display: block; }}
        </style>
    </head>
    <body>
        <div class="swiper mySwiper">
            <div class="swiper-wrapper">
                {slides_html}
            </div>
            <div class="swiper-pagination"></div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
        <script>
            var swiper = new Swiper(".mySwiper", {{
                slidesPerView: "auto",
                spaceBetween: 15,
                grabCursor: true,
                autoplay: {{ delay: 2800, disableOnInteraction: false }},
                pagination: {{ el: ".swiper-pagination", clickable: true }},
            }});
        </script>
    </body>
    </html>
    """
    components.html(carousel_html, height=195)

def ask_backend(user_query):
    try:
        res = requests.post(f"{BACKEND_URL}/chat", json={"query": user_query}, timeout=60)
        if res.status_code == 200:
            return res.json().get("answer", "لم يتم الحصول على إجابة.")
        else:
            return "حدث خطأ في الاتصال بالخادم."
    except Exception as e:
        return f"خطأ في الاتصال: {str(e)}"

def main():
    st.set_page_config(
        page_title="المجيب الآلي - تربية نينوى وجامعة الموصل",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'bot_response_count' not in st.session_state:
        st.session_state.bot_response_count = 0

    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
            html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl !important; text-align: right !important; }
            [data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="collapsedControl"] { display: none !important; }
            footer {visibility: hidden;}
            header [data-testid="stAppDeployButton"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; direction: rtl; margin-bottom: 15px;">
            <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; width: 45px; height: 45px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;">🤖</div>
            <h1 style="margin: 0; color: #3b82f6; font-weight: 700; font-size: 22px;">المجيب الآلي تربية نينوى وجامعة الموصل</h1>
        </div>
    """, unsafe_allow_html=True)

    st.write("**إعلانات:**")
    render_ads_carousel()

    for message in st.session_state.messages:
        if message.get('type') == 'carousel':
            with st.chat_message("assistant", avatar=AD_AVATAR):
                st.write("**اعلانات:**")
                render_ads_carousel()
        else:
            avatar = USER_AVATAR if message['role'] == 'user' else SYSTEM_AVATAR
            st.chat_message(message['role'], avatar=avatar).markdown(message['content'])

    prompt = st.chat_input("اكتب سؤالك هنا...")
    if prompt:
        st.chat_message('user', avatar=USER_AVATAR).markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'type': 'text', 'content': prompt})

        with st.chat_message("assistant", avatar=SYSTEM_AVATAR):
            with st.spinner("جاري البحث ..."):
                result = ask_backend(prompt)
                st.markdown(result)

        st.session_state.messages.append({'role': 'assistant', 'type': 'text', 'content': result})
        st.session_state.bot_response_count += 1

        if st.session_state.bot_response_count % 3 == 0:
            with st.chat_message("assistant", avatar=AD_AVATAR):
                st.write("**اعلانات:**")
                render_ads_carousel()
            st.session_state.messages.append({'role': 'assistant', 'type': 'carousel'})

if __name__ == "__main__":
    main()
