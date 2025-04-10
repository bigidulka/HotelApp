# File path: forms/user_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.user import User

class UserForm(tk.Toplevel):
    def __init__(self, parent, user_id=None):
        """
        :param parent: родительское окно (AdminForm)
        :param user_id: если None -> режим добавления, иначе -> режим редактирования пользователя
        """
        super().__init__(parent)
        self.user_model = User()
        self.user_id = user_id  # None или int
        
        self.roles = self.user_model.get_roles()

        # Заголовок окна в зависимости от режима
        if self.user_id is None:
            self.title("Добавление пользователя - HotelApp")
        else:
            self.title("Редактирование пользователя - HotelApp")

        self.geometry("400x350")
        self.minsize(400, 350)
        self.resizable(True, True)

        # Настраиваем стили
        self.style = ttk.Style(self)
        self.configure_styles()

        # Основной фрейм
        self.main_frame = ttk.Frame(self, style="FormArea.TFrame")
        self.main_frame.pack(fill="both", expand=True)

        # Создаём форму
        self.create_form()

        # Если user_id не None, значит редактируем — загружаем данные пользователя
        if self.user_id is not None:
            self.load_user_data()

    def configure_styles(self):
        self.style.theme_use("clam")
        self.style.configure("FormArea.TFrame", background="#F5F5F5")
        self.style.configure("Regular.TLabel", background="#F5F5F5", foreground="#333333", font=("Arial", 11))
        self.style.configure("Regular.TEntry", font=("Arial", 11), padding=5)
        self.style.configure("SaveButton.TButton", font=("Arial", 11, "bold"),
                             foreground="#FFFFFF", background="#5D4037", padding=(10, 5))
        self.style.map("SaveButton.TButton", background=[("active", "#4E342E")])

    def create_form(self):
        fields_frame = ttk.Frame(self.main_frame, style="FormArea.TFrame")
        fields_frame.pack(padx=20, pady=20, fill="x", expand=True)

        # Логин
        ttk.Label(fields_frame, text="Логин:", style="Regular.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.txt_login = ttk.Entry(fields_frame, style="Regular.TEntry")
        self.txt_login.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # Пароль
        ttk.Label(fields_frame, text="Пароль:", style="Regular.TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.txt_password = ttk.Entry(fields_frame, show="*", style="Regular.TEntry")
        self.txt_password.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # Роль
        ttk.Label(fields_frame, text="Роль:", style="Regular.TLabel").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        # Для упрощения две роли, можно добавить больше
        role_names = [r[1] for r in self.roles]  # Только имена
        self.cmb_role = tk.StringVar()
        role_dropdown = ttk.OptionMenu(fields_frame, self.cmb_role, role_names[0], *role_names)
        role_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        # Кнопка «Сохранить»
        if self.user_id is None:
            btn_text = "Добавить"
        else:
            btn_text = "Сохранить изменения"

        btn_save = ttk.Button(fields_frame, text=btn_text, style="SaveButton.TButton", command=self.on_save)
        btn_save.grid(row=3, column=0, columnspan=2, pady=15)

        fields_frame.columnconfigure(1, weight=1)

    def load_user_data(self):
        """
        Загружаем данные о пользователе (логин, роль).
        В реальном проекте желательно иметь get_user_by_id, но можно обойтись get_all_users + фильтр.
        """
        all_users = self.user_model.get_all_users()  # [(id, login, role, isBlocked), ...]
        user_data = next((u for u in all_users if u[0] == self.user_id), None)
        if not user_data:
            messagebox.showerror("Ошибка", f"Пользователь с ID={self.user_id} не найден.")
            self.destroy()
            return

        # user_data = (UserID, Login, rolename, IsBlocked)
        # Пароль мы обычно не отображаем (или не знаем), так что txt_password оставим пустым
        login = user_data[1]
        role = user_data[2]

        self.txt_login.insert(0, login)
        self.cmb_role.set(role)
        # Пароль не загружаем, т.к. он хранится в хэшированном виде (или вообще не нужен)

    def on_save(self):
        """
        1) Считываем поля (login, password, role)
        2) Находим role_id по имени роли
        3) Если self.user_id is None -> add_user, иначе -> update_user
        4) Закрываем окно при успехе
        """
        login = self.txt_login.get().strip()
        password = self.txt_password.get().strip()
        selected_role_name = self.cmb_role.get()

        if not login or not selected_role_name:
            messagebox.showerror("Ошибка", "Поля 'Логин' и 'Роль' обязательны для заполнения.")
            return

        # Находим ID роли по её имени
        role_id = next((r[0] for r in self.roles if r[1] == selected_role_name), None)
        if role_id is None:
            messagebox.showerror("Ошибка", "Выбрана некорректная роль.")
            return

        # Определяем, добавляем или обновляем
        if self.user_id is None:
            # Режим добавления
            if not password:
                messagebox.showerror("Ошибка", "При добавлении пароль обязателен.")
                return

            success, msg = self.user_model.add_user(login, password, role_id)
        else:
            # Режим редактирования
            pass_for_update = password if password else None
            success, msg = self.user_model.update_user(self.user_id, login, pass_for_update, role_id)

        if success:
            messagebox.showinfo("Информация", msg)
            self.destroy()
        else:
            messagebox.showerror("Ошибка", msg)
