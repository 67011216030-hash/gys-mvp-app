import streamlit as st
import pandas as pd
import datetime

st.title("ระบบบันทึกชั่วโมง กยศ.")
st.write("อัปโหลดรูปภาพและกรอกรายละเอียดกิจกรรมเพื่อจัดเก็บเป็นหลักฐาน")

# สร้าง Session State เพื่อเก็บข้อมูลชั่วคราว (จำลองการดึงข้อมูลจาก Database)
if "activity_list" not in st.session_state:
    st.session_state.activity_list = [
        {"ชื่อกิจกรรม": "อบรมวิชาการ", "ผู้รับผิดชอบ": "อ.สมชาย", "วันที่": "2026-08-10", "เวลา": "09.00 - 12.00", "ชั่วโมง": 3},
        {"ชื่อกิจกรรม": "ค่ายอาสา", "ผู้รับผิดชอบ": "พี่ประธานค่าย", "วันที่": "2026-08-15", "เวลา": "08.00 - 16.00", "ชั่วโมง": 8}
    ]

# ส่วนที่ 1: ฟอร์มกรอกข้อมูลและอัปโหลดรูปภาพ
with st.form("activity_form", clear_on_submit=True):
    activity_name = st.text_input("ชื่อกิจกรรม")
    project_owner = st.text_input("ชื่อผู้รับผิดชอบโครงการ (สำหรับติดต่อขอลายเซ็น)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        activity_date = st.date_input("วันที่จัดกิจกรรม")
    with col2:
        start_time = st.time_input("เวลาเริ่ม", datetime.time(9, 0))
    with col3:
        end_time = st.time_input("เวลาสิ้นสุด", datetime.time(11, 0))
        
    activity_hours = st.number_input("จำนวนชั่วโมงที่ได้รับ", min_value=1, step=1)
    uploaded_file = st.file_uploader("อัปโหลดรูปภาพหลักฐาน", type=["jpg", "png", "jpeg"])
    
    submitted = st.form_submit_button("บันทึกข้อมูล")
    
    if submitted:
        if activity_name and uploaded_file:
            # นำข้อมูลใหม่ที่เพิ่งกรอก ไปต่อท้ายในตารางฐานข้อมูลจำลอง
            new_activity = {
                "ชื่อกิจกรรม": activity_name,
                "ผู้รับผิดชอบ": project_owner,
                "วันที่": activity_date.strftime("%Y-%m-%d"),
                "เวลา": f"{start_time.strftime('%H.%M')} - {end_time.strftime('%H.%M')}",
                "ชั่วโมง": activity_hours
            }
            st.session_state.activity_list.append(new_activity)
            
            st.success("บันทึกข้อมูลสำเร็จ! เลื่อนดูข้อมูลที่อัปเดตในตารางด้านล่างได้เลย")
            # สามารถเพิ่มบรรทัดนี้เพื่อพรีวิวรูปภาพที่อัปโหลด
            # st.image(uploaded_file, caption="รูปภาพหลักฐาน", width=300)
        else:
            st.error("กรุณากรอกชื่อกิจกรรมและอัปโหลดรูปภาพ")

st.divider()

# ส่วนที่ 2: ตารางแสดงข้อมูล
st.subheader("ประวัติกิจกรรมที่บันทึกไว้")
df = pd.DataFrame(st.session_state.activity_list)
st.table(df)

# คำนวณยอดชั่วโมงรวมแบบเรียลไทม์
total_hours = df["ชั่วโมง"].sum()
st.metric(label="ยอดชั่วโมงสะสมรวม", value=f"{total_hours} ชั่วโมง")

st.divider()

# ส่วนที่ 3: ปุ่ม Export PDF (Mockup)
st.subheader("ส่งออกเอกสาร")
if st.button("📄 ดาวน์โหลดสรุปกิจกรรม (PDF)"):
    st.info("📌 (จำลองระบบ) ระบบจะทำการสร้างไฟล์ PDF ที่มีรูปภาพและรายละเอียดทั้งหมด พร้อมเว้นช่องว่างสำหรับให้ผู้รับผิดชอบเซ็นชื่อ")
