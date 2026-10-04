import streamlit as st
import pandas as pd
import datetime
import base64

st.title("ระบบบันทึกชั่วโมง กยศ.")
st.write("อัปโหลดรูปภาพและกรอกรายละเอียดกิจกรรมเพื่อจัดเก็บเป็นหลักฐาน")

# ฟังก์ชันสำหรับแปลงไฟล์รูปภาพที่อัปโหลดให้เป็น Base64 Data URL (เพื่อให้แสดงในตารางได้)
def get_image_base64(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        b64_str = base64.b64encode(bytes_data).decode()
        mime_type = uploaded_file.type
        return f"data:{mime_type};base64,{b64_str}"
    return None

# สร้าง Session State เพื่อเก็บข้อมูลชั่วคราว
if "activity_list" not in st.session_state:
    st.session_state.activity_list = [
        {"รูปภาพ": None, "ชื่อกิจกรรม": "อบรมวิชาการ", "ผู้รับผิดชอบ": "อ.สมชาย", "วันที่เริ่มต้น": datetime.date(2026, 8, 10), "วันที่สิ้นสุด": datetime.date(2026, 8, 10), "เวลา": "09.00 - 12.00", "ชั่วโมง": 3},
        {"รูปภาพ": None, "ชื่อกิจกรรม": "ค่ายอาสา", "ผู้รับผิดชอบ": "พี่ประธานค่าย", "วันที่เริ่มต้น": datetime.date(2026, 8, 15), "วันที่สิ้นสุด": datetime.date(2026, 8, 16), "เวลา": "08.00 - 16.00", "ชั่วโมง": 8}
    ]

# ส่วนที่ 1: ฟอร์มกรอกข้อมูล
with st.form("activity_form", clear_on_submit=True):
    activity_name = st.text_input("ชื่อกิจกรรม")
    project_owner = st.text_input("ชื่อผู้รับผิดชอบโครงการ (สำหรับติดต่อขอลายเซ็น)")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        start_date = st.date_input("วันที่เริ่มต้น")
    with col2:
        end_date = st.date_input("วันที่สิ้นสุด")
    with col3:
        start_time = st.time_input("เวลาเริ่ม", datetime.time(9, 0))
    with col4:
        end_time = st.time_input("เวลาสิ้นสุด", datetime.time(11, 0))
        
    activity_hours = st.number_input("จำนวนชั่วโมงที่ได้รับ", min_value=1, step=1, value=2)
    uploaded_file = st.file_uploader("อัปโหลดรูปภาพหลักฐาน", type=["jpg", "png", "jpeg"])
    
    submitted = st.form_submit_button("บันทึกข้อมูล")
    
    if submitted:
        if start_date > end_date:
            st.error("❌ วันที่เริ่มต้นต้องไม่ช้ากว่าวันที่สิ้นสุด")
        # บังคับว่าต้องกรอกข้อมูลและอัปโหลดรูปภาพด้วย ถึงจะบันทึกได้
        elif activity_name and project_owner and uploaded_file:
            # แปลงภาพเป็น Base64
            img_b64 = get_image_base64(uploaded_file)
            
            new_activity = {
                "รูปภาพ": img_b64,
                "ชื่อกิจกรรม": activity_name,
                "ผู้รับผิดชอบ": project_owner,
                "วันที่เริ่มต้น": start_date,
                "วันที่สิ้นสุด": end_date,
                "เวลา": f"{start_time.strftime('%H.%M')} - {end_time.strftime('%H.%M')}",
                "ชั่วโมง": activity_hours
            }
            st.session_state.activity_list.append(new_activity)
            st.success("✅ บันทึกข้อมูลพร้อมรูปภาพหลักฐานสำเร็จ!")
        else:
            st.error("❌ กรุณากรอกชื่อกิจกรรม ชื่อผู้รับผิดชอบ และอัปโหลดรูปภาพหลักฐานให้ครบถ้วน")

st.divider()

# ส่วนที่ 2: ตารางแสดงข้อมูล
st.subheader("ประวัติกิจกรรมที่บันทึกไว้")
st.caption("💡 ทิปส์: ดับเบิลคลิกที่ตารางเพื่อแก้ไขข้อมูล หรือเลือกแถวแล้วกดไอคอนถังขยะเพื่อลบ")

df = pd.DataFrame(st.session_state.activity_list)

# แสดงผลตารางและกำหนดค่าคอลัมน์ "รูปภาพ" ให้แสดงผลเป็นภาพ (ImageColumn)
edited_df = st.data_editor(
    df,
    column_config={
        "รูปภาพ": st.column_config.ImageColumn(
            "หลักฐาน", help="รูปภาพหลักฐานกิจกรรม", width="medium"
        )
    },
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
)

# อัปเดตข้อมูลกลับเข้า Session State หากมีการแก้ไขหรือลบออก
st.session_state.activity_list = edited_df.to_dict('records')

# คำนวณยอดชั่วโมงรวมแบบเรียลไทม์
total_hours = edited_df["ชั่วโมง"].sum() if not edited_df.empty else 0
st.metric(label="ยอดชั่วโมงสะสมรวม", value=f"{total_hours} ชั่วโมง")

st.divider()

# ส่วนที่ 3: ปุ่ม Export PDF
st.subheader("ส่งออกเอกสาร")
if st.button("📄 ดาวน์โหลดสรุปกิจกรรม (PDF)"):
    st.info("📌 (จำลองระบบ) ระบบจะทำการสร้างไฟล์ PDF ที่มีรูปภาพและรายละเอียดทั้งหมด พร้อมเว้นช่องว่างสำหรับให้ผู้รับผิดชอบเซ็นชื่อ")
