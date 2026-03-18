from datetime import datetime as dt

nick = [1155123456, "Nick Wilde", 28, 3.86, "19/08/2025 08:03:54 AM"]
judy = [1155987543, "Judy Hopps", 37, 2.95, "07/12/2025 10:08:33 PM"]
gary = [1155654321, "Gary De'Snake", 42, 3.56, "23/01/2026 11:40:01 PM"]
flash = [1155998877, "Flash Slothmore", 24, 3.12, "01/01/2026 09:06:36 AM"]

TOTAL_CREDITS = 52
students = [nick, judy, gary, flash]

print(
    f"{'Student ID':<10} | {'Full Name':<15} | "
    f"{'Credits':<7} | {'GPA':<4} | "
    f"{'Progress %':<10} | {'Last Access':<17}"
)

for n in students:
    sid, name, credits, gpa, time = n
    time_obj = dt.strptime(time, "%d/%m/%Y %I:%M:%S %p")
    progress = credits / TOTAL_CREDITS * 100
    print(
        f"{sid:<10} | {name:<15} | {credits:<7} |"
        f"{gpa:<4.2f} | {progress:>9.2f}% | {time_obj:%m/%d/%y %H:%M:%S}"
    )
