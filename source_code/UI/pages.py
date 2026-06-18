"""
Giao diện Streamlit.

Trang 1: Quản lý lớp học
Trang 2: Quản lý sinh viên
Trang 3: Quản lý thời khóa biểu
Trang 4: Điểm danh
Trang 5: Tra cứu MSSV
Trang 6: Báo cáo thống kê
"""
import streamlit as st
import pandas as pd

from models.objects.student import Student
from models.objects.classroom import Classroom
from models.objects.attendance import AttendanceRecord
from services.file_manager import save_students, save_classes, save_attendance
from services.report import attendance_statistics, absence_statistics, warning_students
from structures.hashtable import HashTable
from algorithms.merge_sort import merge_sort
from algorithms.heap_sort import heap_sort


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _build_student_hashtable():
    """Xây dựng HashTable từ session_state.students để tra cứu nhanh theo MSSV"""
    ht = HashTable()
    for sv in st.session_state.students:
        ht.insert(sv.student_id, sv)
    return ht


def _get_class_ids():
    return [c.class_id for c in st.session_state.classes]


# ─────────────────────────────────────────────
# TRANG 1: QUẢN LÝ LỚP HỌC
# ─────────────────────────────────────────────

def render_quan_ly_lop():
    st.title("🏫 Quản lý lớp học")
    col1, col2 = st.columns([1, 2])

    with col1:
        with st.form("form_lop"):
            ma_lop = st.text_input("Mã lớp (VD: IT01)")
            ten_lop = st.text_input("Tên lớp (VD: Cau Truc Du Lieu)")
            lich_hoc = st.text_input("Lịch học (VD: Thứ 2 - Thứ 4)")
            submitted = st.form_submit_button("Thêm Lớp")

        if submitted:
            if ma_lop and ten_lop:
                # Kiểm tra trùng mã lớp
                if any(c.class_id == ma_lop.strip().upper() for c in st.session_state.classes):
                    st.error(f"Mã lớp {ma_lop.upper()} đã tồn tại!")
                else:
                    new_class = Classroom(ma_lop, ten_lop, lich_hoc)
                    st.session_state.classes.append(new_class)
                    save_classes(st.session_state.classes)
                    st.success(f"Đã thêm lớp {new_class.class_id}!")
                    st.rerun()
            else:
                st.error("Vui lòng nhập Mã lớp và Tên lớp!")

    with col2:
        if st.session_state.classes:
            # Sắp xếp theo mã lớp bằng merge_sort
            sorted_classes = merge_sort(st.session_state.classes, key=lambda c: c.class_id)
            df = pd.DataFrame([c.to_dict() for c in sorted_classes])
            st.dataframe(df, use_container_width=True)

            # Xoá lớp
            st.markdown("---")
            del_id = st.selectbox("Chọn lớp cần xoá", _get_class_ids(), key="del_lop")
            if st.button("🗑️ Xoá lớp"):
                st.session_state.classes = [c for c in st.session_state.classes if c.class_id != del_id]
                save_classes(st.session_state.classes)
                st.success(f"Đã xoá lớp {del_id}!")
                st.rerun()
        else:
            st.info("Chưa có dữ liệu lớp học.")


# ─────────────────────────────────────────────
# TRANG 2: QUẢN LÝ SINH VIÊN
# ─────────────────────────────────────────────

