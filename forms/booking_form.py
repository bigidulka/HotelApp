# File path: forms/booking_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.booking import Booking

class BookingForm(tk.Toplevel):
    def __init__(self, parent, booking_id=None):
        super().__init__(parent)
        self.booking_model = Booking()
        self.booking_id = booking_id

        if self.booking_id is None:
            self.title("Добавление бронирования")
        else:
            self.title("Редактирование бронирования")

        self.geometry("400x300")
        self.minsize(400, 300)
        self.resizable(True, True)

        self.style = ttk.Style(self)
        self.configure_styles()

        self.main_frame = ttk.Frame(self, style="FormArea.TFrame")
        self.main_frame.pack(fill="both", expand=True)

        self.create_form()

        if self.booking_id is not None:
            self.load_booking_data()

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

        ttk.Label(fields_frame, text="RoomID:", style="Regular.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.txt_roomid = ttk.Entry(fields_frame, style="Regular.TEntry")
        self.txt_roomid.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        ttk.Label(fields_frame, text="GuestID:", style="Regular.TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.txt_guestid = ttk.Entry(fields_frame, style="Regular.TEntry")
        self.txt_guestid.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        ttk.Label(fields_frame, text="Checkin (YYYY-MM-DD):", style="Regular.TLabel").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.txt_checkin = ttk.Entry(fields_frame, style="Regular.TEntry")
        self.txt_checkin.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        ttk.Label(fields_frame, text="Checkout (YYYY-MM-DD):", style="Regular.TLabel").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.txt_checkout = ttk.Entry(fields_frame, style="Regular.TEntry")
        self.txt_checkout.grid(row=3, column=1, padx=5, pady=5, sticky="we")

        if self.booking_id is None:
            btn_text = "Добавить"
        else:
            btn_text = "Сохранить изменения"

        btn_save = ttk.Button(fields_frame, text=btn_text, style="SaveButton.TButton", command=self.on_save)
        btn_save.grid(row=4, column=0, columnspan=2, pady=15)

        fields_frame.columnconfigure(1, weight=1)

    def load_booking_data(self):
        all_bookings = self.booking_model.get_all_bookings()
        bk_data = next((b for b in all_bookings if b[0] == self.booking_id), None)
        if not bk_data:
            messagebox.showerror("Ошибка", f"Бронирование с ID={self.booking_id} не найдено.")
            self.destroy()
            return

        # bk_data = (id, roomid, guestid, checkindate, checkoutdate)
        self.txt_roomid.insert(0, str(bk_data[1]))
        self.txt_guestid.insert(0, str(bk_data[2]))
        self.txt_checkin.insert(0, str(bk_data[3]))
        self.txt_checkout.insert(0, str(bk_data[4]))

    def on_save(self):
        roomid_str = self.txt_roomid.get().strip()
        guestid_str = self.txt_guestid.get().strip()
        checkin_date = self.txt_checkin.get().strip()
        checkout_date = self.txt_checkout.get().strip()

        if not roomid_str or not guestid_str or not checkin_date or not checkout_date:
            messagebox.showerror("Ошибка", "Все поля обязательны.")
            return

        try:
            room_id = int(roomid_str)
            guest_id = int(guestid_str)
        except ValueError:
            messagebox.showerror("Ошибка", "RoomID и GuestID должны быть числами.")
            return

        if self.booking_id is None:
            # Добавление
            success, msg = self.booking_model.add_booking(room_id, guest_id, checkin_date, checkout_date)
        else:
            # Редактирование
            success, msg = self.booking_model.update_booking(self.booking_id, room_id, guest_id, checkin_date, checkout_date)

        if success:
            messagebox.showinfo("Информация", msg)
            self.destroy()
        else:
            messagebox.showerror("Ошибка", msg)