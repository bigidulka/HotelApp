# File path: forms/login_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from forms.change_password_form import ChangePasswordForm
from forms.admin_form import AdminForm
from models.user import User

class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.user_model = User()

        # Устанавливаем заголовок
        self.title("Авторизация - HotelApp")
        
        # Делаем окно масштабируемым, задаём стартовые и минимальные размеры
        self.geometry("900x500")     # Начальный размер (можно менять)
        self.minsize(700, 350)       # Минимально допустимые размеры
        self.resizable(True, True)   # Разрешаем изменение размеров

        # Настраиваем стили
        self.style = ttk.Style(self)
        self.configure_styles()

        # Создаём основной фрейм (заполняет всё окно)
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Левый фрейм: “баннер”
        self.banner_frame = ttk.Frame(self.main_frame, style="Banner.TFrame")
        self.banner_frame.pack(side="left", fill="both", expand=True)

        # Правый фрейм: блок с формой
        self.form_frame = ttk.Frame(self.main_frame, style="FormArea.TFrame")
        self.form_frame.pack(side="right", fill="both", expand=True)

        # Заполняем баннер-контентом
        self.create_banner()

        # Создаём саму форму авторизации
        self.create_login_form()

    def configure_styles(self):
        self.style.theme_use("clam")

        # Левый фрейм (баннер) — светло-коричневый фон
        self.style.configure(
            "Banner.TFrame",
            background="#A1887F"
        )

        # Правый фрейм (форма) — светло-серый
        self.style.configure(
            "FormArea.TFrame",
            background="#F5F5F5"
        )

        # Заголовок в баннере (коричневый шрифт)
        self.style.configure(
            "BannerTitle.TLabel",
            background="#A1887F",
            foreground="#3E2723",
            font=("Arial", 18, "bold")
        )

        # Надписи в форме
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

        # Кнопка «Войти» — коричневая
        self.style.configure(
            "Login.TButton",
            font=("Arial", 12, "bold"),
            foreground="#FFFFFF",
            background="#5D4037",
            padding=(10, 6)
        )
        self.style.map(
            "Login.TButton",
            background=[("active", "#4E342E")]
        )

        # Заголовок «Авторизация» на форме
        self.style.configure(
            "FormTitle.TLabel",
            background="#F5F5F5",
            foreground="#3E2723",
            font=("Arial", 16, "bold")
        )

    def create_banner(self):
        lbl_title = ttk.Label(
            self.banner_frame,
            text="Добро\nпожаловать\nв HotelApp",
            style="BannerTitle.TLabel",
            anchor="center"
        )
        lbl_title.place(relx=0.5, rely=0.5, anchor="center")

    def create_login_form(self):
        # Заголовок «Авторизация»
        label_form_title = ttk.Label(
            self.form_frame,
            text="Авторизация",
            style="FormTitle.TLabel"
        )
        label_form_title.pack(pady=(30, 10))

        # Фрейм для полей
        fields_frame = ttk.Frame(self.form_frame, style="FormArea.TFrame")
        fields_frame.pack(pady=10, padx=30, fill="x")

        # Логин
        lbl_login = ttk.Label(fields_frame, text="Логин:", style="Regular.TLabel")
        lbl_login.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.txt_login = ttk.Entry(fields_frame, style="Regular.TEntry")
        self.txt_login.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # Пароль
        lbl_password = ttk.Label(fields_frame, text="Пароль:", style="Regular.TLabel")
        lbl_password.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.txt_password = ttk.Entry(fields_frame, style="Regular.TEntry", show="*")
        self.txt_password.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        fields_frame.columnconfigure(1, weight=1)

        # Кнопка "Войти"
        btn_login = ttk.Button(self.form_frame, text="Войти", style="Login.TButton", command=self.on_login)
        btn_login.pack(pady=20)

        # Переход фокуса на пароль по Enter
        self.txt_login.bind("<Return>", lambda e: self.txt_password.focus())
        self.txt_password.bind("<Return>", lambda e: self.on_login())

    def on_login(self):
        login = self.txt_login.get().strip()
        password = self.txt_password.get().strip()

        if not login or not password:
            messagebox.showerror("Ошибка", "Поля 'Логин' и 'Пароль' обязательны для заполнения.")
            return

        user_data, error = self.user_model.verify_user(login, password)
        if error:
            messagebox.showerror("Ошибка", error)
            return

        messagebox.showinfo("Информация", "Вы успешно авторизовались.")

        # Если нужно сменить пароль (password_changed=False)
        if not user_data["password_changed"]:
            change_password_form = ChangePasswordForm(self, user_data["login"])
            change_password_form.grab_set()
            self.wait_window(change_password_form)

        # Если роль — администратор
        if user_data["role"] == "Администратор":
            admin_form = AdminForm(self)
            admin_form.grab_set()
            self.withdraw()