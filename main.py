import csv
import random
import tkinter as tk
import ctypes
import os
import platform
import sys
from datetime import datetime, timedelta


import subprocess

def flush_dns(): # fixing host file not synced with browser results
    try:
        system = platform.system().lower()
        if system == "windows":
            subprocess.run(['ipconfig', '/flushdns'], capture_output=True, check=True)
        elif system == "darwin":
            subprocess.run(['sudo', 'dscacheutil', '-flushcache'], capture_output=True, check=True)
        elif system == "linux":
            try:
                subprocess.run(['sudo', 'systemctl', 'restart', 'systemd-resolved'], capture_output=True, check=True)
            except:
                try:
                    subprocess.run(['sudo', 'service', 'network-manager', 'restart'], capture_output=True, check=True)
                except:
                    pass
        return True
    except:
        return False

def is_admin():
    try:
        if platform.system().lower() == "windows":
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.getuid() == 0
    except:
        return False

def run_as_admin():
    if platform.system().lower() == "windows":
        if not is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
            print("Please run as admin for website blocking functionality.")

run_as_admin()

# stats variables
global total_time_studied, total_days, current_day_streak, longest_streak

total_time_studied = 0
total_days = 0
current_day_streak = 0
longest_streak = 0


study_time = 25
break_time = 5
status_is_study = True
remaining_study_time = 0
remaining_break_time = 0
timer_running = True
timer_id = None
isDarkMode = False
themecolour = "aliceblue"
text_colour = "gray25"

with open("stats.csv", mode='r', newline='') as file: # write updated variables back to csv once program closed

    csv_reader = list(csv.reader(file)) # gets stats values as array
    total_time_studied = int(csv_reader[1][0])
    total_days = int(csv_reader[1][1])
    current_day_streak = int(csv_reader[1][2])
    longest_streak = int(csv_reader[1][3])
    last_study_date = csv_reader[1][4]


print(f"Total Time Studied: {total_time_studied}\nTotal Days: {total_days}\nCurrent Day Streak: {current_day_streak}\nLongest Streak: {longest_streak}\nLast Study Date: {last_study_date}")

def placeholder(name):
    print(f"{name} clicked!")

def toggle_theme():
    global isDarkMode, themecolour, StudyPyColour, text_colour
    if isDarkMode:
        isDarkMode = False
        themecolour = "aliceblue"
        text_colour = "gray25"
    else:
        isDarkMode = True
        themecolour = "LightSteelBlue4"
        text_colour = "white"

    root.configure(bg = themecolour)
    show_main_menu()

