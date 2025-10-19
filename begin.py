import tkinter as tk
import profile_details  # written by me

def begin():
    profile_details .show_profile_details(root)  # Show the profile details page/ written by me

root = tk.Tk()
root.geometry("800x600")
root.configure(bg="#f2e6f9")
root.title("Digital Guilt Tracker")

# Icon Canvas (rounded white box + bars)
icon_canvas = tk.Canvas(root, width=160, height=160, bg="#f2e6f9", highlightthickness=0)
icon_canvas.pack(pady=20)

# Rounded white square shape
icon_canvas.create_polygon(
    20, 10,
    140, 10,
    150, 10,
    150, 30,
    150, 130,
    150, 150,
    140, 150,
    20, 150,
    10, 150,
    10, 130,
    10, 30,
    10, 10,
    smooth=True,
    fill="white",
    outline=""
)

# "GUILT LEVELS" text inside the white box
icon_canvas.create_text(80, 25, text="GUILT LEVELS", fill="#5f4b8b", font=("Helvetica", 10, "bold"))

# 3 purple guilt level bars
icon_canvas.create_rectangle(40, 90, 55, 140, fill="#b499e5", width=0)
icon_canvas.create_rectangle(70, 70, 85, 140, fill="#a87ce3", width=0)
icon_canvas.create_rectangle(100, 50, 115, 140, fill="#8f5bdc", width=0)

# Main Title
tk.Label(root, text="GuiltTracker", bg="#f2e6f9", fg="#512a88", font=("Helvetica", 20, "bold")).pack(pady=(10, 5))

# Subtitle
tk.Label(root, text="Log and reflect on daily guilt levels", bg="#f2e6f9", fg="#512a88", font=("Helvetica", 12)).pack(pady=(0, 20))

# Begin Button
tk.Button(root, text="Begin", font=("Helvetica", 12), fg="#512a88", bg="white", relief="solid", bd=1, padx=20, pady=5,command=begin).pack()

root.mainloop()