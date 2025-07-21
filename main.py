import csv
import random
import tkinter as tk

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
img = tk.PhotoImage(file='icon.png')
root.iconphoto(False, img)

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
        timer_running = True
        status_is_study = True
        timer_id = None

        mode_label = tk.Label(root, text="Study 🎓" if status_is_study else "Break 😌", font=("Helvetica", 18), justify="center", bg="aliceblue", fg="gray25")
        mode_label.pack(pady=(60, 10))


        pomodoro_time_label = tk.Label(root, text="", font=("Helvetica", 30), justify="center", bg="aliceblue", fg="gray25")
        pomodoro_time_label.pack(pady=(20, 10))

        def update_timer():
            global remaining_study_time, remaining_break_time, status_is_study, timer_id

            if not timer_running:
                return

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
                    remaining_study_time = study_time * 60
                    remaining_break_time = break_time * 60
                    update_timer()

        def pause_timer():
            global timer_running, timer_id
            timer_running = False
            if timer_id is not None:
                root.after_cancel(timer_id)
                timer_id = None

        def resume_timer():
            global timer_running, timer_id
            if not timer_running:
                timer_running = True
                if timer_id is None:
                    update_timer()

        def restart_timer():
            global timer_running, timer_id, remaining_break_time, remaining_study_time, status_is_study
            if timer_id != None:
                root.after_cancel(timer_id)
                timer_id = None
            remaining_study_time = study_time * 60
            remaining_break_time = break_time * 60
            status_is_study = True
            mode_label.config(text="Study 🎓")
            timer_running = True
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

    def to_do_list():
        for widget in root.winfo_children():
            widget.destroy()

        to_do_label = tk.Label(root, text="Enter a New Task:", font=("Helvetica", 18), justify="center", bg="aliceblue", fg="gray25")
        to_do_label.pack(pady=(20, 10))

        to_do_entry = tk.Entry(root, font=("Helvetica", 18), justify="center", fg="gray25", bg="aliceblue")
        to_do_entry.pack(pady=(0, 20))


        listbox_frame = tk.Frame(root, bg="aliceblue")
        listbox_frame.pack(pady=10, fill="both", expand=True)


        pending_frame = tk.Frame(listbox_frame, bg="aliceblue")
        pending_frame.pack(side=tk.LEFT, padx=20, fill="both", expand=True)

        pending_label = tk.Label(pending_frame, text="Pending Tasks", font=("Helvetica", 16), bg="aliceblue", fg="gray25")
        pending_label.pack()

        pending_listbox = tk.Listbox(pending_frame, font=("Helvetica", 14), fg="gray25", bg="white", selectmode=tk.MULTIPLE)
        pending_listbox.pack(fill="both", expand=True, pady=(5, 0))


        completed_frame = tk.Frame(listbox_frame, bg="aliceblue")
        completed_frame.pack(side=tk.LEFT, padx=20, fill="both", expand=True)

        completed_label = tk.Label(completed_frame, text="Completed Tasks", font=("Helvetica", 16), bg="aliceblue", fg="gray25")
        completed_label.pack()

        completed_listbox = tk.Listbox(completed_frame, font=("Helvetica", 14), fg="gray25", bg="white", selectmode=tk.MULTIPLE)
        completed_listbox.pack(fill="both", expand=True, pady=(5, 0))

        def load_tasks():
            pending_listbox.delete(0, tk.END)
            completed_listbox.delete(0, tk.END)

            to_do_array = []
            with open("todo.csv", mode="r") as csv_file:
                reader = csv.reader(csv_file)
                for task, status in reader:
                    if status == "True":
                        completed_listbox.insert(tk.END, task)
                    else:
                        pending_listbox.insert(tk.END, task)
                print(to_do_array)

        def add_task(event = None):
            task_text = to_do_entry.get()
            if task_text.strip() == "":
                return

            with open("todo.csv", mode="a", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([task_text, "False"])

            to_do_entry.delete(0, tk.END)
            load_tasks()

        def complete_task():

            selected_indices = pending_listbox.curselection() # array of indices (position of tasks in list that have been selected)
            if not selected_indices: # if no tasks selected, return
                return

            selected_tasks = [pending_listbox.get(i) for i in selected_indices] # makes array with each task that has been selected using the indices of curselection

            updated_tasks = []

            with open("todo.csv", mode="r") as csv_file:
                reader = csv.reader(csv_file)
                for task, status in reader:
                    if task in selected_tasks and status == "False":
                        updated_tasks.append([task, "True"])
                    else:
                        updated_tasks.append([task, status])

            with open("todo.csv", mode="w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(updated_tasks)

            load_tasks()

        def delete_task(event=None):

            selected_tasks = [] # tasks to delete

            for i in pending_listbox.curselection():
                task = pending_listbox.get(i)
                selected_tasks.append((task, "False"))

            for i in completed_listbox.curselection():
                task = completed_listbox.get(i)
                selected_tasks.append((task, "True"))

            updated_tasks = [] # tasks to keep

            with open("todo.csv", mode="r") as csv_file:
                reader = csv.reader(csv_file)
                for task, status in reader:
                    if (task, status) not in selected_tasks:
                        updated_tasks.append([task, status]) # updated_tasks only contains the tasks that were unselected to be deleted

            with open("todo.csv", mode="w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(updated_tasks) # rewrites the file, only including tasks that were NOT selected to be deleted

            load_tasks()




        to_do_entry.bind("<Return>", add_task)

        pending_listbox.bind("<Delete>", delete_task)
        pending_listbox.bind("<BackSpace>", delete_task)
        completed_listbox.bind("<Delete>", delete_task)
        completed_listbox.bind("<BackSpace>", delete_task)

        add_task_button = tk.Button(root, text="Add Task", command=add_task, **button_style)
        add_task_button.pack(pady=20)

        complete_button = tk.Button(root, text="Complete Task", command=complete_task, **button_style)
        complete_button.pack(pady=0)

        back_button = tk.Button(root, text="Back", command=show_main_menu, **button_style)
        back_button.pack(pady=0)

        load_tasks()







    buttons = [
        ("⛰️ Motivation", show_quote),
        ("🕒 Pomodoro Timer", pomodoro),
        ("⚙️ Set Times", set_times),
        ("☮️ Focus Mode", lambda: placeholder("Focus Mode")),
        ("✅ To-Do List", to_do_list),
        ("📚 Exams", lambda: placeholder("Exams"))
    ]

    for text, command in buttons:
        b = tk.Button(button_frame, text=text, command=command, **button_style)
        b.pack(pady=5)

show_main_menu()
root.mainloop()