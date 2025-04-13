import customtkinter
from tkinter import *
from PIL import ImageTk

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')





def add(task):
    f = customtkinter.CTkFrame(root)

    customtkinter.CTkCheckBox(f, text=task).pack(anchor=NW, side=LEFT)
    customtkinter.CTkButton(f, image=img_del,text='', width=30, command=lambda: f.pack_forget()).pack(anchor=NW,side=LEFT, padx=10)
    f.pack(anchor=NW, padx=5,pady=5)

def add_task():
    window = customtkinter.CTkToplevel(root)
    window.title('Add request')
    window.geometry('300x80')

    task_text = customtkinter.CTkEntry(window, width=250)
    task_text.pack(pady=5)

    customtkinter.CTkButton(window, text='Add',font=('Arial', 13, 'bold'), command=lambda: add(task_text.get())).pack()
    window.mainloop()

root = customtkinter.CTk()
root.title('To Do List')
root.geometry('700x300')

img_del = ImageTk.PhotoImage(file='del.png')

btn_add_task = customtkinter.CTkButton(root, text='Add Task', font=('Arial', 13, 'bold'), command=add_task)
btn_add_task.pack(anchor=S, side=BOTTOM, pady=5)

root.mainloop()