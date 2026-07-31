import streamlit as st
import requests
import os
import base64
import streamlit.components.v1 as components

# 🟢 تم تحديث الرابط الافتراضي ليشمل /api/chat
BACKEND_URL = os.getenv("BACKEND_URL", "https://chatbot-nienava-backend.onrender.com/api/chat")

SYSTEM_AVATAR = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
USER_AVATAR = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80"
AD_AVATAR = "https://cdn-icons-png.flaticon.com/512/2997/2997311.png"

def query_backend_api(user_query):
    """إرسال السؤال إلى FastAPI على Render مع رفع مهلة الانتظار"""
    try:
        response = requests.post(
            BACKEND_URL,
            json={"question": user_query},
            headers={"Content-Type": "application/json"},
            timeout=120  # رفع المهلة إلى 120 ثانية لاستيقاظ Render وتجهيز الـ RAG
        )
        if response.status_code == 200:
            return response.json().get("answer", "لم يتم العثور على إجابة.")
        elif response.status_code == 404:
            return f"❌ خطأ (404): المسار غير موجود. تأكد من أن الرابط هو:\n`{BACKEND_URL}`"
        else:
            return f"عذراً، حدث خطأ في الاستجابة من الخادم (رمز الخطأ: {response.status_code})."
            
    except requests.exceptions.Timeout:
        return "⏳ الخادم يستغرق وقتاً أطول للاستيقاظ وتحميل النماذج. يرجى إرسال السؤال مرة أخرى الآن."
    except Exception as e:
        return f"خطأ في الاتصال بالشبكة: {str(e)}"
