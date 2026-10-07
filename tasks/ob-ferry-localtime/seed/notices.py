from timetable import local_departure


def board_line(port, utc_time, vessel):
    return f"{vessel:<14} {local_departure(utc_time, port):%H:%M}  {port}"
