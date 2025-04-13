# import customtkinter
# from tkinter import *
# from PIL import ImageTk

# customtkinter.set_appearance_mode('dark')
# customtkinter.set_default_color_theme('dark-blue')





# def add(task):
#     f = customtkinter.CTkFrame(root)

#     customtkinter.CTkCheckBox(f, text=task).pack(anchor=NW, side=LEFT)
#     customtkinter.CTkButton(f, image=img_del,text='', width=30, command=lambda: f.pack_forget()).pack(anchor=NW,side=LEFT, padx=10)
#     f.pack(anchor=NW, padx=5,pady=5)

# def add_task():
#     window = customtkinter.CTkToplevel(root)
#     window.title('Add request')
#     window.geometry('300x80')

#     task_text = customtkinter.CTkEntry(window, width=250)
#     task_text.pack(pady=5)

#     customtkinter.CTkButton(window, text='Add',font=('Arial', 13, 'bold'), command=lambda: add(task_text.get())).pack()
#     window.mainloop()

# root = customtkinter.CTk()
# root.title('To Do List')
# root.geometry('700x300')

# img_del = ImageTk.PhotoImage(file='del.png')

# btn_add_task = customtkinter.CTkButton(root, text='Add Task', font=('Arial', 13, 'bold'), command=add_task)
# btn_add_task.pack(anchor=S, side=BOTTOM, pady=5)

# root.mainloop()


import customtkinter
from tkinter import *
from PIL import ImageTk, Image
import json
import os

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Enhanced To Do List')
        self.root.geometry('800x500')
        
        # Загрузка иконок
        self.load_images()
        
        # Загрузка задач
        self.tasks = []
        self.load_tasks()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Счетчик задач
        self.task_count = len(self.tasks)
        
    def load_images(self):
        try:
            self.img_del = ImageTk.PhotoImage(Image.open('del.png').resize((20, 20)))
            self.img_edit = ImageTk.PhotoImage(Image.open('edit.png').resize((20, 20)))
            self.img_save = ImageTk.PhotoImage(Image.open('save.png').resize((20, 20)))
        except:
            # Заглушки если изображения не найдены
            self.img_del = ImageTk.PhotoImage(Image.new('RGB', (20, 20), color='red'))
            self.img_edit = ImageTk.PhotoImage(Image.new('RGB', (20, 20), color='blue'))
            self.img_save = ImageTk.PhotoImage(Image.new('RGB', (20, 20), color='green'))
    
    def create_widgets(self):
        # Фрейм для списка задач
        self.tasks_frame = customtkinter.CTkScrollableFrame(self.root, width=700, height=400)
        self.tasks_frame.pack(pady=10)
        
        # Статус бар
        self.status_var = StringVar()
        self.update_status()
        status_bar = customtkinter.CTkLabel(self.root, textvariable=self.status_var)
        status_bar.pack(side=BOTTOM, fill=X)
        
        # Кнопки управления
        btn_frame = customtkinter.CTkFrame(self.root)
        btn_frame.pack(side=BOTTOM, pady=5)
        
        customtkinter.CTkButton(btn_frame, text='Add Task', command=self.add_task_window).pack(side=LEFT, padx=5)
        customtkinter.CTkButton(btn_frame, text='Clear All', command=self.clear_all).pack(side=LEFT, padx=5)
        customtkinter.CTkButton(btn_frame, text='Save Tasks', command=self.save_tasks).pack(side=LEFT, padx=5)
        
        # Отображение существующих задач
        for task in self.tasks:
            self.add_task_to_ui(task['text'], task['completed'])
    
    def add_task_to_ui(self, task_text, completed=False):
        task_frame = customtkinter.CTkFrame(self.tasks_frame)
        task_frame.pack(fill=X, padx=5, pady=2)
        
        # Чекбокс для статуса задачи
        status_var = BooleanVar(value=completed)
        checkbox = customtkinter.CTkCheckBox(task_frame, text=task_text, variable=status_var,
                                           command=lambda: self.update_task_status(task_frame, status_var.get()))
        checkbox.pack(side=LEFT, fill=X, expand=True)
        
        # Кнопка редактирования
        customtkinter.CTkButton(task_frame, image=self.img_edit, text='', width=30,
                              command=lambda: self.edit_task(task_frame)).pack(side=LEFT, padx=5)
        
        # Кнопка удаления
        customtkinter.CTkButton(task_frame, image=self.img_del, text='', width=30,
                              command=lambda: self.delete_task(task_frame)).pack(side=LEFT)
        
        # Сохраняем ссылку на текстовое поле (для редактирования)
        task_frame.task_text = task_text
        task_frame.checkbox = checkbox
    
    def add_task_window(self):
        window = customtkinter.CTkToplevel(self.root)
        window.title('Add New Task')
        window.geometry('350x120')
        
        customtkinter.CTkLabel(window, text='Enter task:').pack(pady=5)
        
        task_entry = customtkinter.CTkEntry(window, width=300)
        task_entry.pack(pady=5)
        
        customtkinter.CTkButton(window, text='Add', 
                              command=lambda: [self.add_task(task_entry.get()), window.destroy()]).pack(pady=5)
    
    def add_task(self, task_text):
        if task_text.strip():
            self.tasks.append({'text': task_text, 'completed': False})
            self.add_task_to_ui(task_text)
            self.task_count += 1
            self.update_status()
    
    def edit_task(self, task_frame):
        # Создаем окно редактирования
        edit_window = customtkinter.CTkToplevel(self.root)
        edit_window.title('Edit Task')
        edit_window.geometry('350x120')
        
        # Текстовое поле с текущим текстом задачи
        edit_entry = customtkinter.CTkEntry(edit_window, width=300)
        edit_entry.insert(0, task_frame.task_text)
        edit_entry.pack(pady=10)
        
        # Функция сохранения изменений
        def save_changes():
            new_text = edit_entry.get().strip()
            if new_text:
                task_frame.task_text = new_text
                task_frame.checkbox.configure(text=new_text)
                self.update_tasks_list()
                edit_window.destroy()
        
        customtkinter.CTkButton(edit_window, text='Save', command=save_changes).pack(pady=5)
    
    def delete_task(self, task_frame):
        task_frame.pack_forget()
        self.update_tasks_list()
        self.task_count -= 1
        self.update_status()
    
    def update_task_status(self, task_frame, completed):
        self.update_tasks_list()
    
    def update_tasks_list(self):
        self.tasks = []
        for child in self.tasks_frame.winfo_children():
            if hasattr(child, 'checkbox'):
                self.tasks.append({
                    'text': child.task_text,
                    'completed': child.checkbox.get()
                })
    
    def clear_all(self):
        for child in self.tasks_frame.winfo_children():
            child.destroy()
        self.tasks = []
        self.task_count = 0
        self.update_status()
    
    def save_tasks(self):
        with open('tasks.json', 'w') as f:
            json.dump(self.tasks, f)
        self.status_var.set("Tasks saved successfully!")
        self.root.after(2000, self.update_status)
    
    def load_tasks(self):
        if os.path.exists('tasks.json'):
            try:
                with open('tasks.json', 'r') as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []
    
    def update_status(self):
        completed = sum(1 for task in self.tasks if task['completed'])
        self.status_var.set(f"Total tasks:  | Completed: {completed} | Pending: ")

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = ToDoApp(root)
    root.mainloop()

