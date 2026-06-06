"""
File chạy chính của chương trình.

Nhiệm vụ:
- Khởi tạo dữ liệu
- Gọi giao diện Streamlit
- Kết nối UI với backend
- Điều hướng các trang
"""
import streamlit as st

# NHIỆM VỤ: Kết nối UI với backend (Nhập các hàm vẽ giao diện từ ui/pages.py)
from ui.pages import (
    render_quan_ly_lop, 
    render_quan_ly_sv, 
    render_quan_ly_tkb, 
    render_diem_danh, 
    render_tra_cuu, 
    render_bao_cao
)
# Thêm import file_manager sau khi xong phần dịch vụ
# from services.file_manager import load_all_data, save_all_data
def init_data():
    """NHIỆM VỤ: Khởi tạo dữ liệu và đưa vào Session State"""
    # gọi hàm load_all_data() từ backend
    # để đọc dữ liệu từ file txt lên thay vì để list rỗng.
    if 'students' not in st.session_state:
        st.session_state.students = [] 
    if 'classes' not in st.session_state:
        st.session_state.classes = []
    if 'attendance' not in st.session_state:
        st.session_state.attendance = []
def main():
    # giao diện Streamlit (Cấu hình cơ bản)
    st.set_page_config(
        page_title="Hệ Thống Điểm Danh", 
        page_icon="🎓", 
        layout="wide"
    )
    # Khởi chạy hàm nạp dữ liệu ban đầu
    init_data()
    # NHIỆM VỤ: Điều hướng các trang (Tạo Sidebar Menu)
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
    st.sidebar.info("Hệ thống quản lý điểm danh v1.0")

    # NHIỆM VỤ: Kết nối UI với điều hướng (Chạy hàm vẽ giao diện tương ứng)
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

# Điểm bắt đầu chương trình của Python
if __name__ == "__main__":
    main()