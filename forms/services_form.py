# File path: forms/services_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.services import Services

class ServiceForm(tk.Toplevel):
    def __init__(self, parent, service_id=None):
        super().__init__(parent)
        self.services_model = Services()
        self.service_id = service_id

        if self.service_id is None:
            self.title("Добавление услуги")
        else:
            self.title("Редактирование услуги")

        self.geometry("400x250")
        self.minsize(400, 250)
        self.resizable(True, True)

        self.style = ttk.Style(self)
        self.configure_styles()

        self.main_frame = ttk.Frame(self, style="FormArea.TFrame")
        self.main_frame.pack(fill="both", expand=True)

        self.create_form()

        if self.service_id is not None:
            self.load_service_data()

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

        ttk.Label(fields_frame, text="Название услуги:", style="Regular.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.txt_servicename = ttk.Entry(fields_frame, style="Regular.TEntry")
        self.txt_servicename.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        ttk.Label(fields_frame, text="Цена:", style="Regular.TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.txt_price = ttk.Entry(fields_frame, style="Regular.TEntry")
        self.txt_price.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        if self.service_id is None:
            btn_text = "Добавить"
        else:
            btn_text = "Сохранить изменения"

        btn_save = ttk.Button(fields_frame, text=btn_text, style="SaveButton.TButton", command=self.on_save)
        btn_save.grid(row=2, column=0, columnspan=2, pady=15)

        fields_frame.columnconfigure(1, weight=1)

    def load_service_data(self):
        all_services = self.services_model.get_all_services()
        svc_data = next((s for s in all_services if s[0] == self.service_id), None)
        if not svc_data:
            messagebox.showerror("Ошибка", f"Услуга с ID={self.service_id} не найдена.")
            self.destroy()
            return

        # svc_data = (id, servicename, price)
        self.txt_servicename.insert(0, svc_data[1])
        self.txt_price.insert(0, str(svc_data[2]))

    def on_save(self):
        servicename = self.txt_servicename.get().strip()
        price_str = self.txt_price.get().strip()

        if not servicename or not price_str:
            messagebox.showerror("Ошибка", "Все поля обязательны.")
            return

        # Попробуем float
        try:
            price_val = float(price_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Цена должна быть числом (например, 300.00).")
            return

        if self.service_id is None:
            # Добавление
            success, msg = self.services_model.add_service(servicename, price_val)
        else:
            # Редактирование
            success, msg = self.services_model.update_service(self.service_id, servicename, price_val)

        if success:
            messagebox.showinfo("Информация", msg)
            self.destroy()
        else:
            messagebox.showerror("Ошибка", msg)