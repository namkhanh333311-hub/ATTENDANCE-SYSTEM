"""
Kiểm tra sinh viên có nguy cơ cấm thi.

Công thức:

absence_rate =
absent_sessions /
total_sessions

Nếu > 20%
=> cảnh báo

Hàm:

calculate_absence_rate()

check_warning()
"""
def calculate_absence_rate(absent_sessions, total_sessions):
    if total_sessions == 0:
        return 0

    return absent_sessions / total_sessions


def check_warning(absent_sessions, total_sessions):
    rate = calculate_absence_rate(
        absent_sessions,
        total_sessions
    )

    return rate > 0.2