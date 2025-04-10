# File path: forms/guests_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.guests import Guest

class GuestForm(tk.Toplevel):
    def __init__(self, parent, guest_id=None):
        """
        :param parent: родительское окно (AdminForm)
        :param guest_id: None => добавление, иначе => редактирование
        """
        super().__init__(parent)
        self.guest_model = Guest()
        self.guest_id = guest_id

        if self.guest_id is None:
            self.title("Добавление гостя")
        else:
            self.title("Редактирование гостя")

        self.geometry("400x250")
        self.minsize(400, 250)
        self.resizable(True, True)

        self.style = ttk.Style(self)
        self.configure_styles()

        self.main_frame = ttk.Frame(self, style="FormArea.TFrame")
        self.main_frame.pack(fill="both", expand=True)

        self.create_form()

        if self.guest_id is not None:
            self.load_guest_data()

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

        ttk.Label(fields_frame, text="Паспорт:", style="Regular.TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.txt_passport = ttk.Entry(fields_frame, style="Regular.TEntry")
        self.txt_passport.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        if self.guest_id is None:
            btn_text = "Добавить"
        else:
            btn_text = "Сохранить изменения"

        btn_save = ttk.Button(fields_frame, text=btn_text, style="SaveButton.TButton", command=self.on_save)
        btn_save.grid(row=2, column=0, columnspan=2, pady=15)

        fields_frame.columnconfigure(1, weight=1)

    def load_guest_data(self):
        all_guests = self.guest_model.get_all_guests()
        guest_data = next((g for g in all_guests if g[0] == self.guest_id), None)
        if not guest_data:
            messagebox.showerror("Ошибка", f"Гость с ID={self.guest_id} не найден.")
            self.destroy()
            return

        # guest_data = (id, fullname, passportdata)
        self.txt_fullname.insert(0, guest_data[1])
        self.txt_passport.insert(0, guest_data[2])

    def on_save(self):
        fullname = self.txt_fullname.get().strip()
        passport = self.txt_passport.get().strip()

        if not fullname or not passport:
            messagebox.showerror("Ошибка", "Все поля обязательны.")
            return

        if self.guest_id is None:
            # Добавление
            success, msg = self.guest_model.add_guest(fullname, passport)
        else:
            # Редактирование
            success, msg = self.guest_model.update_guest(self.guest_id, fullname, passport)

        if success:
            messagebox.showinfo("Информация", msg)
            self.destroy()
        else:
            messagebox.showerror("Ошибка", msg)