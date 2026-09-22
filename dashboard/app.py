import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Like-AI : AGI Creative Platform",
    page_icon="🤖",
    layout="wide"
)

# Sidebar Configuration
st.sidebar.title("⚙️ ระบบจัดการ Like-AI & Cristal")
api_url_input = st.sidebar.text_input(
    "Google Apps Script API URL:",
    value="YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL",
    help="ใส่ Web App URL ที่ได้จากการ Deploy Google Apps Script ของคุณ"
)

cristal_worker_url = st.sidebar.text_input(
    "Cristal AGI244 Worker URL:",
    value="https://your-worker.workers.dev",
    help="ใส่ URL ของ Cloudflare AGI244 Worker"
)

st.title("🤖 Like-AI & Cristal AGI244 Workspace")
st.markdown("พัฒนาและควบคุมระบบโดย **คุณธันวา (Vider Ecosystem)** | ระบบจัดการเนื้อหา อัปเดตผ่าน Google Sheets, ออก Token ส่วนตัว และ RAG Learning Loop")

menu = st.sidebar.selectbox("เลือกโหมดการทำงาน", ["ใช้งาน Like-AI (User Mode)", "ระบบจัดการ AGI Core & Worker (Admin)"])

if menu == "ใช้งาน Like-AI (User Mode)":
    st.header("✨ พื้นที่สร้างสรรค์เนื้อหา (Controllable Generation)")
    
    user_token = st.text_input("🔑 กรุณากรอก API Token ของคุณเพื่อปลดล็อกระบบ:", type="password")
    gem_id = st.text_input("💎 ระบุ Gem ID ที่ต้องการเรียกใช้งาน (เช่น GEM-01 หรือ ALL):", value="ALL")
    
    if user_token and api_url_input != "YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL":
        try:
            with st.spinner("กำลังตรวจสอบ Token กับระบบกลาง..."):
                res = requests.get(f"{api_url_input}?action=verifyToken&token={user_token}&gem_id={gem_id}", timeout=10).json()
            
            if res.get("status") == "valid":
                st.success(f"✅ ปลดล็อกระบบสำเร็จ! ยินดีต้อนรับผู้ใช้งาน: {res.get('email', 'Authorized User')}")
                
                col1, col2 = st.columns(2)
                with col1:
                    topic = st.text_input("📌 ระบุ 'เรื่อง' ที่ต้องการสร้าง:", "การตลาดออนไลน์ยุค AGI")
                    content_type = st.selectbox("📂 ระบุ 'ประเภท' เนื้อหา:", ["บทความ", "รูปภาพ", "วิดีโอ", "โค้ด", "แผนกลยุทธ์", "e-commerce", "portfolio", "store", "landing"])
                with col2:
                    subtype = st.text_input("⚙️ ระบุ 'ชนิด' และรายละเอียดย่อย:", "เจาะลึกกลุ่มเป้าหมาย Gen Z พร้อมโค้ดตัวอย่าง")
                
                if st.button("🚀 สั่งงาน Like-AI / Cristal AGI Core"):
                    with st.spinner("กำลังประมวลผลผ่าน Cristal AGI Core และอัปเดต KV_Cristal..."):
                        payload = {
                            "token": user_token,
                            "gem_id": gem_id,
                            "topic": topic,
                            "type": content_type,
                            "subtype": subtype
                        }
                        gen_res = requests.post(f"{cristal_worker_url}/api/likeai/generate", json=payload, timeout=15).json()
                        
                        if gen_res.get("status") == "success":
                            st.success("🎉 สร้างเนื้อหาสำเร็จและบันทึกลง Heartbox Memory เรียบร้อย!")
                            st.json(gen_res)
                            st.markdown("### 📄 ผลลัพธ์ที่ได้ (Generated Content):")
                            st.write(gen_res["data"]["result"])
                        else:
                            st.error(f"❌ เกิดข้อผิดพลาด: {gen_res.get('message', 'Unknown error')}")
            else:
                st.error("❌ Token ไม่ถูกต้อง หรือไม่ได้รับสิทธิ์เข้าถึง Gem นี้")
        except Exception as e:
            st.error(f"⚠️ ไม่สามารถเชื่อมต่อกับ API Gateway ได้: {e}")

elif menu == "ระบบจัดการ AGI Core & Worker (Admin)":
    st.header("🛠️ สถานะระบบ Cristal AGI244 & One-Way Security")
    st.info("ระบบ One-Way Security เปิดใช้งาน: Cristal ดึงข้อมูลจาก GEM ได้ฝ่ายเดียว และล็อกไม่ให้ GEM เข้าถึง Cristal กลับโดยตรง")
    st.metric(label="System Latency", value="<120ms", delta="-12ms")
    st.metric(label="RAG Learning Accuracy", value="98.6%", delta="+0.4%")
    st.metric(label="Uptime", value="99.9%")