def render_quan_ly_sv():
    st.title("👨‍🎓 Quản lý sinh viên")
    col1, col2 = st.columns([1, 2])

    with col1:
        if not st.session_state.classes:
            st.warning("Vui lòng thêm lớp học trước!")
        else:
            with st.form("form_sv"):
                ma_sv = st.text_input("Mã sinh viên (VD: SV013)")
                ten_sv = st.text_input("Họ và tên")
                lop_chon = st.selectbox("Chọn lớp", _get_class_ids())
                submitted = st.form_submit_button("Thêm Sinh Viên")

            if submitted:
                if ma_sv and ten_sv:
                    ht = _build_student_hashtable()
                    if ht.search(ma_sv.strip().upper()):
                        st.error(f"MSSV {ma_sv.upper()} đã tồn tại!")
                    else:
                        new_sv = Student(ma_sv, ten_sv)
                        st.session_state.students.append(new_sv)
                        # Thêm vào danh sách lớp
                        for c in st.session_state.classes:
                            if c.class_id == lop_chon:
                                c.add_student(new_sv.student_id)
                                break
                        save_students(st.session_state.students)
                        save_classes(st.session_state.classes)
                        st.success(f"Đã thêm {new_sv.full_name} vào lớp {lop_chon}!")
                        st.rerun()
                else:
                    st.error("Vui lòng nhập đủ thông tin!")

    with col2:
        if st.session_state.students:
            # Sắp xếp theo MSSV bằng merge_sort
            sorted_sv = merge_sort(st.session_state.students, key=lambda s: s.student_id)

            # Lọc theo lớp
            filter_lop = st.selectbox("Lọc theo lớp", ["Tất cả"] + _get_class_ids())
            if filter_lop != "Tất cả":
                lop_obj = next((c for c in st.session_state.classes if c.class_id == filter_lop), None)
                if lop_obj:
                    ids_in_class = set(lop_obj.get_all_students())
                    sorted_sv = [s for s in sorted_sv if s.student_id in ids_in_class]

            df = pd.DataFrame([s.to_dict() for s in sorted_sv])
            st.dataframe(df, use_container_width=True)
            st.caption(f"Tổng: {len(sorted_sv)} sinh viên")
        else:
            st.info("Chưa có sinh viên.")


# ─────────────────────────────────────────────
# TRANG 3: QUẢN LÝ THỜI KHÓA BIỂU
# ─────────────────────────────────────────────

def render_quan_ly_tkb():
    st.title("📅 Quản lý thời khóa biểu")

    if not st.session_state.classes:
        st.warning("Vui lòng thêm lớp học trước!")
        return

    with st.form("form_tkb"):
        lop_chon = st.selectbox("Lớp học", _get_class_ids())
        ngay_hoc = st.text_input("Lịch học (VD: Thứ 2, 4, 6)")
        submitted = st.form_submit_button("Cập nhật lịch")

    if submitted:
        for c in st.session_state.classes:
            if c.class_id == lop_chon:
                c.schedule = ngay_hoc.strip()
                break
        save_classes(st.session_state.classes)
        st.success(f"Đã cập nhật lịch lớp {lop_chon}: {ngay_hoc}")

    # Hiển thị TKB hiện tại
    st.markdown("---")
    st.subheader("Thời khóa biểu hiện tại")
    sorted_classes = merge_sort(st.session_state.classes, key=lambda c: c.class_id)
    df = pd.DataFrame([c.to_dict() for c in sorted_classes])
    st.dataframe(df, use_container_width=True)


# ─────────────────────────────────────────────
# TRANG 4: ĐIỂM DANH
# ─────────────────────────────────────────────

def render_diem_danh():
    st.title("✅ Ghi nhận Điểm danh")

    if not st.session_state.classes:
        st.warning("Chưa có lớp học nào!")
        return

    col1, col2 = st.columns([1, 3])
    with col1:
        ngay = st.date_input("Ngày điểm danh")
        lop_chon = st.selectbox("Chọn lớp", _get_class_ids())

    # Lấy danh sách sinh viên trong lớp
    lop_obj = next((c for c in st.session_state.classes if c.class_id == lop_chon), None)
    if not lop_obj or not lop_obj.get_all_students():
        st.info("Lớp này chưa có sinh viên.")
        return

    ht = _build_student_hashtable()
    sv_trong_lop = [ht.search(sid) for sid in lop_obj.get_all_students()]
    sv_trong_lop = [sv for sv in sv_trong_lop if sv is not None]

    # Kiểm tra đã điểm danh buổi này chưa
    ngay_str = str(ngay)
    da_diem_danh = any(
        r.date == ngay_str and r.class_id == lop_chon
        for r in st.session_state.attendance
    )
    if da_diem_danh:
        st.warning(f"Lớp {lop_chon} đã được điểm danh ngày {ngay_str}. Xem lại ở Tra cứu hoặc Báo cáo.")
        return

    with st.form("form_diemdanh"):
        st.subheader(f"Điểm danh lớp {lop_chon} — {ngay_str}")
        ket_qua = {}
        for sv in sv_trong_lop:
            status = st.radio(
                f"{sv.student_id} — {sv.full_name}",
                ["Có mặt", "Vắng phép", "Vắng không phép"],
                horizontal=True,
                key=f"dd_{sv.student_id}"
            )
            ket_qua[sv.student_id] = status

        submitted = st.form_submit_button("💾 Lưu Điểm Danh")

    if submitted:
        for ma_sv, trang_thai in ket_qua.items():
            record = AttendanceRecord(ngay_str, lop_chon, ma_sv, trang_thai)
            st.session_state.attendance.append(record)
        save_attendance(st.session_state.attendance)
        st.success(f"Đã lưu điểm danh {len(ket_qua)} sinh viên lớp {lop_chon}!")
        st.rerun()


