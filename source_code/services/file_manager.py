"""
Đọc và ghi file.

Các hàm:

load_students()
save_students()

load_classes()
save_classes()

load_attendance()
save_attendance()
"""
import os

DATA_DIR = "data"

STUDENT_FILE = os.path.join(DATA_DIR, "students.txt")
CLASS_FILE = os.path.join(DATA_DIR, "classes.txt")
ATTENDANCE_FILE = os.path.join(DATA_DIR, "attendance.txt")


def ensure_data_folder():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_students():
    ensure_data_folder()

    if not os.path.exists(STUDENT_FILE):
        return []

    with open(STUDENT_FILE, "r", encoding="utf-8") as f:
        return f.readlines()


def save_students(students):
    ensure_data_folder()

    with open(STUDENT_FILE, "w", encoding="utf-8") as f:
        for student in students:
            f.write(student.to_file_string())


def load_classes():
    ensure_data_folder()

    if not os.path.exists(CLASS_FILE):
        return []

    with open(CLASS_FILE, "r", encoding="utf-8") as f:
        return f.readlines()


def save_classes(classes):
    ensure_data_folder()

    with open(CLASS_FILE, "w", encoding="utf-8") as f:
        for classroom in classes:
            f.write(classroom.to_file_string())


def load_attendance():
    ensure_data_folder()

    if not os.path.exists(ATTENDANCE_FILE):
        return []

    with open(ATTENDANCE_FILE, "r", encoding="utf-8") as f:
        return f.readlines()


def save_attendance(records):
    ensure_data_folder()

    with open(ATTENDANCE_FILE, "w", encoding="utf-8") as f:
        for record in records:
            f.write(record.to_file_line())