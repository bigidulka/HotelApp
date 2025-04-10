# File path: forms/staff_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.staff import Staff

class StaffForm(tk.Toplevel):
    def __init__(self, parent, staff_id=None):
        super().__init__(parent)
        self.staff_model = Staff()
        self.staff_id = staff_id

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

        ttk.Label(fields_frame, text="RoleID:", style="Regular.TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.txt_roleid = ttk.Entry(fields_frame, style="Regular.TEntry")
        self.txt_roleid.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        if self.staff_id is None:
            btn_text = "Добавить"
        else:
            btn_text = "Сохранить изменения"

        btn_save = ttk.Button(fields_frame, text=btn_text, style="SaveButton.TButton", command=self.on_save)
        btn_save.grid(row=2, column=0, columnspan=2, pady=15)

        fields_frame.columnconfigure(1, weight=1)

    def load_staff_data(self):
        all_staff = self.staff_model.get_all_staff()
        st_data = next((s for s in all_staff if s[0] == self.staff_id), None)
        if not st_data:
            messagebox.showerror("Ошибка", f"Сотрудник с ID={self.staff_id} не найден.")
            self.destroy()
            return

        # st_data = (id, fullname, roleid)
        self.txt_fullname.insert(0, st_data[1])
        self.txt_roleid.insert(0, str(st_data[2]))

    def on_save(self):
        fullname = self.txt_fullname.get().strip()
        roleid_str = self.txt_roleid.get().strip()

        if not fullname or not roleid_str:
            messagebox.showerror("Ошибка", "Все поля обязательны.")
            return

        try:
            role_id = int(roleid_str)
        except ValueError:
            messagebox.showerror("Ошибка", "RoleID должен быть числом.")
            return

        if self.staff_id is None:
            # Добавление
            success, msg = self.staff_model.add_staff(fullname, role_id)
        else:
            # Редактирование
            success, msg = self.staff_model.update_staff(self.staff_id, fullname, role_id)

        if success:
            messagebox.showinfo("Информация", msg)
            self.destroy()
        else:
            messagebox.showerror("Ошибка", msg)