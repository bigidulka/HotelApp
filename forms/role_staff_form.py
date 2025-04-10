# File path: forms/role_staff_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.user import User

class RoleStaffForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Создание новой роли для сотрудников")
        self.geometry("350x150")
        self.resizable(False, False)
        self.user_model = User()  # используем методы модели User для добавления роли
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        ttk.Label(frame, text="Название роли:").pack(pady=(0,10))
        self.entry_role = ttk.Entry(frame)
        self.entry_role.pack(pady=(0,10), fill="x")
        btn = ttk.Button(frame, text="Создать роль", command=self.create_role)
        btn.pack()

    def create_role(self):
        role_name = self.entry_role.get().strip()
        if not role_name:
            messagebox.showerror("Ошибка", "Введите название роли.")
            return
        success, msg = self.user_model.add_role(role_name)
        if success:
            messagebox.showinfo("Успех", msg)
            self.destroy()
        else:
            messagebox.showerror("Ошибка", msg)
