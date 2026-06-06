class AttendanceRecord:
    def __init__(self, date: str, class_id: str, student_id: str, status: str):
        self.date = date
        self.class_id = class_id.strip().upper()
        self.student_id = student_id.strip().upper()
        self.status = status  # Các giá trị: "Có mặt", "Vắng phép", "Vắng không phép"

    # --- HỖ TRỢ HIỂN THỊ LÊN GIAO DIỆN STREAMLIT ---
    def to_dict(self):
        """Chuyển Object thành Dictionary để vẽ bảng trên web"""
        return {
            "Ngày": str(self.date), 
            "Lớp": self.class_id, 
            "Mã SV": self.student_id, 
            "Trạng thái": self.status
        }

    # --- HỖ TRỢ ĐỌC/GHI FILE TXT ---
    def to_file_line(self):
        """Đóng gói Object thành 1 dòng chuỗi để ghi xuống file txt"""
        return f"{self.date}|{self.class_id}|{self.student_id}|{self.status}\n"

    @classmethod
    def from_file_line(cls, line: str):
        """Giải nén 1 dòng chuỗi từ file txt để tạo lại Object AttendanceRecord"""
        parts = line.strip().split('|')
        # parts[0]: date, parts[1]: class_id, parts[2]: student_id, parts[3]: status
        return cls(parts[0], parts[1], parts[2], parts[3])