"""
Sinh báo cáo.

Các chức năng:

1. Thống kê sĩ số từng buổi

2. Danh sách sinh viên vắng nhiều nhất

3. Tỷ lệ vắng của từng sinh viên

4. Danh sách sinh viên bị cảnh báo
"""
from services.warning import (
    calculate_absence_rate,
    check_warning
)


def attendance_statistics(records):
    result = {}

    for record in records:
        date = record.date

        result[date] = result.get(date, 0) + 1

    return result


def absence_statistics(records):
    result = {}

    for record in records:
        if "Vắng" in record.status:
            sid = record.student_id
            result[sid] = result.get(sid, 0) + 1

    return result


def warning_students(records, total_sessions):
    absent_map = absence_statistics(records)

    warnings = []

    for sid, absent_count in absent_map.items():
        if check_warning(absent_count, total_sessions):
            warnings.append(
                (
                    sid,
                    calculate_absence_rate(
                        absent_count,
                        total_sessions
                    )
                )
            )

    return warnings