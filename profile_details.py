from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Pillow
import backend as be
import login as sp

be.init_db()
def continue_handled(entry_widgets,placeholder_text):
    isValid = True
    for i,entry in enumerate(entry_widgets):
        value = entry.get()
        if not value.strip() or value!=value.strip() or value == placeholder_text[i]:
            isValid = False
            messagebox.showerror("Invalid input","Please enter correct details")
            break
        elif i==0 and not isinstance(value,str):
                messagebox.showerror("Invalid input","Please enter correct name.")
                isValid = False
                break
        elif i==1:
            try:
                value = int(entry.get())
                if value > 100:
                    messagebox.showerror("Invalid age","Age should be less than 100.")
                    isValid = False
                    break 
            except Exception:
                 messagebox.showerror("Invalid age","Please enter correct age.")
                 isValid = False
        elif i==2 and not isinstance(value,str):
                messagebox.showerror("Invalid input","Please enter correct email.")
                isValid = False
                break 
        elif i == 2 and "@" not in value:
            messagebox.showerror("Invalid input", "Please enter correct email.")
            isValid = False
            break
        elif i == 3 and len(value) < 6 or value == "":
            messagebox.showerror("Invalid password", "Password must be at least 6 characters.")
            isValid = False
            break
    return isValid

def submit(entry_widgets, placeholder_text):
    if continue_handled(entry_widgets, placeholder_text):
        name = entry_widgets[0].get().strip()
        age = int(entry_widgets[1].get().strip())
        email = entry_widgets[2].get().strip()
        password = entry_widgets[3].get().strip()
        if be.add_user(name, age,email,password):
            messagebox.showinfo("Submitted", "Profile Created Successfully")
        else:
            messagebox.showerror("Error", "Email already exists, please log in.")

def on_entry_click(event,entry_widget,placeholder_text):
    """Function to clear the placeholder when the entry is clicked."""
    if entry_widget.get() == placeholder_text:
        entry_widget.delete(0, tk.END)
  
def on_focus_out(event,entry_widget,placeholder_text):
    """Function to clear the placeholder when the entry is clicked."""
    if entry_widget.get() == "":
        entry_widget.insert(0, placeholder_text)
def login(root):
    sp.show_login_screen(root)

visible=False
def show_profile_details(root):
    for widget in root.winfo_children():
        widget.destroy()
    def toggle_password():
        global visible
        if visible:
          entry_password.config(show='*')
          show_button.config(image=show_image)
          visible=False
        else:
          entry_password.config(show='')
          show_button.config(image=hide_image)
          visible=True   
    root.configure(bg='#d0c0fa')
    image = Image.open("./images/profile.png")  # Any format
    resized_image = image.resize((80, 80))
    tk_image = ImageTk.PhotoImage(resized_image)
    root.tk_image = tk_image
    canvas = Canvas(root, bg="#d0c0fa", width=resized_image.width, height=resized_image.height,highlightthickness=0)
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image) # Top-left corner at (0,0)
    canvas.pack(pady=10)

    # frame=tk.Frame(root,height=600,width=800,bg='#f2e6f9')
    # frame.pack()
    frame = tk.Frame(root, bg='#f2e6f9', padx=40, pady=30, relief="groove")
    frame.pack(pady=20) 


    label1 = tk.Label(frame, text="Guilt Level Tracker", font='Helvetica 20 bold', fg='#512a88', bg='#f2e6f9')
    label1.pack()

    label2 = tk.Label(frame, text="Reflect on daily guilt levels", font='Helvetica 12',fg='#512a88' ,bg='#f2e6f9')
    label2.pack()

    label3 = tk.Label(frame, text="Set up your Guilt Profile", font='Helvetica 22 bold',fg='#512a88', bg='#f2e6f9')
    label3.pack()

    label4 = tk.Label(frame, text="Log In!", fg="blue", cursor="hand2", bg="#f2e6f9", font=("Helvetica", 10, "underline"))
    label4.pack()

    label4.bind("<Button-1>", lambda event: login(root))
    place_holder = ['Enter your full name','Enter your age','Enter your mail','Create your password']

    entry_name = tk.Entry(frame, width=35, font=('Arial', 15),fg='#512a88',bg='#f2e6f9',relief='solid',highlightthickness=2)
    entry_name.insert(0,place_holder[0])
    entry_name.pack(pady="8")
    entry_name.config(highlightbackground="#512a88", highlightcolor= "#512a88")
    

    entry_name.bind("<FocusIn>",lambda event: on_entry_click(event,entry_name,place_holder[0])) #binding click event on input field
    entry_name.bind("<FocusOut>",lambda event: on_focus_out(event,entry_name,place_holder[0]))

    entry_age = tk.Entry(frame, width=35, font=('Arial', 15),fg='#512a88',bg='#f2e6f9',relief='solid',highlightthickness=2)
    entry_age.insert(0,place_holder[1])
    entry_age.pack()
    entry_age.config(highlightbackground="#512a88", highlightcolor= "#512a88")

    entry_age.bind("<FocusIn>",lambda event: on_entry_click(event,entry_age,place_holder[1])) #binding click event on input field
    entry_age.bind("<FocusOut>",lambda event: on_focus_out(event,entry_age,place_holder[1]))


    entry_mail = tk.Entry(frame, width=35, font=('Arial', 15),fg='#512a88',bg='#f2e6f9',relief='solid',highlightthickness=2)
    entry_mail.insert(0,place_holder[2])
    entry_mail.pack(pady="8")
    entry_mail.config(highlightbackground="#512a88", highlightcolor= "#512a88")

    entry_mail.bind("<FocusIn>",lambda event: on_entry_click(event,entry_mail,place_holder[2])) #binding click event on input field
    entry_mail.bind("<FocusOut>",lambda event: on_focus_out(event,entry_mail,place_holder[2]))

    password_frame = tk.Frame(frame, bg="#d0c0fa")
    password_frame.pack()

    entry_password = tk.Entry(password_frame, width=35, font=("Arial", 15),fg='#512a88',bg='#f2e6f9',relief='solid',highlightthickness=2)
    entry_password.insert(0, place_holder[3])
    entry_password.pack(side="left", padx=(0, 5))
    entry_password.config(highlightbackground="#512a88", highlightcolor= "#512a88")

    show_image=tk.PhotoImage(file="./images/show.png")
    hide_image=tk.PhotoImage(file='./images/hide.png')

    show_button=tk.Button(frame,image=show_image,relief='flat',command=toggle_password)
    show_button.place(x=340,y=252)
    # show_button.place(x=549,y=360)
    # toggle_btn = tk.Button(root, text="Show", command=toggle_password)
    # toggle_btn.place(x=450,y=330)

    entry_password.bind("<FocusIn>",lambda event: on_entry_click(event,entry_password,place_holder[3])) #binding click event on input field
    entry_password.bind("<FocusOut>",lambda event: on_focus_out(event,entry_password,place_holder[3]))

    entrytext_list = [entry_name,entry_age,entry_mail,entry_password]

    continue_btn = tk.Button(frame, text='Continue', font='Helvetica 10 bold', fg='#512a88', bg="#d0c0fa",
                        padx=40, pady=5,command=lambda: submit(entrytext_list,place_holder))

    continue_btn.pack(padx=0,pady=10)
