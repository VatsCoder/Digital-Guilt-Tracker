from tkinter import *
from tkinter import ttk
import backend as be
import dashboard as dboard

def show_history(root, user_id):
    # clear old widgets
    for widget in root.winfo_children():
        widget.destroy()

    Label(root, text="📜 Guilt History", font=("Helvetica", 16, "bold"),
          bg="#f2e6f9", fg="#512a88").pack(pady=10)

    # frame for treeview + scrollbar
    frame = Frame(root, bg="#f2e6f9")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    columns = ("Date", "Emotion", "Reason", "Guilt Rate", "Guilt Score")

    tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

    # headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    # vertical scrollbar
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    # get logs from db
    logs = be.get_all_logs(user_id)

    if not logs:
        tree.insert("", "end", values=("No data", "", "", "", ""))
    else:
        for log in logs:
            tree.insert("", "end", values=log)

    # back button
    back_btn = Button(root, text="Back to Dashboard", 
                     font=("Helvetica", 12, "bold"), 
                     bg="#512a88", fg="white",
                     command=lambda: dboard.show_dashboard(root, user_id))
    back_btn.pack(pady=10)
