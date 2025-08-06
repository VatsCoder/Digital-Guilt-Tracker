from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Pillow

def continue_handled():
    messagebox.showinfo("Profile Submitted","Profile Submitted")

root = tk.Tk()
root.geometry("600x400")
root.title("Digital Guilt Tracker")
root.configure(bg='#d0c0fa')

image = Image.open("./images/profile.png")  # Any format
resized_image = image.resize((80, 80))
tk_image = ImageTk.PhotoImage(resized_image)
 
canvas = Canvas(root, bg="#d0c0fa", width=resized_image.width, height=resized_image.height,highlightthickness=0)
canvas.create_image(0, 0, anchor=tk.NW, image=tk_image) # Top-left corner at (0,0)
canvas.pack(pady=10)



image1 = Image.open("./images/signal-status.png")  # Any format
resized_image1 = image1.resize((40, 40))
tk_image1 = ImageTk.PhotoImage(resized_image1)

canvas = Canvas(root, width=resized_image1.width, height=resized_image1.height)
canvas.create_image(2, 0, anchor=tk.NW, image=tk_image1) # Top-left corner at (0,0)
# canvas.place(x="350", y="50")

label1 = tk.Label(root, text="Guilt Level Tracker", font='Helvetica 16 bold', fg='#5715ad', bg='#d0c0fa')
label1.pack()

label2 = tk.Label(root, text="Reflect on daily guilt levels", font='Helvetica 8', bg='#d0c0fa')
label2.pack()

label3 = tk.Label(root, text="Set up your guilt profile", font='Helvetica 25 bold', bg='#d0c0fa')
label3.pack()

entry_name = tk.Entry(root, width=35, font=('Arial', 15))
entry_name.insert(0,'Enter your full name')
entry_name.pack(pady="20")

entry_age = tk.Entry(root, width=35, font=('Arial', 15))
entry_age.insert(0,'Enter your age')
entry_age.pack()

entry_mail = tk.Entry(root, width=35, font=('Arial', 15))
entry_mail.insert(0,'Enter your mail')
entry_mail.pack(pady="20")

continue_btn = tk.Button(root, text='Continue', font='Helvetica 10 bold', fg='White', bg="#b70eca",
                       padx=50, pady=5,command=continue_handled)
continue_btn.pack()

root.mainloop()