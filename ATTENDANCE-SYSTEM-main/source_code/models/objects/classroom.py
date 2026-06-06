"""
Lớp Classroom.

Thuộc tính:
- class_id
- class_name
- schedule

Chức năng:
- Lưu thông tin lớp học
- Quản lý danh sách sinh viên của lớp
"""
def __init__(self, class_id: str, class_name: str, schedule: str):
        # 1. Các thuộc tính được yêu cầu
        self.class_id = class_id.strip().upper()
        self.class_name = class_name.strip()
        self.schedule = schedule.strip()
        
        # Danh sách chứa mã sinh viên thuộc lớp này
        self.student_ids = [] 

    # --- CHỨC NĂNG 1: Quản lý danh sách sinh viên của lớp ---
    
    def add_student(self, student_id: str):
        """Thêm một sinh viên vào danh sách lớp"""
        student_id = student_id.strip().upper()
        if student_id not in self.student_ids:
            self.student_ids.append(student_id)

    def remove_student(self, student_id: str):
        """Xóa một sinh viên khỏi danh sách lớp"""
        student_id = student_id.strip().upper()
        if student_id in self.student_ids:
            self.student_ids.remove(student_id)
            
    def get_all_students(self) -> list:
        """Lấy toàn bộ danh sách mã sinh viên trong lớp"""
        return self.student_ids

    # --- CHỨC NĂNG 2: Lưu thông tin lớp học (và đọc từ file) ---
    
    def to_file_string(self) -> str:
        """
        Chuyển thông tin lớp thành chuỗi để lưu file.
        Danh sách sinh viên được nối với nhau bằng dấu phẩy.
        Định dạng: class_id|class_name|schedule|sv01,sv02,sv03
        """
        students_str = ",".join(self.student_ids)
        return f"{self.class_id}|{self.class_name}|{self.schedule}|{students_str}\n"

    @classmethod
    def from_file_string(cls, line: str):
        """
        Tái tạo đối tượng Classroom từ chuỗi đọc được trong file.
        """
        parts = line.strip().split('|')
        if len(parts) >= 3:
            # Tạo đối tượng lớp ban đầu
            classroom = cls(parts[0], parts[1], parts[2])
            
            # Nếu lớp đã có sinh viên (phần tử thứ 4 tồn tại và không rỗng)
            if len(parts) == 4 and parts[3]:
                student_list = parts[3].split(',')
                for sv_id in student_list:
                    classroom.add_student(sv_id)
                    
            return classroom
            
        raise ValueError(f"Dòng dữ liệu không hợp lệ: {line}")

    # --- Hàm bổ trợ cho giao diện Streamlit ---
    def to_dict(self):
        """Chuyển đổi thành Dictionary để Streamlit hiển thị lên bảng"""
        return {
            "Mã Lớp": self.class_id,
            "Tên Lớp": self.class_name,
            "Lịch Học": self.schedule,
            "Sĩ Số": len(self.student_ids)
        }