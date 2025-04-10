# File path: forms/staff_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.staff import Staff
from forms.role_staff_form import RoleStaffForm

class StaffForm(tk.Toplevel):
    def __init__(self, parent, staff_id=None):
        super().__init__(parent)
        self.staff_model = Staff()
        self.staff_id = staff_id
        self.refresh_roles()  # получаем список ролей из БД

        if self.staff_id is None:
            self.title("Добавление сотрудника")
        else:
            self.title("Редактирование сотрудника")

        self.geometry("400x250")
        self.minsize(400, 250)
        self.resizable(True, True)

        self.style = ttk.Style(self)
        self.configure_styles()

        self.main_frame = ttk.Frame(self, style="FormArea.TFrame")
        self.main_frame.pack(fill="both", expand=True)

        self.create_form()

        if self.staff_id is not None:
            self.load_staff_data()

    def refresh_roles(self):
        # Получаем роли для сотрудников: метод get_staff_roles() должен возвращать
        # только те роли из таблицы, которые предназначены для сотрудников (например,
        # исключая 'Администратор' и 'Пользователь').
        self.roles = self.staff_model.get_staff_roles()

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

        ttk.Label(fields_frame, text="ФИО:", style="Regular.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.txt_fullname = ttk.Entry(fields_frame, style="Regular.TEntry")
        self.txt_fullname.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        ttk.Label(fields_frame, text="Роль:", style="Regular.TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        role_names = [r[1] for r in self.roles]
        self.cmb_role = tk.StringVar()
        if role_names:
            self.cmb_role.set(role_names[0])
        else:
            self.cmb_role.set("Нет доступных ролей")

        self.role_dropdown = ttk.OptionMenu(fields_frame, self.cmb_role, self.cmb_role.get(), *role_names)
        self.role_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # Кнопка для создания новой роли
        btn_create_role = ttk.Button(fields_frame, text="Создать роль", command=self.open_role_form)
        btn_create_role.grid(row=1, column=2, padx=5, pady=5)

        if self.staff_id is None:
            btn_text = "Добавить"
        else:
            btn_text = "Сохранить изменения"

        btn_save = ttk.Button(fields_frame, text=btn_text, style="SaveButton.TButton", command=self.on_save)
        btn_save.grid(row=2, column=0, columnspan=3, pady=15)

        fields_frame.columnconfigure(1, weight=1)

    def open_role_form(self):
        form = RoleStaffForm(self)
        form.grab_set()
        self.wait_window(form)
        # После закрытия формы обновляем список ролей и меню выпадающего списка:
        self.refresh_roles()
        role_names = [r[1] for r in self.roles]
        menu = self.role_dropdown["menu"]
        menu.delete(0, 'end')
        for name in role_names:
            menu.add_command(label=name, command=lambda value=name: self.cmb_role.set(value))
        if role_names:
            self.cmb_role.set(role_names[0])
        else:
            self.cmb_role.set("Нет доступных ролей")

    def load_staff_data(self):
        all_staff = self.staff_model.get_all_staff()
        st_data = next((s for s in all_staff if s[0] == self.staff_id), None)
        if not st_data:
            messagebox.showerror("Ошибка", f"Сотрудник с ID={self.staff_id} не найден.")
            self.destroy()
            return
        # st_data = (id, fullname, rolename)
        self.txt_fullname.insert(0, st_data[1])
        role_name = st_data[2]
        self.cmb_role.set(role_name)

    def on_save(self):
        fullname = self.txt_fullname.get().strip()
        selected_role_name = self.cmb_role.get()
        if not fullname or not selected_role_name:
            messagebox.showerror("Ошибка", "Все поля обязательны.")
            return
        role_id = next((r[0] for r in self.roles if r[1] == selected_role_name), None)
        if role_id is None:
            messagebox.showerror("Ошибка", "Выбрана некорректная роль.")
            return
        if self.staff_id is None:
            success, msg = self.staff_model.add_staff(fullname, role_id)
        else:
            success, msg = self.staff_model.update_staff(self.staff_id, fullname, role_id)
        if success:
            messagebox.showinfo("Информация", msg)
            self.destroy()
        else:
            messagebox.showerror("Ошибка", msg)
