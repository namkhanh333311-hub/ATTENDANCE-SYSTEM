"""
File chạy chính của chương trình.

Nhiệm vụ:
- Khởi tạo dữ liệu
- Gọi giao diện Streamlit
- Kết nối UI với backend
- Điều hướng các trang
"""
import streamlit as st

from UI.pages import (
    render_quan_ly_lop,
    render_quan_ly_sv,
    render_quan_ly_tkb,
    render_diem_danh,
    render_tra_cuu,
    render_bao_cao
)
from services.file_manager import load_all_data, save_all_data


def init_data():
    """Khởi tạo dữ liệu từ file vào Session State (chỉ chạy lần đầu)"""
    if 'initialized' not in st.session_state:
        students, classes, attendance = load_all_data()
        st.session_state.students = students
        st.session_state.classes = classes
        st.session_state.attendance = attendance
        st.session_state.initialized = True


def main():
    st.set_page_config(
        page_title="Hệ Thống Điểm Danh",
        page_icon="🎓",
        layout="wide"
    )

    init_data()

    st.sidebar.title("📌 Menu Chức Năng")
    menu_options = [
        "1. Quản lý lớp học",
        "2. Quản lý sinh viên",
        "3. Quản lý thời khóa biểu",
        "4. Điểm danh",
        "5. Tra cứu MSSV",
        "6. Báo cáo thống kê"
    ]
    choice = st.sidebar.radio("Vui lòng chọn chức năng:", menu_options)

    st.sidebar.markdown("---")
    if st.sidebar.button("💾 Lưu tất cả dữ liệu"):
        save_all_data(
            st.session_state.students,
            st.session_state.classes,
            st.session_state.attendance
        )
        st.sidebar.success("Đã lưu!")

    st.sidebar.info("Hệ thống quản lý điểm danh v1.0")

    if choice == "1. Quản lý lớp học":
        render_quan_ly_lop()
    elif choice == "2. Quản lý sinh viên":
        render_quan_ly_sv()
    elif choice == "3. Quản lý thời khóa biểu":
        render_quan_ly_tkb()
    elif choice == "4. Điểm danh":
        render_diem_danh()
    elif choice == "5. Tra cứu MSSV":
        render_tra_cuu()
    elif choice == "6. Báo cáo thống kê":
        render_bao_cao()


if __name__ == "__main__":
    main()
