import streamlit as st
import pandas as pd
import datetime

st.title("ระบบบันทึกชั่วโมง กยศ.")
st.write("อัปโหลดรูปภาพและกรอกรายละเอียดกิจกรรมเพื่อจัดเก็บเป็นหลักฐาน")

# ส่วนที่ 1: ฟอร์มกรอกข้อมูลและอัปโหลดรูปภาพ
with st.form("activity_form"):
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
            st.success("บันทึกข้อมูลสำเร็จ!")
            st.image(uploaded_file, caption=f"หลักฐาน: {activity_name}")
            st.write(f"**ผู้รับผิดชอบโครงการ:** {project_owner}")
            st.write(f"**วันที่:** {activity_date} | **เวลา:** {start_time.strftime('%H.%M')} - {end_time.strftime('%H.%M')} น.")
            st.write(f"**จำนวนชั่วโมง:** {activity_hours} ชั่วโมง")
        else:
            st.error("กรุณากรอกชื่อกิจกรรมและอัปโหลดรูปภาพ")

st.divider()

# ส่วนที่ 2: ตารางแสดงข้อมูลจำลอง (Dashboard)
st.subheader("ประวัติกิจกรรมที่บันทึกไว้ (ข้อมูลจำลอง)")
data = {
    "ชื่อกิจกรรม": ["อบรมวิชาการ", "ค่ายอาสา", "ปลูกป่า"],
    "ผู้รับผิดชอบ": ["อ.สมชาย", "พี่ประธานค่าย", "กองกิจการนิสิต"],
    "วันที่": ["2026-08-10", "2026-08-15", "2026-08-22"],
    "เวลา": ["09.00 - 12.00", "08.00 - 16.00", "09.00 - 15.00"],
    "ชั่วโมง": [3, 8, 6]
}
df = pd.DataFrame(data)
st.table(df)

total_hours = df["ชั่วโมง"].sum()
st.metric(label="ยอดชั่วโมงสะสมรวม", value=f"{total_hours} ชั่วโมง")

st.divider()

# ส่วนที่ 3: ปุ่ม Export PDF (Mockup)
st.subheader("ส่งออกเอกสาร")
if st.button("📄 ดาวน์โหลดสรุปกิจกรรม (PDF)"):
    st.info("📌 (จำลองระบบ) ระบบจะทำการสร้างไฟล์ PDF ที่มีรูปภาพและรายละเอียดทั้งหมด พร้อมเว้นช่องว่างสำหรับให้ผู้รับผิดชอบเซ็นชื่อ")
