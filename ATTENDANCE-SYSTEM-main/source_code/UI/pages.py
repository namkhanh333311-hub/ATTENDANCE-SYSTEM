import streamlit as st
import pandas as pd

# Khởi tạo dữ liệu mẫu trong session_state nếu chưa có
def init_session_state():
    if 'students' not in st.session_state:
        st.session_state.students = []
    if 'classes' not in st.session_state:
        st.session_state.classes = []
    if 'attendance' not in st.session_state:
        st.session_state.attendance = []

# --- TRANG 1: QUẢN LÝ LỚP HỌC ---
def render_quan_ly_lop():
    st.title("🏫 Quản lý lớp học")
    col1, col2 = st.columns([1, 2])
    with col1:
        with st.form("form_lop"):
            ma_lop = st.text_input("Mã lớp (VD: IT01)")
            tong_buoi = st.number_input("Tổng số buổi học", min_value=1, step=1)
            if st.form_submit_button("Thêm Lớp"):
                if ma_lop:
                    st.session_state.classes.append({"Mã Lớp": ma_lop, "Tổng Buổi": tong_buoi})
                    st.success("Thêm lớp thành công!")
                else:
                    st.error("Vui lòng nhập Mã lớp!")
    with col2:
        if st.session_state.classes:
            st.dataframe(pd.DataFrame(st.session_state.classes), use_container_width=True)
        else:
            st.info("Chưa có dữ liệu lớp học.")

# --- TRANG 2: QUẢN LÝ SINH VIÊN ---
def render_quan_ly_sv():
    st.title("👨‍🎓 Quản lý sinh viên")
    col1, col2 = st.columns([1, 2])
    with col1:
        with st.form("form_sv"):
            ma_sv = st.text_input("Mã sinh viên")
            ten_sv = st.text_input("Họ và tên")
            lop = st.selectbox("Chọn lớp", [c["Mã Lớp"] for c in st.session_state.classes]) if st.session_state.classes else st.selectbox("Chọn lớp", ["Chưa có lớp"])
            if st.form_submit_button("Thêm Sinh Viên"):
                if ma_sv and ten_sv:
                    st.session_state.students.append({"Mã SV": ma_sv, "Họ Tên": ten_sv, "Lớp": lop})
                    st.success("Thêm thành công!")
                else:
                    st.error("Vui lòng nhập đủ thông tin!")
    with col2:
        if st.session_state.students:
            st.dataframe(pd.DataFrame(st.session_state.students), use_container_width=True)
        else:
            st.info("Chưa có sinh viên.")

# --- TRANG 3: QUẢN LÝ THỜI KHÓA BIỂU ---
def render_quan_ly_tkb():
    st.title("📅 Quản lý thời khóa biểu")
    st.write("Gán lịch học và phòng học cho các lớp hiện có.")
    if not st.session_state.classes:
        st.warning("Vui lòng thêm lớp học trước!")
        return
    
    with st.form("form_tkb"):
        lop_chon = st.selectbox("Lớp học", [c["Mã Lớp"] for c in st.session_state.classes])
        ngay_hoc = st.text_input("Lịch học (VD: Thứ 2, 4, 6)")
        phong_hoc = st.text_input("Phòng học")
        if st.form_submit_button("Cập nhật TKB"):
            st.success(f"Đã cập nhật TKB cho lớp {lop_chon}: {ngay_hoc} tại {phong_hoc}")

# --- TRANG 4: ĐIỂM DANH ---
def render_diem_danh():
    st.title("✅ Ghi nhận Điểm danh")
    if not st.session_state.students:
        st.warning("Chưa có dữ liệu sinh viên để điểm danh!")
        return

    ngay = st.date_input("Ngày điểm danh")
    lop_chon = st.selectbox("Lọc theo lớp", list(set([s["Lớp"] for s in st.session_state.students])))
    
    sv_trong_lop = [s for s in st.session_state.students if s["Lớp"] == lop_chon]
    
    with st.form("form_diemdanh"):
        ket_qua = {}
        for sv in sv_trong_lop:
            status = st.radio(f"{sv['Mã SV']} - {sv['Họ Tên']}", ["Có mặt", "Vắng phép", "Vắng không phép"], horizontal=True, key=sv['Mã SV'])
            ket_qua[sv['Mã SV']] = status
            
        if st.form_submit_button("Lưu Điểm Danh"):
            for ma_sv, trang_thai in ket_qua.items():
                st.session_state.attendance.append({"Ngày": ngay, "Lớp": lop_chon, "Mã SV": ma_sv, "Trạng thái": trang_thai})
            st.success("Lưu điểm danh thành công!")

# --- TRANG 5: TRA CỨU MSSV ---
def render_tra_cuu():
    st.title("🔍 Tra cứu MSSV")
    tim_kiem = st.text_input("Nhập Mã Sinh Viên cần tra cứu:")
    if st.button("Tìm kiếm"):
        if not tim_kiem:
            st.error("Vui lòng nhập MSSV!")
        else:
            sv_info = next((s for s in st.session_state.students if s["Mã SV"] == tim_kiem), None)
            if sv_info:
                st.subheader(f"Thông tin: {sv_info['Họ Tên']} ({sv_info['Lớp']})")
                lich_su = [a for a in st.session_state.attendance if a["Mã SV"] == tim_kiem]
                if lich_su:
                    st.table(pd.DataFrame(lich_su))
                else:
                    st.info("Sinh viên này chưa có lịch sử điểm danh.")
            else:
                st.error("Không tìm thấy sinh viên!")

# --- TRANG 6: BÁO CÁO THỐNG KÊ ---
def render_bao_cao():
    st.title("📊 Báo cáo thống kê")
    if not st.session_state.attendance:
        st.info("Chưa có dữ liệu điểm danh để thống kê.")
        return
        
    df = pd.DataFrame(st.session_state.attendance)
    st.subheader("Lịch sử điểm danh ")
    st.dataframe(df, use_container_width=True)
    
    st.subheader("Thống kê số lượng theo trạng thái")
    thong_ke = df['Trạng thái'].value_counts()
    st.bar_chart(thong_ke)