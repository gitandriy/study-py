import tkinter as tk
import csv
import random

from fontTools.merge import timer
from nltk.downloader import update

study_time = 25
break_time = 5
status_is_study = True
remaining_study_time = 0
remaining_break_time = 0
timer_running = True
timer_id = None

def placeholder(name):
    print(f"{name} clicked!")



def quotes2array(filepath):
    quotes = []
    with open(filepath, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            quotes.append(row[0])
    return quotes

quotes = quotes2array("quotes.csv")

root = tk.Tk()
root.title("StudyPy")
root.geometry("800x600")
root.configure(bg='aliceblue')

title_label = tk.Label(
    root,
    text = "StudyPy",
    font = ("Helvetica", 32),
    fg = "gray25",
    bg = "aliceblue"
)



def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    title_label = tk.Label(root, text = "StudyPy", font = ("Helvetica", 32), fg = "gray25", bg = "aliceblue")
    title_label.pack(pady=20)

    button_frame = tk.Frame(root, bg = 'aliceblue')
    button_frame.pack(pady=20)

    button_style = {
        "width": 20,
        "height": 2,
        "font": ("Helvetica", 14),
        "bg": "white",
        "fg": "gray25",
        "activebackground": "gray25",
        "activeforeground": "white",
        "bd": 2
    }

    def show_quote():
        for widget in root.winfo_children():
            widget.destroy()

        quote = random.choice(quotes)

        quote_label = tk.Label(root, text=quote, font=("Helvetica", 18), wraplength=700, justify="center", bg="aliceblue", fg="gray25")
        quote_label.pack(pady=100)

        back_button = tk.Button(root, text="Back", command=show_main_menu, **button_style)
        back_button.pack(pady=20)



    def set_times():
        for widget in root.winfo_children():
            widget.destroy()

        study_time_label = tk.Label(root, text="Study Time:", font=("Helvetica", 18), justify="center", bg="aliceblue", fg="gray25")
        study_time_label.pack(pady=(60,10))

        study_time_entry = tk.Entry(root, font = ("Helvetica", 18), justify="center", fg = "gray25", bg = "aliceblue")
        study_time_entry.pack(pady=0)

        break_time_label = tk.Label(root, text="Break Time:", font=("Helvetica", 18), justify="center", bg="aliceblue",fg="gray25")
        break_time_label.pack(pady=(60, 10))

        break_time_entry = tk.Entry(root, font=("Helvetica", 18), justify="center", fg="gray25", bg="aliceblue")
        break_time_entry.pack(pady=0)

        def save_times():
            global study_time, break_time
            study_time = int(study_time_entry.get())
            break_time = int(break_time_entry.get())
            print(f"Study time entered: {study_time}\nBreak time entered: {break_time}")

        def save_button():
            save_times()
            show_main_menu()

        save_button = tk.Button(root, text="Save", command=save_button, **button_style)
        save_button.pack(pady=50)

        back_button = tk.Button(root, text="Back", command=show_main_menu, **button_style)
        back_button.pack(pady=50)




    def pomodoro():
        global status_is_study, remaining_study_time, remaining_break_time, timer_running, timer_id

        if timer_id is not None: # if timer id exists (from prev pomodoro) delete it
            root.after_cancel(timer_id)
            timer_id = None

        for widget in root.winfo_children():
            widget.destroy()

        remaining_study_time = int(study_time)*60
        remaining_break_time = int(break_time)*60

        mode_label = tk.Label(root, text="Study 🎓" if status_is_study else "Break 😌", font=("Helvetica", 18), justify="center", bg="aliceblue", fg="gray25")
        mode_label.pack(pady=(60, 10))


        pomodoro_time_label = tk.Label(root, text="", font=("Helvetica", 30), justify="center", bg="aliceblue", fg="gray25")
        pomodoro_time_label.pack(pady=(20, 10))

        def update_timer():
            global remaining_study_time, remaining_break_time, status_is_study, timer_id

            if status_is_study:
                if remaining_study_time > 0:
                    minutes = remaining_study_time // 60
                    seconds = remaining_study_time % 60
                    if pomodoro_time_label.winfo_exists():
                        pomodoro_time_label.config(text = f"{minutes:02d}:{seconds:02d}")
                    remaining_study_time -= 1
                    timer_id = root.after(1000, update_timer)
                else:
                    status_is_study = False
                    pomodoro()
            else:
                if remaining_break_time > 0:
                    minutes = remaining_break_time // 60
                    seconds = remaining_break_time % 60
                    pomodoro_time_label.config(text = f"{minutes:02d}:{seconds:02d}")
                    remaining_break_time -= 1
                    timer_id = root.after(1000, update_timer)
                else:
                    status_is_study = True
                    pomodoro()

        def pause_timer():
            global timer_id, timer_running
            root.after_cancel(timer_id)
            timer_running = False

        def resume_timer():
            global timer_running
            if timer_running == False:
                timer_running = True
                update_timer()

        def restart_timer():
            global remaining_study_time, remaining_break_time
            root.after_cancel(timer_id)
            remaining_study_time = study_time * 60
            remaining_break_time = break_time * 60
            update_timer()

        pause_button = tk.Button(root, text="Pause ⏸️", command=pause_timer, **button_style)
        pause_button.pack(pady=20)

        resume_button = tk.Button(root, text="Resume ▶️", command=resume_timer, **button_style)
        resume_button.pack(pady=20)

        restart_button = tk.Button(root, text="Restart 🔄", command=restart_timer, **button_style)
        restart_button.pack(pady=20)

        back_button = tk.Button(root, text="Back", command=show_main_menu, **button_style)
        back_button.pack(pady=40)

        update_timer()

    buttons = [
        ("⛰️ Motivation", show_quote),
        ("🕒 Pomodoro Timer", pomodoro),
        ("⚙️ Set Times", set_times),
        ("☮️ Focus Mode", lambda: placeholder("Focus Mode")),
        ("✅ To-Do List", lambda: placeholder("To-Do List")),
        ("📚 Exams", lambda: placeholder("Exams"))
    ]

    for text, command in buttons:
        b = tk.Button(button_frame, text=text, command=command, **button_style)
        b.pack(pady=5)

show_main_menu()
root.mainloop()