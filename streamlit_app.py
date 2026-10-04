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
        activity_date = st.date_input("วันที่จัดกิจกรรม", datetime.date(2026, 10, 4))
    with col2:
        start_time = st.time_input("เวลาเริ่ม", datetime.time(9, 0))
    with col3:
        end_time = st.time_input("เวลาสิ้นสุด", datetime.time(11, 0))
        
    # ปรับค่าเริ่มต้นเป็น 2 ชั่วโมงให้สอดคล้องกับเวลา 09:00 - 11:00
    hours_earned = st.number_input("จำนวนชั่วโมงที่ได้รับ", min_value=1, step=1, value=2)
    
    uploaded_file = st.file_uploader("อัปโหลดรูปภาพหลักฐาน", type=["jpg", "png"])
    
    # ปุ่ม Submit ต้องอยู่ภายใน with st.form()
    submitted = st.form_submit_button("บันทึกข้อมูล")

    # ลอจิกจัดการข้อมูลเมื่อกดบันทึก
    if submitted:
        if activity_name and project_owner:
            # จัดรูปแบบเวลาให้อ่านง่าย
            time_str = f"{start_time.strftime('%H.%M')} - {end_time.strftime('%H.%M')}"
            
            # เพิ่มข้อมูลที่กรอกใหม่ลงใน Session State
            st.session_state.activity_list.append({
                "ชื่อกิจกรรม": activity_name,
                "ผู้รับผิดชอบ": project_owner,
                "วันที่": activity_date.strftime("%Y-%m-%d"),
                "เวลา": time_str,
                "ชั่วโมง": hours_earned
            })
            st.success("บันทึกข้อมูลกิจกรรมเรียบร้อยแล้ว!")
        else:
            st.error("กรุณากรอกชื่อกิจกรรมและชื่อผู้รับผิดชอบให้ครบถ้วน")

# ส่วนที่ 2: แสดงผลข้อมูลที่บันทึกแล้วเพื่อตรวจเช็ก
st.subheader("ประวัติกิจกรรมที่บันทึกแล้ว")
if st.session_state.activity_list:
    df = pd.DataFrame(st.session_state.activity_list)
    # ใช้ st.dataframe เพื่อแสดงตารางแบบ Interactive
    st.dataframe(df, use_container_width=True)
    
    # สรุปยอดชั่วโมงรวมทั้งหมด
    total_hours = df["ชั่วโมง"].sum()
    st.info(f"รวมชั่วโมงจิตอาสาทั้งหมด: **{total_hours} ชั่วโมง**")
