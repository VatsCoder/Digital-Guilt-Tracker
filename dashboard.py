import tkinter as tk
from tkinter import font, ttk
import backend as be
from datetime import date, timedelta
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import login

# Colors
PURPLE = "#6A5ACD"
LAVENDER = "#D8C7F3"
INK = "#2E2E54"
CREAM = "#F6EFE6"


def show_dashboard(root, user_id):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("800x600")
    root.title("Guilt Tracker - Dashboard")
    root.configure(bg=LAVENDER)
    root.resizable(False, False)

    feeling_var = tk.StringVar(value="")

    def on_feeling_click(value):
        feeling_var.set(value)

    # Main cream canvas inside lavender background
    canvas = tk.Canvas(root, bg=CREAM, highlightthickness=0, width=780, height=580)
    canvas.place(x=10, y=10)

    # Fonts
    title_font = font.Font(family="Helvetica", size=20, weight="bold")
    label_font = font.Font(family="Helvetica", size=13)
    small_font = font.Font(family="Helvetica", size=11)
    p = font.Font(family="Helvetica", size=11)

    # Function for rounded rectangles
    def round_rect(x1, y1, x2, y2, r=15, **kwargs):
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1
        ]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def calculate_guilt_score(emotion, guilt):
        emotion_weights = {"happy": -10, "neutral": 0, "sad": 10, "stressed": 15, "anxious": 20}
        base_emotion = emotion_weights.get(emotion.lower(), 0)
        guilt_score = base_emotion + guilt
        return guilt_score

    def on_save(user_id):
        emotion = feeling_var.get()
        guilt = guilt_slider.get()
        reason = reason_entry.get()
        trigger = trigger_entry.get()
        today = date.today().isoformat()

        score = calculate_guilt_score(emotion, guilt)
        be.save_guilt_entry(user_id, today, emotion, guilt, reason, trigger, score)
        progress_number.config(text=score)
        update_chart(ax, chart_fig, user_id)

    # Title bar
    canvas.create_text(20, 30, anchor="w", text="GUILT TRACKER", font=title_font, fill=INK)

    # Feelings
    canvas.create_text(20, 70, anchor="w", text="How are you feeling right now?", font=label_font, fill=INK)
    emotions = [("😊", "happy"), ("😢", "sad"), ("😐", "neutral"), ("😫", "stressed"), ("😟", "anxious")]
    x_start = 50
    for emoji, label in emotions:
        emoji_label = tk.Label(root, text=emoji, font=("Helvetica", 28), fg=INK, bg=CREAM, cursor="hand2")
        canvas.create_window(x_start, 105, window=emoji_label)
        canvas.create_text(x_start, 135, text=label, font=small_font, fill=INK)
        emoji_label.bind("<Button-1>", lambda event, feeling=label: on_feeling_click(feeling))
        x_start += 85

    # Reason for guilt
    canvas.create_text(20, 170, anchor="w", text="Reason for guilt", font=label_font, fill=INK)
    reason_entry = tk.Entry(root, font=("Helvetica", 12), relief="solid", bd=1, width=50, fg="grey")
    reason_placeholder = 'Enter reason for your guilt'
    reason_entry.insert(0, reason_placeholder)
    canvas.create_window(270, 170, anchor="w", window=reason_entry, height=30)

    # Trigger & control
    canvas.create_text(20, 210, anchor="w", text="Trigger & control", font=label_font, fill=INK)
    trigger_entry = tk.Entry(root, font=p, relief="solid", bd=1, width=25, fg="grey")
    trigger_placeholder = 'Enter app to restrict'
    trigger_entry.insert(0, trigger_placeholder)
    canvas.create_window(270, 210, anchor="w", window=trigger_entry, height=28)

    def clear_placeholder(event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def add_placeholder(event, entry, placeholder):
        if entry.get().strip() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    reason_entry.bind("<FocusIn>", lambda e: clear_placeholder(e, reason_entry, reason_placeholder))
    reason_entry.bind("<FocusOut>", lambda e: add_placeholder(e, reason_entry, reason_placeholder))

    trigger_entry.bind("<FocusIn>", lambda e: clear_placeholder(e, trigger_entry, trigger_placeholder))
    trigger_entry.bind("<FocusOut>", lambda e: add_placeholder(e, trigger_entry, trigger_placeholder))

    time_btn = tk.Button(root, text="30m", font=p, bg=LAVENDER, relief="flat", width=6)
    canvas.create_window(500, 210, anchor="w", window=time_btn, height=28)

    custom_btn = tk.Button(root, text="Custom", font=p, bg=LAVENDER, relief="flat", width=9)
    canvas.create_window(580, 210, anchor="w", window=custom_btn, height=28)

    # Guilt Rating
    canvas.create_text(20, 250, anchor="w", text="Guilt Rating", font=label_font, fill=INK)
    guilt_slider = tk.Scale(root, from_=0, to=10, orient="horizontal", length=450, bg="#d0c0fa",
                            highlightthickness=0, troughcolor="#c4aaf2",
                            activebackground="#7a4dd7", font=("Helvetica", 10, "bold"))
    canvas.create_window(495, 250, window=guilt_slider)

    # Progress box
    canvas.create_text(50, 280, anchor="w", text="Progress", font=label_font, fill=INK)
    round_rect(40, 310, 350, 400, r=20, fill="", outline=INK, width=1.5)
    progress_number = tk.Label(root, text="0", font=("Helvetica", 30, "bold"), fg=INK, bg=CREAM)
    canvas.create_window(110, 350, window=progress_number)

    # Weekly chart
    round_rect(390, 290, 770, 500, r=20, fill="", outline=INK, width=1.5)
    fig = Figure(figsize=(3.6, 2), dpi=100, facecolor=CREAM)
    ax = fig.add_subplot(111, facecolor=CREAM)
    chart_fig = FigureCanvasTkAgg(fig, master=root)
    chart_fig.get_tk_widget().place(x=410, y=305)

    def update_chart(ax, chart_fig, user_id):
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        days = [(start_of_week + timedelta(days=i)) for i in range(7)]
        day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        scores = [0] * 7
        data = be.get_weekly_guilt_entries(user_id, start_of_week.isoformat())

        last_entry_per_day = {}
        for d, s, entry_id in data:
            if d not in last_entry_per_day or entry_id > last_entry_per_day[d][1]:
                last_entry_per_day[d] = (s, entry_id)

        for i, day in enumerate(days):
            day_str = day.isoformat()
            if day_str in last_entry_per_day:
                scores[i] = last_entry_per_day[day_str][0]

        ax.clear()
        ax.bar(range(7), scores, color="#9F98D0", width=0.6)
        ax.set_xticks(range(7))
        ax.set_xticklabels(day_labels)
        ax.set_ylim(0, max(scores) + 10 if max(scores) > 0 else 10)
        ax.set_ylabel("Guilt Score")
        chart_fig.draw()

    update_chart(ax, chart_fig, user_id)

    # Motivational text
    round_rect(40, 410, 350, 500, r=20, fill="", outline=INK, width=1.5)
    canvas.create_text(200, 450, text="You are capable of overcoming guilt.",
                       font=("Helvetica", 11, "italic"), fill=INK)

    # Save button
    save_btn = tk.Button(root, text="Save", font=("Helvetica", 14, "bold"),
                         bg=LAVENDER, relief="flat", width=25,
                         command=lambda: on_save(user_id))
    canvas.create_window(375, 550, window=save_btn, height=35)
    progress_number.config(text="0")

    today = date.today().isoformat()
    today_score = be.get_today_score(user_id, today)
    if today_score is None:
        progress_number.config(text="0")
    else:
        progress_number.config(text=today_score)

    # SETTINGS BUTTON
    # settings_btn = tk.Button(root, text="⚙ Settings", font=("Helvetica", 11),
    #                          bg=LAVENDER, relief="flat", width=10,
    #                          command=lambda: show_settings_page(root, user_id))
    # settings_btn.place(x=20, y=550)
    # SETTINGS BUTTON WITH DROPDOWN MENU
    def show_menu(event):
      settings_menu.tk_popup(event.x_root, event.y_root)

    settings_btn = tk.Button(root, text="⚙ Settings ▼", font=("Helvetica", 11),
                         bg=LAVENDER, relief="flat", width=12)
    settings_btn.place(x=20, y=550)

# Dropdown menu
    settings_menu = tk.Menu(root, tearoff=0, bg="LAVENDER", fg="black", font=("Helvetica", 11))
    settings_menu.add_command(label="⏰ History", command=lambda: show_history_page(root, user_id))
    settings_menu.add_command(label="🔒 Logout", command=lambda: login.show_login_screen(root))

# Bind left-click to show dropdown
    settings_btn.bind("<Button-1>", show_menu)



# HISTORY PAGE
def show_history_page(root, user_id):
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg=LAVENDER)
    root.title("Guilt Tracker - History")

    back_btn = tk.Button(root, text="← Back", font=("Helvetica", 11, "bold"),
                         bg=LAVENDER, relief="flat",fg=INK,
                         command=lambda: show_dashboard(root, user_id))
    back_btn.place(x=20, y=20)

    history_label = tk.Label(root, text="Your Entries", font=("Helvetica", 14, "bold"),
                             bg=LAVENDER, fg=INK)
    history_label.pack(pady=10)

    # Table with scrollbar
    cols = ("Date", "Emotion", "Guilt Rate", "Control", "Score")
    frame = tk.Frame(root)
    frame.pack(pady=10)

    history_table = ttk.Treeview(frame, columns=cols, show="headings", height=30)

    for col in cols:
        history_table.heading(col, text=col)
        history_table.column(col, anchor="center", width=130,stretch=True)

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=history_table.yview)
    history_table.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    history_table.pack(side="left", fill="both", expand=True)

    # Fetch entries from backend
    entries = be.get_all_logs(user_id)
    for row in entries:
        history_table.insert("", tk.END, values=row)

    def delete_selected():
        selected = history_table.selection()
        if not selected:
            tk.messagebox.showwarning("No selection", "Please select a row to delete.")
            return
        for item in selected:
            values = history_table.item(item, "values")
            # values: (Date, Emotion, Guilt Rate, Control, Score)
            be.delete_log(user_id, *values)
            history_table.delete(item)

    delete_btn = tk.Button(root, text="Delete", font=("Helvetica", 12, "bold"),
                       bg=LAVENDER, fg=INK, relief="flat",width=6,
                       command=delete_selected)
    delete_btn.place(x=700, y=20) 


# SETTINGS PAGE
# def show_settings_page(root, user_id):
#     for widget in root.winfo_children():
#         widget.destroy()

#     root.configure(bg=LAVENDER)
#     root.title("Settings")

#     back_btn = tk.Button(root, text="← Back", font=("Helvetica", 11, "bold"),
#                          bg=LAVENDER, relief="flat",
#                          command=lambda: show_dashboard(root, user_id))
#     back_btn.place(x=20, y=20)

#     history_btn = tk.Button(root, text="History", font=("Helvetica", 14, "bold"),
#                             bg="#AC87E6", relief="flat", width=15,
#                             command=lambda: show_history_page(root, user_id))
#     history_btn.pack(pady=20)

#     logout_btn = tk.Button(root, text="Logout", font=("Helvetica", 14, "bold"),
#                            bg="#ff4d4d", fg="white", relief="flat", width=15,
#                            command=lambda: login.show_login_screen(root))
#     logout_btn.pack(pady=20)