# ─────────────────────────────────────────────
# TRANG 5: TRA CỨU MSSV
# ─────────────────────────────────────────────

def render_tra_cuu():
    st.title("🔍 Tra cứu MSSV")

    tim_kiem = st.text_input("Nhập Mã Sinh Viên cần tra cứu:").strip().upper()

    if st.button("Tìm kiếm") or tim_kiem:
        if not tim_kiem:
            st.error("Vui lòng nhập MSSV!")
            return

        # Dùng HashTable để tra cứu O(1)
        ht = _build_student_hashtable()
        sv = ht.search(tim_kiem)

        if not sv:
            st.error(f"Không tìm thấy sinh viên có MSSV: {tim_kiem}")
            return

        # Thông tin sinh viên
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Thông tin sinh viên")
            st.metric("Mã SV", sv.student_id)
            st.metric("Họ tên", sv.full_name)

            # Lớp học của SV
            lop_cua_sv = [c.class_id for c in st.session_state.classes if sv.student_id in c.get_all_students()]
            st.metric("Lớp", ", ".join(lop_cua_sv) if lop_cua_sv else "Chưa có")

        # Lịch sử điểm danh
        lich_su = [r for r in st.session_state.attendance if r.student_id == tim_kiem]

        with col2:
            if lich_su:
                tong = len(lich_su)
                vang = sum(1 for r in lich_su if "Vắng" in r.status)
                co_mat = tong - vang
                ty_le_vang = vang / tong * 100 if tong > 0 else 0

                st.metric("Tổng buổi", tong)
                st.metric("Có mặt", co_mat)
                st.metric("Vắng", vang, delta=f"{ty_le_vang:.1f}%", delta_color="inverse")
                if ty_le_vang > 20:
                    st.error("⚠️ Nguy cơ cấm thi (vắng > 20%)")
            else:
                st.info("Chưa có lịch sử điểm danh.")

        if lich_su:
            st.markdown("---")
            st.subheader("Lịch sử điểm danh")
            sorted_lich_su = merge_sort(lich_su, key=lambda r: r.date)
            df = pd.DataFrame([r.to_dict() for r in sorted_lich_su])
            st.dataframe(df, use_container_width=True)


# ─────────────────────────────────────────────
# TRANG 6: BÁO CÁO THỐNG KÊ
# ─────────────────────────────────────────────

