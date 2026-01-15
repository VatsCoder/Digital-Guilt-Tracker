from tkinter import *
import tkinter as tk
import backend as be
from tkinter import messagebox
import profile_details
import dashboard as dboard

visible=False

def signup(root):
    profile_details.show_profile_details(root)
    
def show_login_screen(root):
    for widget in root.winfo_children():
        widget.destroy()
    def Uentry_focus_in(event):
        if Username_entry.get()=="Enter your username":
            Username_entry.delete(0,'end')
            Username_entry.config(fg='#512a88')

    def Uentry_focus_out(event):
        if Username_entry.get()=="":
            Username_entry.insert(0,'Enter your username')
            Username_entry.config(fg='#512a88')

    def Pentry_focus_in(event):
        if Password_entry.get()=="Enter your password":
            Password_entry.delete(0,'end')
            Password_entry.config(fg='#512a88',show='*')

    def Pentry_focus_out(event):
        if Password_entry.get()=="":
            Password_entry.insert(0,'Enter your password')
            Password_entry.config(fg='#512a88',show='')
    # def submit():
    #     messagebox.showinfo("login","login successful")    
    def toggle_password():
        global visible
        if visible:
          Password_entry.config(show='*')
          show_button.config(image=show_image)
          visible=False
        else:
          Password_entry.config(show='')
          show_button.config(image=hide_image)
          visible=True
    
    def handle_login(event=None):
        email = Username_entry.get().strip()
        password = Password_entry.get().strip()
        user = be.login_user(email,password)
        if user:
            user_id, user_name = user
            dboard.show_dashboard(root, user_id)
            # tk.Label(root, text=user_name, font=("Helvetica", 10, "bold"), bg="#d0c0fa").pack()
        else:
            messagebox.showerror("Error", "User not found. Please sign up first.")

    
    frame=tk.Frame(root,height=300,width=500,bg='#f2e6f9')
    frame.pack(pady=120)
    frame.pack_propagate(False)

    #Main heading
    label1=tk.Label(frame,text='Guilt Tracker',fg="#512a88",bg='#f2e6f9', font=("Helvetica", 20, "bold"))
    label1.pack(pady=5)

    # Subheading
    label2=tk.Label(frame,text='Enter your login credentials',fg="#512a88",bg='#f2e6f9', font=("Helvetica", 12))
    label2.pack()

    #Username
    label3=tk.Label(frame,text='Username:',fg="#512a88",bg='#f2e6f9', font=("Helvetica", 12,'bold'))
    label3.pack(anchor='w',pady=20,padx=25)

    #Username entry
    Username_entry=tk.Entry(frame,font=('helvetica',12),fg="#512a88",bg='#f2e6f9',relief='solid',highlightthickness=2)
    Username_entry.place(x=35,y=120,width=430,height=35)
    Username_entry.config(highlightbackground="#512a88", highlightcolor= "#512a88")
    Username_entry.insert(0,'Enter your username')
    Username_entry.bind("<FocusIn>",Uentry_focus_in)
    Username_entry.bind("<FocusOut>",Uentry_focus_out)

    #password
    label4=tk.Label(frame,text='Password:',fg="#512a88",bg='#f2e6f9', font=("Helvetica", 12,'bold'))
    label4.pack(anchor='w',pady=20,padx=25)

    #password entry
    Password_entry=tk.Entry(frame,font=('helvetica',12),bg='#f2e6f9',fg="#512a88",relief='solid',highlightthickness=2)
    Password_entry.place(x=35,y=185,width=430,height=35)
    Password_entry.config(highlightbackground="#512a88", highlightcolor= "#512a88")
    Password_entry.insert(0,'Enter your password')
    Password_entry.bind("<FocusIn>",Pentry_focus_in)
    Password_entry.bind("<FocusOut>",Pentry_focus_out)

    #show button
    show_image=tk.PhotoImage(file="./images/show.png")
    hide_image=tk.PhotoImage(file='./images/hide.png')

    show_button=tk.Button(frame,image=show_image,relief='flat',command=toggle_password)
    show_button.place(x=415,y=188)
    #submit button
    submit_button=tk.Button(frame,text='Submit',font=('helvetica',10,'bold'),fg='#512a88',bg='#d0c0fa',relief='raised',command=handle_login)
    submit_button.place(x=210,y=240,width=90,height=30)
    root.bind("<Return>", handle_login)

    #indication for new user to create new account
    label5=tk.Label(frame,text='Not registered?',font=('helvetica',10),fg='#512a88',bg='#f2e6f9')
    label5.place(x=170,y=278)

    label6=tk.Label(frame,text='Create account',cursor='hand2',font=('helvetica',10),fg='#512a88',bg='#f2e6f9')
    label6.place(x=260,y=278)

    label6.bind("<Button-1>", lambda e:signup(root))
    # tk.Button(root, text="Login", font=("Helvetica", 12, "bold"), bg="#b70eca", fg="white", command=handle_login).pack(pady=20)
