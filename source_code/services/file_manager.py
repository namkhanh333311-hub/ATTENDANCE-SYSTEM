"""
Đọc và ghi file.

Các hàm:

load_students()
save_students()

load_classes()
save_classes()

load_attendance()
save_attendance()

load_all_data()
save_all_data()
"""
import os

from models.objects.student import Student
from models.objects.classroom import Classroom
from models.objects.attendance import AttendanceRecord

# Đường dẫn tuyệt đối đến thư mục data/ — luôn đúng dù chạy từ đâu
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

STUDENT_FILE = os.path.join(DATA_DIR, "students.txt")
CLASS_FILE = os.path.join(DATA_DIR, "classes.txt")
ATTENDANCE_FILE = os.path.join(DATA_DIR, "attendance.txt")


def ensure_data_folder():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_students():
    ensure_data_folder()
    if not os.path.exists(STUDENT_FILE):
        return []
    students = []
    with open(STUDENT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    students.append(Student.from_file_string(line))
                except ValueError:
                    pass
    return students


def save_students(students):
    ensure_data_folder()
    with open(STUDENT_FILE, "w", encoding="utf-8") as f:
        for student in students:
            f.write(student.to_file_string())


def load_classes():
    ensure_data_folder()
    if not os.path.exists(CLASS_FILE):
        return []
    classes = []
    with open(CLASS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    classes.append(Classroom.from_file_string(line))
                except ValueError:
                    pass
    return classes


def save_classes(classes):
    ensure_data_folder()
    with open(CLASS_FILE, "w", encoding="utf-8") as f:
        for classroom in classes:
            f.write(classroom.to_file_string())


def load_attendance():
    ensure_data_folder()
    if not os.path.exists(ATTENDANCE_FILE):
        return []
    records = []
    with open(ATTENDANCE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(AttendanceRecord.from_file_line(line))
                except (ValueError, IndexError):
                    pass
    return records


def save_attendance(records):
    ensure_data_folder()
    with open(ATTENDANCE_FILE, "w", encoding="utf-8") as f:
        for record in records:
            f.write(record.to_file_line())


def load_all_data():
    """Đọc toàn bộ dữ liệu từ file, trả về (students, classes, attendance)"""
    students = load_students()
    classes = load_classes()
    attendance = load_attendance()
    return students, classes, attendance


def save_all_data(students, classes, attendance):
    """Ghi toàn bộ dữ liệu xuống file"""
    save_students(students)
    save_classes(classes)
    save_attendance(attendance)