def render_bao_cao():
    st.title("📊 Báo cáo thống kê")

    if not st.session_state.attendance:
        st.info("Chưa có dữ liệu điểm danh để thống kê.")
        return

    # Lọc theo lớp
    lop_filter = st.selectbox("Lọc theo lớp", ["Tất cả"] + _get_class_ids())
    records = st.session_state.attendance
    if lop_filter != "Tất cả":
        records = [r for r in records if r.class_id == lop_filter]

    if not records:
        st.info("Không có dữ liệu cho lớp này.")
        return

    # ── Thống kê tổng quan ──
    col1, col2, col3 = st.columns(3)
    tong = len(records)
    co_mat = sum(1 for r in records if r.status == "Có mặt")
    vang = tong - co_mat
    with col1:
        st.metric("Tổng lượt điểm danh", tong)
    with col2:
        st.metric("Có mặt", co_mat)
    with col3:
        st.metric("Vắng", vang)

    # ── Thống kê theo ngày ──
    st.markdown("---")
    st.subheader("Số lượt có mặt theo ngày")
    thong_ke_ngay = attendance_statistics(records)
    if thong_ke_ngay:
        sorted_dates = merge_sort(list(thong_ke_ngay.items()), key=lambda x: x[0])
        df_ngay = pd.DataFrame(sorted_dates, columns=["Ngày", "Số lượt"])
        st.bar_chart(df_ngay.set_index("Ngày"))

    # ── Thống kê số buổi vắng theo SV ──
    st.markdown("---")
    st.subheader("Số buổi vắng theo sinh viên")
    vang_map = absence_statistics(records)
    if vang_map:
        ht = _build_student_hashtable()
        rows = []
        for sid, count in vang_map.items():
            sv = ht.search(sid)
            ten = sv.full_name if sv else sid
            rows.append({"Mã SV": sid, "Họ Tên": ten, "Số buổi vắng": count})
        rows_sorted = merge_sort(rows, key=lambda x: -x["Số buổi vắng"])
        st.dataframe(pd.DataFrame(rows_sorted), use_container_width=True)

    # ── Top sinh viên vắng nhiều nhất (Heap Sort) ──
    st.markdown("---")
    st.subheader("🔥 Top 5 sinh viên vắng nhiều nhất (Heap Sort)")
    if vang_map:
        ht = _build_student_hashtable()
        heap_input = []
        for sid, count in vang_map.items():
            sv = ht.search(sid)
            ten = sv.full_name if sv else sid
            heap_input.append((count, sid, ten))

        # heap_sort tự cài đặt (dựa trên MaxHeap) trả về danh sách giảm dần theo count
        top_sorted = heap_sort(heap_input)
        top5 = top_sorted[:5]

        rows_top = [
            {"Hạng": i + 1, "Mã SV": sid, "Họ Tên": ten, "Số buổi vắng": count}
            for i, (count, sid, ten) in enumerate(top5)
        ]
        st.dataframe(pd.DataFrame(rows_top), use_container_width=True)
    else:
        st.info("Chưa có dữ liệu vắng để xếp hạng.")

    # ── Danh sách cảnh báo cấm thi ──
    st.markdown("---")
    st.subheader("⚠️ Danh sách sinh viên có nguy cơ cấm thi (vắng > 20%)")

    # Tổng số buổi của từng lớp (trong dữ liệu đang lọc)
    buoi_theo_lop: dict = {}
    for r in records:
        if r.class_id not in buoi_theo_lop:
            buoi_theo_lop[r.class_id] = set()
        buoi_theo_lop[r.class_id].add(r.date)

    # Tổng số buổi của RIÊNG từng sinh viên = tổng buổi của các lớp mà SV đó đang học
    # (không cộng dồn buổi của lớp mà SV không theo học, tránh pha loãng tỷ lệ vắng)
    sessions_per_student = {}
    for sid in vang_map.keys():
        lop_cua_sv = [c.class_id for c in st.session_state.classes if sid in c.get_all_students()]
        sessions_per_student[sid] = sum(
            len(buoi_theo_lop.get(cid, set())) for cid in lop_cua_sv
        )

    warnings = warning_students(records, sessions_per_student)
    if warnings:
        ht = _build_student_hashtable()
        rows_warn = []
        for sid, rate in warnings:
            sv = ht.search(sid)
            ten = sv.full_name if sv else sid
            rows_warn.append({
                "Mã SV": sid,
                "Họ Tên": ten,
                "Tỷ lệ vắng": f"{rate * 100:.1f}%"
            })
        rows_warn_sorted = merge_sort(rows_warn, key=lambda x: -float(x["Tỷ lệ vắng"].replace("%", "")))
        st.error(f"Có {len(rows_warn_sorted)} sinh viên cần cảnh báo!")
        st.dataframe(pd.DataFrame(rows_warn_sorted), use_container_width=True)
    else:
        st.success("Không có sinh viên nào cần cảnh báo.")

    # ── Toàn bộ lịch sử ──
    st.markdown("---")
    st.subheader("Toàn bộ lịch sử điểm danh")
    all_sorted = merge_sort(records, key=lambda r: (r.date, r.class_id))
    df_all = pd.DataFrame([r.to_dict() for r in all_sorted])
    st.dataframe(df_all, use_container_width=True)