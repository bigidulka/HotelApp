# File path: forms/change_password_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.user import User

class ChangePasswordForm(tk.Toplevel):
    def __init__(self, parent, login):
        super().__init__(parent)
        self.user_model = User()
        self.login = login

        # Параметры окна
        self.title("Смена пароля")
        self.geometry("700x350")   # Начальный размер
        self.minsize(700, 350)     # Минимальный размер
        self.resizable(True, True) # Разрешаем масштабирование

        # Настраиваем стили ttk
        self.style = ttk.Style(self)
        self.configure_styles()

        # Создаём фрейм-контейнер, который займёт всё окно
        self.main_frame = ttk.Frame(self, style="FormArea.TFrame")
        self.main_frame.pack(fill="both", expand=True)

        self.create_form()

    def configure_styles(self):
        """
        Используем стили, похожие на LoginForm, но без баннера.
        """
        self.style.theme_use("clam")

        # Задний план (FormArea) — светло-серый
        self.style.configure(
            "FormArea.TFrame",
            background="#F5F5F5"
        )

        # Заголовок формы
        self.style.configure(
            "FormTitle.TLabel",
            background="#F5F5F5",
            foreground="#3E2723",
            font=("Arial", 16, "bold")
        )

        # Обычные метки
        self.style.configure(
            "Regular.TLabel",
            background="#F5F5F5",
            foreground="#333333",
            font=("Arial", 11)
        )

        # Поля ввода
        self.style.configure(
            "Regular.TEntry",
            font=("Arial", 11),
            padding=5
        )

        # Кнопка «Изменить пароль»
        self.style.configure(
            "ChangeButton.TButton",
            font=("Arial", 12, "bold"),
            foreground="#FFFFFF",
            background="#5D4037",  # Коричневый
            padding=(10, 6)
        )
        self.style.map(
            "ChangeButton.TButton",
            background=[("active", "#4E342E")]  # чуть темнее при наведении
        )

    def create_form(self):
        """
        Размещаем заголовок и поля (текущий, новый, подтверждение) в основном фрейме.
        """
        # Заголовок формы
        lbl_title = ttk.Label(
            self.main_frame,
            text="Смена пароля",
            style="FormTitle.TLabel"
        )
        lbl_title.pack(pady=(30, 10))

        # Фрейм для полей ввода
        fields_frame = ttk.Frame(self.main_frame, style="FormArea.TFrame")
        fields_frame.pack(padx=30, pady=10, fill="x")

        # Текущий пароль
        lbl_current = ttk.Label(fields_frame, text="Текущий пароль:", style="Regular.TLabel")
        lbl_current.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.txt_current_password = ttk.Entry(fields_frame, style="Regular.TEntry", show="*")
        self.txt_current_password.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # Новый пароль
        lbl_new = ttk.Label(fields_frame, text="Новый пароль:", style="Regular.TLabel")
        lbl_new.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.txt_new_password = ttk.Entry(fields_frame, style="Regular.TEntry", show="*")
        self.txt_new_password.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # Подтверждение
        lbl_confirm = ttk.Label(fields_frame, text="Подтверждение:", style="Regular.TLabel")
        lbl_confirm.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.txt_confirm_password = ttk.Entry(fields_frame, style="Regular.TEntry", show="*")
        self.txt_confirm_password.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        fields_frame.columnconfigure(1, weight=1)

        # Кнопка «Изменить пароль»
        btn_change = ttk.Button(self.main_frame, text="Изменить пароль", style="ChangeButton.TButton", command=self.on_change)
        btn_change.pack(pady=20)

    def on_change(self):
        """
        Логика смены пароля:
        - Проверяем заполненность полей
        - Сравниваем новый пароль и подтверждение
        - Вызываем метод change_password
        """
        current_password = self.txt_current_password.get().strip()
        new_password = self.txt_new_password.get().strip()
        confirm_password = self.txt_confirm_password.get().strip()

        # Проверка всех полей
        if not current_password or not new_password or not confirm_password:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения.")
            return

        if new_password != confirm_password:
            messagebox.showerror("Ошибка", "Новый пароль и подтверждение не совпадают.")
            return

        # Вызываем метод модели
        success, msg = self.user_model.change_password(self.login, current_password, new_password)
        if success:
            messagebox.showinfo("Информация", msg)
            self.destroy()  # Закрываем форму
        else:
            messagebox.showerror("Ошибка", msg)
