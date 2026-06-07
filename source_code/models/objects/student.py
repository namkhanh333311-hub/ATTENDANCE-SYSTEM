"""
Lớp Student.

Thuộc tính:
- student_id
- full_name

Chức năng:
- Tạo đối tượng sinh viên
- Chuyển đối tượng thành chuỗi để lưu file
- Đọc dữ liệu từ file
"""
class Student:
    def __init__(self, student_id: str, full_name: str):
        # Tạo đối tượng sinh viên với 2 thuộc tính được yêu cầu
        self.student_id = student_id.strip().upper()
        self.full_name = full_name.strip().title()

    def to_file_string(self) -> str:
        """
        Chuyển đối tượng thành chuỗi để lưu file.
        Dữ liệu được ngăn cách bởi dấu gạch đứng '|' kèm ký tự xuống dòng.
        """
        return f"{self.student_id}|{self.full_name}\n"

    @classmethod
    def from_file_string(cls, line: str):
        """
        Đọc dữ liệu từ file (nhận vào 1 dòng chuỗi) và tái tạo lại đối tượng Student.
        """
        parts = line.strip().split('|')
        if len(parts) >= 2:
            # parts[0] là mã SV, parts[1] là họ tên
            return cls(parts[0], parts[1])
        raise ValueError(f"Dòng dữ liệu không hợp lệ: {line}")

    # --- Hàm bổ trợ cho giao diện Streamlit ---
    def to_dict(self):
        """Chuyển đối tượng thành Dictionary để render bảng trên UI"""
        return {"Mã SV": self.student_id, "Họ Tên": self.full_name}

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"