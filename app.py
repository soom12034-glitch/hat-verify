import streamlit as st
from googleapiclient.discovery import build
from google.oauth2 import service_account
import base64

st.set_page_config(page_title="HAT Verification", layout="centered")

# الاتصال بجوجل درايف عبر الأسرار (Secrets)
def get_drive_service():
    if "gcp_service_account" in st.secrets:
        info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(info)
        return build('drive', 'v3', credentials=creds)
    else:
        st.error("لم يتم إعداد مفاتيح الاتصال (Secrets) في الموقع.")
        return None

def show_pdf(file_id):
    try:
        service = get_drive_service()
        if not service: return
        
        request = service.files().get_media(fileId=file_id)
        pdf_content = request.execute()
        base64_pdf = base64.b64encode(pdf_content).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    except:
        st.error("الشهادة غير موجودة أو الرابط غير صحيح.")

st.title("🛡️ نظام التحقق - HAT Engineering")
file_id = st.query_params.get("id")

if file_id:
    show_pdf(file_id)
else:
    st.info("يرجى مسح الباركود من الشهادة.")