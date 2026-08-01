import streamlit as st
import os
import requests
import streamlit.components.v1 as components

# رابط الباك إند على Render
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

SYSTEM_AVATAR = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
USER_AVATAR = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80"
AD_AVATAR = "https://cdn-icons-png.flaticon.com/512/2997/2997311.png"

# قائمة الإعلانات (تمت إضافة إعلان التواصل عبر الواتساب)
ADS_DATA = [
    {
        "type": "whatsapp",
        "url": "https://wa.me/9647712345678", 
        "title": "التواصل مع الواتساب", 
        "phone": "07712345678"
    },
    {"type": "image", "image": "https://ik.imagekit.io/63rncvror/img1.png?updatedAt=1785603220307", "url": "https://www.facebook.com/profile.php?id=61589363754427", "title": "مجمع المثنى الطبي"},
    {"type": "image", "image": "https://i.ibb.co/BHpCVXw6/ad2.png", "url": "https://www.facebook.com/najmatalmosulco/", "title": "شركة نجمة الموصل"},
    {"type": "image", "image": "https://i.ibb.co/wFZ8Y205/ad3.png", "url": "https://baly.iq/taxi/", "title": "تطبيق بلي - توصيل سريع"},
    {"type": "image", "image": "https://i.ibb.co/hFdR7xP1/ad4.png", "url": "https://www.iq.zain.com/ar", "title": "زين العراق - أحدث العروض"},
    {"type": "image", "image": "https://i.ibb.co/TBQZh7mm/ad5.png", "url": "https://www.facebook.com/profile.php?id=100063940127604", "title": "إعلان راعي المنصة"},
    {"type": "image", "image": "https://i.ibb.co/FkkqgTp0/ad6.png", "url": "https://www.facebook.com/larsafoundation/", "title": "مؤسسة لارسا"},
    {"type": "image", "image": "https://i.ibb.co/GvYcqGz2/ad7.png", "url": "https://www.facebook.com/barqmouslba/", "title": "برق الموصل"},
    {"type": "image", "image": "https://i.ibb.co/GQ5rhcrm/ad8.png", "url": "https://www.facebook.com/p/%D9%85%D8%AC%D9%85%D8%B9-%D8%B3%D9%8A%D8%AF-%D8%A7%D9%84%D8%A7%D8%B3%D8%B9%D8%A7%D8%B1-3-%D9%81%D8%B1%D8%B9-%D8%A7%D9%84%D9%85%D8%AC%D9%85%D8%B9%D8%A9-100066359418433/?locale=ku_TR", "title": "مجمع سيد الاسعار"},
    {"type": "image", "image": "https://i.ibb.co/Jjby0JYZ/ad9.png", "url": "https://www.facebook.com/anaskashmola/", "title": "خدمات إعلانية متميزة"},
    {"type": "image", "image": "https://i.ibb.co/FqCZ3Sch/ad10.png", "url": "https://alnoor.edu.iq/ar/", "title": "جامعة النور الأهلية"}
]

def render_ads_carousel():
    slides_html = ""
    for ad in ADS_DATA:
        if ad.get("type") == "whatsapp":
            slides_html += f"""
            <div class="swiper-slide">
                <a href="{ad['url']}" target="_blank" class="ad-card-link">
                    <div class="ad-card whatsapp-card">
                        <img src="https://cdn-icons-png.flaticon.com/512/3670/3670051.png" class="wa-icon" alt="WhatsApp" />
                        <div class="wa-title">{ad['title']}</div>
                        <div class="wa-phone">{ad['phone']}</div>
                    </div>
                </a>
            </div>
            """
        else:
            slides_html += f"""
            <div class="swiper-slide">
                <a href="{ad['url']}" target="_blank" class="ad-card-link">
                    <div class="ad-card" style="--bg-image: url('{ad['image']}');">
                        <img src="{ad['image']}" alt="{ad['title']}" loading="eager" />
                    </div>
                </a>
            </div>
            """

    carousel_html = f"""
    <!DOCTYPE html>
    <html dir="ltr">
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
        <style>
            body {{ 
                margin: 0; 
                font-family: system-ui, -apple-system, sans-serif; 
                background: transparent; 
                direction: ltr; 
            }}
            .swiper {{ 
                width: 100%; 
                padding: 10px 5px 30px 5px; 
            }}
            .swiper-slide {{ 
                width: 320px; 
            }}
            .ad-card-link {{ 
                text-decoration: none; 
                display: block; 
            }}
            
            .ad-card {{ 
                position: relative;
                width: 100%; 
                height: 180px; 
                border-radius: 16px; 
                overflow: hidden; 
                box-shadow: 0 6px 18px rgba(0,0,0,0.12); 
                transition: transform 0.3s ease, box-shadow 0.3s ease; 
                display: flex;
                align-items: center;
                justify-content: center;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
            
            .ad-card::before {{
                content: "";
                position: absolute;
                top: -10%;
                left: -10%;
                width: 120%;
                height: 120%;
                background-image: var(--bg-image);
                background-size: cover;
                background-position: center;
                filter: blur(16px) brightness(0.85);
                transform: scale(1.1);
                z-index: 1;
            }}

            /* تصميم كارد الواتساب المميز */
            .whatsapp-card {{
                background: linear-gradient(135deg, #128C7E 0%, #25D366 100%) !important;
                flex-direction: column !important;
                gap: 8px;
                color: white;
                text-align: center;
                padding: 15px;
                box-sizing: border-box;
            }}
            .whatsapp-card::before {{
                display: none !important;
            }}
            .wa-icon {{
                width: 52px !important;
                height: 52px !important;
                filter: drop-shadow(0 4px 6px rgba(0,0,0,0.15)) !important;
            }}
            .wa-title {{
                font-size: 18px;
                font-weight: 700;
                margin-top: 4px;
            }}
            .wa-phone {{
                font-size: 20px;
                font-weight: 800;
                letter-spacing: 1px;
                background: rgba(255, 255, 255, 0.2);
                padding: 4px 16px;
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.4);
            }}

            .ad-card:hover {{ 
                transform: translateY(-5px) scale(1.02); 
                box-shadow: 0 12px 25px rgba(0,0,0,0.2); 
            }}

            .ad-card:hover::before {{
                filter: blur(12px) brightness(0.95);
            }}
            
            .ad-card img {{ 
                position: relative;
                z-index: 2;
                width: 100%; 
                height: 100%; 
                max-width: 100%; 
                max-height: 100%; 
                object-fit: contain; 
                object-position: center; 
                display: block;
                filter: drop-shadow(0 4px 8px rgba(0,0,0,0.25));
            }}
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
    components.html(carousel_html, height=235)

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
            html, body, [class*="css"] { 
                font-family: 'Cairo', sans-serif; 
                direction: ltr !important; 
                text-align: left !important; 
            }
            [data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="collapsedControl"] { 
                display: none !important; 
            }
            footer { visibility: hidden; }
            header [data-testid="stAppDeployButton"] { display: none; }
        </style>
    """, unsafe_allow_html=True)

    # رأس الصفحة العلوي
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; direction: ltr; margin-bottom: 15px;">
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
