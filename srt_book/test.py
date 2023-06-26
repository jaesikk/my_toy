import os
import tkinter as tk

# 입력값을 파일에 저장하는 함수
def save_input_values(id, pw, nm, start, end, yyyymmdd, t, num_trains_to_check):
    with open("input_values.txt", "w") as file:
        file.write(f"ID: {id}\n")
        file.write(f"Password: {pw}\n")
        file.write(f"Name: {nm}\n")
        file.write(f"Start: {start}\n")
        file.write(f"End: {end}\n")
        file.write(f"Date: {yyyymmdd}\n")
        file.write(f"Time: {t}\n")
        file.write(f"Number of trains to check: {num_trains_to_check}\n")
    print("Input values saved successfully.")

# 파일에서 입력값을 읽어오는 함수
def load_input_values():
    input_values = {}
    with open("input_values.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.strip().split(": ")
            input_values[key] = value
    return input_values

# Submit 버튼 클릭 시 실행되는 함수
def submit_callback():
    global n
    # 입력값 받기
    id = id_entry.get()
    pw = pw_entry.get()
    nm = nm_entry.get()
    start = start_entry.get()
    end = end_entry.get()
    yyyymmdd = yyyymmdd_entry.get()
    t = t_entry.get()
    num_trains_to_check = num_trains_to_check_entry.get()

    # 입력값 저장
    save_input_values(id, pw, nm, start, end, yyyymmdd, t, num_trains_to_check)

    # 파일에서 입력값 읽어오기
    input_values = load_input_values()

    # 결과 텍스트 업데이트
    result_text.configure(state='normal')
    result_text.delete('1.0', tk.END)
    n +=1
    result_text.insert(tk.END, f'{n}번째 log입니다.\n')
    for key, value in input_values.items():
        result_text.insert(tk.END, f"{key}: {value}\n")
    result_text.configure(state='disabled')

n = 0
# tkinter 윈도우 생성
window = tk.Tk()
window.title("Input Values")

# 입력값을 불러오기 위해 파일에서 입력값 읽어오기
input_values = load_input_values()

# ID 입력 필드
id_label = tk.Label(window, text="ID:")
id_label.pack()
id_entry = tk.Entry(window)
id_entry.insert(tk.END, input_values.get("ID", ""))  # 이전 값이 있으면 입력 창에 표시
id_entry.pack()

# Password 입력 필드
pw_label = tk.Label(window, text="Password:")
pw_label.pack()
pw_entry = tk.Entry(window)
pw_entry.insert(tk.END, input_values.get("Password", ""))
pw_entry.pack()

# Name 입력 필드
nm_label = tk.Label(window, text="Name:")
nm_label.pack()
nm_entry = tk.Entry(window)
nm_entry.insert(tk.END, input_values.get("Name", ""))
nm_entry.pack()

# Start 입력 필드
start_label = tk.Label(window, text="Start:")
start_label.pack()
start_entry = tk.Entry(window)
start_entry.insert(tk.END, input_values.get("Start", ""))
start_entry.pack()

# End 입력 필드
end_label = tk.Label(window, text="End:")
end_label.pack()
end_entry = tk.Entry(window)
end_entry.insert(tk.END, input_values.get("End", ""))
end_entry.pack()

# Date 입력 필드
yyyymmdd_label = tk.Label(window, text="Date (YYYYMMDD):")
yyyymmdd_label.pack()
yyyymmdd_entry = tk.Entry(window)
yyyymmdd_entry.insert(tk.END, input_values.get("Date", ""))
yyyymmdd_entry.pack()

# Time 입력 필드
t_label = tk.Label(window, text="Time (even number):")
t_label.pack()
t_entry = tk.Entry(window)
t_entry.insert(tk.END, input_values.get("Time", ""))
t_entry.pack()

# Number of trains to check 입력 필드
num_trains_to_check_label = tk.Label(window, text="Number of trains to check:")
num_trains_to_check_label.pack()
num_trains_to_check_entry = tk.Entry(window)
num_trains_to_check_entry.insert(tk.END, input_values.get("Number of trains to check", ""))
num_trains_to_check_entry.pack()

# Submit 버튼
submit_button = tk.Button(window, text="Submit", command=submit_callback)
submit_button.pack()

# 결과 텍스트 박스
result_text = tk.Text(window, height=10, width=50)
result_text.configure(state='disabled')
result_text.pack()

# 이벤트 루프 실행
window.mainloop()


######################################################################
# import tkinter as tk
#
# def submit_callback():
#     recent_value = entry.get()
#     print("Submit 버튼이 눌렸습니다.")
#     print("가장 최근 값:", recent_value)
#
#     # 최근 값을 파일에 저장
#     with open("recent_value.txt", "w") as file:
#         file.write(recent_value)
#
#     print("__main__ 블록 :: 검색이 실행됩니다.")
#
# def read_recent_value():
#     # 파일에서 최근 값을 읽어옴
#     with open("recent_value.txt", "r") as file:
#         recent_value = file.read()
#     print("파일에서 읽어온 최근 값:", recent_value)
#
# # tkinter 윈도우 생성
# window = tk.Tk()
#
# # 입력 필드 생성
# entry = tk.Entry(window)
# entry.pack()
#
# # submit 버튼 생성
# submit_button = tk.Button(window, text="Submit", command=submit_callback)
# submit_button.pack()
#
# # 파일에서 최근 값을 읽어오는 예시
# read_value_button = tk.Button(window, text="파일에서 최근 값 읽기", command=read_recent_value)
# read_value_button.pack()
#
# # 이벤트 루프 실행
# window.mainloop()