def quotes2array(filepath):
    quotes = []
    with open(filepath, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            quotes.append(row[0])
    return quotes

quotes = quotes2array("quotes.csv")

def get_hosts_path():
    system = platform.system().lower()
    if system == "windows":
        return r'C:\Windows\System32\drivers\etc\hosts'
    else:
        return '/etc/hosts'

def unblock_sites():
    if not is_admin():
        return False

    hosts_path = get_hosts_path()

    try:
        with open(hosts_path, 'r') as file:
            lines = file.readlines()

        with open(hosts_path, 'w') as file:
            inside_block = False
            for line in lines:
                if '# StudyPy Block START' in line.strip():
                    inside_block = True
                    continue
                elif '# StudyPy Block END' in line.strip():
                    inside_block = False
                    continue

                if inside_block:
                    continue

                file.write(line)

            if os.path.exists("focus_lock.tmp"):
                os.remove("focus_lock.tmp")

        flush_dns()
        return True
    except:
        return False





unblock_sites()

root = tk.Tk()
root.title("StudyPy")
root.geometry("800x600")
root.configure(bg=themecolour)
img = tk.PhotoImage(file='icon.png')
root.iconphoto(False, img)

def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        root,
        text="StudyPy",
        font=("Helvetica", 32),
        fg="gray25" if not isDarkMode else "white",
        bg=themecolour
    )
    title_label.pack(pady=20)

    button_frame = tk.Frame(root, bg = themecolour)
    button_frame.pack(pady=20)

    button_style = {
        "width": 20,
        "height": 2,
        "font": ("Helvetica", 14),
        "bg": "white" if not isDarkMode else "gray35",
        "fg": "gray25" if not isDarkMode else "white",
        "activebackground": "gray35" if not isDarkMode else "white",
        "activeforeground": "white" if not isDarkMode else "gray25",
        "bd": 2
    }

    def show_quote():
        for widget in root.winfo_children():
            widget.destroy()

        quote = random.choice(quotes)

        quote_label = tk.Label(root, text=quote, font=("Helvetica", 18), wraplength=700, justify="center", bg=themecolour, fg=text_colour)
        quote_label.pack(pady=100)

        back_button = tk.Button(root, text="Back", command=show_main_menu, **button_style)
        back_button.pack(pady=20)



    def set_times():
        for widget in root.winfo_children():
            widget.destroy()

        study_time_label = tk.Label(root, text="Study Time:", font=("Helvetica", 18), justify="center", bg=themecolour, fg=text_colour)
        study_time_label.pack(pady=(60,10))

        study_time_entry = tk.Entry(root, font = ("Helvetica", 18), justify="center", fg = text_colour, bg = themecolour)
        study_time_entry.pack(pady=0)

        break_time_label = tk.Label(root, text="Break Time:", font=("Helvetica", 18), justify="center", bg=themecolour,fg=text_colour)
        break_time_label.pack(pady=(60, 10))

        break_time_entry = tk.Entry(root, font=("Helvetica", 18), justify="center", fg=text_colour, bg=themecolour)
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
        global study_time, status_is_study, remaining_study_time, remaining_break_time, timer_running, timer_id

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

        mode_label = tk.Label(root, text="Study 🎓" if status_is_study else "Break 😌", font=("Helvetica", 18), justify="center", bg=themecolour, fg=text_colour)
        mode_label.pack(pady=(60, 10))


        pomodoro_time_label = tk.Label(root, text="", font=("Helvetica", 30), justify="center", bg=themecolour, fg=text_colour)
        pomodoro_time_label.pack(pady=(20, 10))

        def update_timer():
            global remaining_study_time, remaining_break_time, status_is_study, timer_id, last_study_date, total_time_studied, total_days, current_day_streak, longest_streak

            if not timer_running:
                return

            if status_is_study:

                if remaining_study_time == study_time * 60: # start call
                    block_sites()

                if remaining_study_time > 0:
                    minutes = remaining_study_time // 60
                    seconds = remaining_study_time % 60
                    if pomodoro_time_label.winfo_exists():
                        pomodoro_time_label.config(text = f"{minutes:02d}:{seconds:02d}")
                    remaining_study_time -= 1
                    timer_id = root.after(1000, update_timer)
                else:

                    total_time_studied += study_time # add study time to stats
                    last_study_date_obj = datetime.strptime(last_study_date, "%Y-%m-%d").date() # convert str date from csv to date object for comparison
                    today = datetime.today().date()
                    if last_study_date_obj < today:
                        total_days += 1

                        if today == last_study_date_obj + timedelta(days = 1):
                            current_day_streak += 1
                        else:
                            current_day_streak = 1 # resets to 1 as they studied today if they reach here

                        if current_day_streak > longest_streak:
                            longest_streak = current_day_streak

                        last_study_date = today.strftime('%Y-%m-%d')

                    unblock_sites()
                    status_is_study = False
                    mode_label.config(text="Break 😌")
                    remaining_break_time = break_time * 60
                    timer_id = root.after(1000, update_timer)
            else:
                if remaining_break_time > 0:
                    minutes = remaining_break_time // 60
                    seconds = remaining_break_time % 60
                    if pomodoro_time_label.winfo_exists():
                        pomodoro_time_label.config(text=f"{minutes:02d}:{seconds:02d}")
                    remaining_break_time -= 1
                    timer_id = root.after(1000, update_timer)
                else:
                    status_is_study = True
                    remaining_study_time = study_time * 60
                    remaining_break_time = break_time * 60
                    mode_label.config(text="Study 🎓")
                    timer_id = root.after(1000, update_timer)

        def pause_timer():
            global timer_running, timer_id
            timer_running = False
            unblock_sites()
            if timer_id is not None:
                root.after_cancel(timer_id)
                timer_id = None

        def resume_timer():
            global timer_running, timer_id
            if not timer_running:
                timer_running = True
                if status_is_study:
                    block_sites()
                if timer_id is None:
                    update_timer()

        def restart_timer():
            global timer_running, timer_id, remaining_break_time, remaining_study_time, status_is_study
            unblock_sites()
            if timer_id != None:
                root.after_cancel(timer_id)
                timer_id = None
            remaining_study_time = study_time * 60
            remaining_break_time = break_time * 60
            status_is_study = True
            mode_label.config(text="Study 🎓")
            timer_running = True
            update_timer()

        def save_partial_study_time(): # saves study time even if the session closes before study time finished
            global total_time_studied, status_is_study, remaining_study_time, study_time, time_studied_seconds, last_study_date, total_days, current_day_streak, longest_streak

            if status_is_study and remaining_study_time < study_time * 60:
                time_studied_seconds = study_time * 60 - remaining_study_time
                total_time_studied += round(time_studied_seconds / 60) # rounds to the closest minute

            last_study_date_obj = datetime.strptime(last_study_date, "%Y-%m-%d").date()
            today = datetime.today().date()

            if last_study_date_obj < today:
                total_days += 1

                if today == last_study_date_obj + timedelta(days=1):
                    current_day_streak += 1
                else:
                    current_day_streak = 1  # resets to 1 as they studied today if they reach here

                if current_day_streak > longest_streak:
                    longest_streak = current_day_streak

                last_study_date = today.strftime('%Y-%m-%d')


        pause_button = tk.Button(root, text="Pause ⏸️", command=pause_timer, **button_style)
        pause_button.pack(pady=20)

        resume_button = tk.Button(root, text="Resume ▶️", command=resume_timer, **button_style)
        resume_button.pack(pady=20)

        restart_button = tk.Button(root, text="Restart 🔄", command=restart_timer, **button_style)
        restart_button.pack(pady=20)

        back_button = tk.Button(root, text="Back", command=lambda: [show_main_menu(), unblock_sites(), save_partial_study_time()], **button_style)
        back_button.pack(pady=40)

        update_timer()

    def to_do_list():
        for widget in root.winfo_children():
            widget.destroy()

        to_do_label = tk.Label(root, text="Enter a New Task:", font=("Helvetica", 18), justify="center", bg=themecolour, fg=text_colour)
        to_do_label.pack(pady=(20, 10))

        to_do_entry = tk.Entry(root, font=("Helvetica", 18), justify="center", fg=text_colour, bg=themecolour)
        to_do_entry.pack(pady=(0, 20))


        listbox_frame = tk.Frame(root, bg=themecolour)
        listbox_frame.pack(pady=10, fill="both", expand=True)


        pending_frame = tk.Frame(listbox_frame, bg=themecolour)
        pending_frame.pack(side=tk.LEFT, padx=20, fill="both", expand=True)

        pending_label = tk.Label(pending_frame, text="Pending Tasks", font=("Helvetica", 16), bg=themecolour, fg=text_colour)
        pending_label.pack()

        pending_listbox = tk.Listbox(pending_frame, font=("Helvetica", 14), fg="gray25", bg="white", selectmode=tk.MULTIPLE)
        pending_listbox.pack(fill="both", expand=True, pady=(5, 0))


        completed_frame = tk.Frame(listbox_frame, bg=themecolour)
        completed_frame.pack(side=tk.LEFT, padx=20, fill="both", expand=True)

        completed_label = tk.Label(completed_frame, text="Completed Tasks", font=("Helvetica", 16), bg=themecolour, fg=text_colour)
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

    def focus_mode():
        for widget in root.winfo_children():
            widget.destroy()

        focus_mode_label = tk.Label(root, text="Focus Settings", font=("Helvetica", 18), justify="center", bg=themecolour, fg=text_colour)
        focus_mode_label.pack(pady=20)

        website_entry = tk.Entry(root, font=("Helvetica", 18), justify="center", fg=text_colour, bg=themecolour)
        website_entry.pack(pady=0)

        website_listbox = tk.Listbox(root, font=("Helvetica", 14), fg="gray25", bg="white", width = 40)
        website_listbox.pack(pady=10)

        def load_blocked_sites():
            website_listbox.delete(0, tk.END)
            try:
                with open('blocked_sites.csv', 'r') as file:
                    for row in csv.reader(file):
                        website_listbox.insert(tk.END, row[0])
            except FileNotFoundError:
                pass


        def add_website():
            website = website_entry.get().strip()
            if website:
                # check if website already exists
                with open('blocked_sites.csv', 'r') as file:
                    if any(website == row[0].strip() for row in csv.reader(file)):
                        website_entry.delete(0, tk.END)
                        return

                with open('blocked_sites.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([website])
                website_entry.delete(0, tk.END)

                if os.path.exists("focus_lock.tmp"):
                    unblock_sites()
                    block_sites()

                load_blocked_sites()

        def remove_website():
            selected = website_listbox.curselection()
            if not selected:
                return
            websites = website_listbox.get(0, tk.END)
            updated = []
            for i in range(len(websites)): # only writes back those that are NOT selected
                if i not in selected:
                    updated.append(websites[i])
            with open('blocked_sites.csv', 'w', newline='') as file:
                writer = csv.writer(file)

                if os.path.exists("focus_lock.tmp"):
                    unblock_sites()
                    block_sites()

                for site in updated:
                    writer.writerow([site])
            load_blocked_sites()


        #buttons
        add_button = tk.Button(root, text="Add Website", command=add_website, **button_style)
        add_button.pack(pady=5)

        remove_button = tk.Button(root, text="Remove Selected", command=remove_website, **button_style)
        remove_button.pack(pady=5)

        back_button = tk.Button(root, text="Back", command=show_main_menu, **button_style)
        back_button.pack(pady=20)

        load_blocked_sites()

    def block_sites():
        print("--- debugging block_sites ---")

        if not is_admin():
            print("error: requires admin priveleges")
            return False
        print("✓ Admin Priveleges")

        # check if CSV exists
        if not os.path.exists('blocked_sites.csv'):
            print("blocked_sites.csv NOT FOUND")
            return False
        print("✓ blocked_sites.csv exists")

        try:
            with open('blocked_sites.csv', 'r') as file:
                content = file.read()
                print(f"CSV content: '{content}'")

            with open('blocked_sites.csv', 'r') as file:
                websites = [row[0].strip() for row in csv.reader(file) if row and row[0].strip()]
                print(f"parsed websites: {websites}")

            if not websites:
                print("error: no websites to block in csv ")
                return False

        except Exception as e:
            print(f"ERROR reading CSV: {e}")
            return False

        hosts_path = get_hosts_path()
        print(f"hosts path: {hosts_path}")

        with open(hosts_path, 'r') as file:
            content = file.read()
            if "# StudyPy Block START" in content:
                print("sites already blocked - removing first")
                unblock_sites()

        # try to write to hosts
        try:
            with open(hosts_path, 'a') as hosts_file:
                hosts_file.write('\n# StudyPy Block START\n')
                for site in websites:
                    line1 = f'127.0.0.1 {site}\n'
                    line2 = f'127.0.0.1 www.{site}\n'
                    hosts_file.write(line1)
                    hosts_file.write(line2)
                    print(f"added: {line1.strip()} and {line2.strip()}")
                hosts_file.write('# StudyPy Block END\n')

            print("✓ wrote to host file")
            flush_dns()
            print("✓ DNS flushed")
            return True

        except Exception as e:
            print(f"error: couldn't write to hosts: {e}")
            return False


    def stats():
        for widget in root.winfo_children():
            widget.destroy()

        stats_title_label = tk.Label(root, text="Stats:", font=("Helvetica", 26), justify="center", bg=themecolour, fg=text_colour)
        stats_title_label.pack(pady=(60,10))

        stats_text_label = tk.Label(root, text=f"Total Time Studied ⌛: {total_time_studied}\nTotal Days 📊: {total_days}\nCurrent Day Streak 🔥: {current_day_streak}\nLongest Streak 🏆: {longest_streak}\nLast Study Date 📅: {last_study_date}", font=("Helvetica", 18), justify="center", bg=themecolour, fg=text_colour)
        stats_text_label.pack(pady=30)

        back_button = tk.Button(root, text="Back", command=show_main_menu, **button_style)
        back_button.pack(pady=20)



    buttons = [
        ("⛰️ Motivation", show_quote),
        ("🕒 Pomodoro Timer", pomodoro),
        ("⚙️ Set Times", set_times),
        ("☮️ Focus Settings", focus_mode),
        ("✅ To-Do List", to_do_list),
        ("📊 Stats", stats)
    ]


    if isDarkMode:
        buttons.append(("Light ☀️", toggle_theme))
    else:
        buttons.append(("Dark 🌙", toggle_theme))

    for text, command in buttons:
        b = tk.Button(button_frame, text=text, command=command, **button_style)
        b.pack(pady=5)


def closing():
    global timer_id, total_time_studied, total_days, current_day_streak, longest_streak

    with open("stats.csv", mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['total_time_studied', 'total_days', 'current_day_streak', 'longest_streak', 'last_study_date'])
        writer.writerow([total_time_studied, total_days, current_day_streak, longest_streak, last_study_date])


    #cancel timer
    try:
        if timer_id is not None:
            root.after_cancel(timer_id)
    except:
        pass

    unblock_sites()

    root.destroy()

root.protocol("WM_DELETE_WINDOW", closing)

show_main_menu()
root.mainloop()