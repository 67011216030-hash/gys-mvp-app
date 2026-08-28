import streamlit as st
import pandas as pd

st.title("ระบบบันทึกชั่วโมง กยศ.")
st.write("อัปโหลดรูปภาพและกรอกรายละเอียดกิจกรรมเพื่อจัดเก็บเป็นหลักฐาน")

# ส่วนที่ 1: ฟอร์มกรอกข้อมูลและอัปโหลดรูปภาพ
with st.form("activity_form"):
    activity_name = st.text_input("ชื่อกิจกรรม")
    activity_date = st.date_input("วันที่จัดกิจกรรม")
    activity_hours = st.number_input("จำนวนชั่วโมงที่ได้รับ", min_value=1, step=1)
    uploaded_file = st.file_uploader("อัปโหลดรูปภาพหลักฐาน", type=["jpg", "png", "jpeg"])
    
    submitted = st.form_submit_button("บันทึกข้อมูล")
    
    if submitted:
        if activity_name and uploaded_file:
            st.success("บันทึกข้อมูลสำเร็จ!")
            st.image(uploaded_file, caption=f"หลักฐาน: {activity_name}")
            st.write(f"**วันที่:** {activity_date} | **จำนวนชั่วโมง:** {activity_hours} ชั่วโมง")
        else:
            st.error("กรุณากรอกชื่อกิจกรรมและอัปโหลดรูปภาพ")

st.divider()

# ส่วนที่ 2: ตารางแสดงข้อมูลจำลอง (Dashboard)
st.subheader("ประวัติกิจกรรมที่บันทึกไว้ (ข้อมูลจำลอง)")
data = {
    "ชื่อกิจกรรม": ["อบรมวิชาการ", "ค่ายอาสา", "ปลูกป่า"],
    "วันที่": ["2026-08-10", "2026-08-15", "2026-08-22"],
    "ชั่วโมง": [3, 6, 4]
}
df = pd.DataFrame(data)
st.table(df)

total_hours = df["ชั่วโมง"].sum()
st.metric(label="ยอดชั่วโมงสะสมรวม", value=f"{total_hours} ชั่วโมง")
