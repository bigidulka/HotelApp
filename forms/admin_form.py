# File path: forms/admin_form.py
import tkinter as tk
from tkinter import ttk, messagebox

from models.user import User
from models.rooms import Room
from models.guests import Guest
from models.staff import Staff
from models.booking import Booking
from models.services import Services

class AdminForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Панель администратора - HotelApp")
        self.geometry("900x600")
        self.minsize(800, 500)
        self.resizable(True, True)

        self.user_model = User()
        self.room_model = Room()
        self.guest_model = Guest()
        self.staff_model = Staff()
        self.booking_model = Booking()
        self.services_model = Services()

        # Текущий режим
        self.current_mode = None

        # Стили
        self.style = ttk.Style(self)
        self.configure_styles()

        # Основной фрейм
        self.main_frame = ttk.Frame(self, style="Admin.TFrame")
        self.main_frame.pack(fill="both", expand=True)

        # Верхняя панель с кнопками (для переключения между сущностями)
        self.create_top_buttons()

        # Фрейм для таблицы
        self.table_frame = ttk.Frame(self.main_frame, style="Admin.TFrame")
        self.table_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Прокрутка
        self.scrollbar_y = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.scrollbar_y.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            self.table_frame,
            style="Admin.Treeview",
            columns=(),
            show="headings",
            yscrollcommand=self.scrollbar_y.set
        )
        self.tree.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.config(command=self.tree.yview)

        # Фрейм для кнопок внизу
        self.buttons_frame = ttk.Frame(self.main_frame, style="Admin.TFrame")
        self.buttons_frame.pack(side="bottom", fill="x", padx=10, pady=(0,10))

        # По умолчанию «Пользователи»
        self.switch_to_users()
        
    # Стиль
    def configure_styles(self):
        self.style.theme_use("clam")

        self.style.configure(
            "Admin.TFrame",
            background="#F5F5F5"
        )
        self.style.configure(
            "Admin.TButton",
            font=("Arial", 11, "bold"),
            foreground="#FFFFFF",
            background="#5D4037",
            padding=(10, 5)
        )
        self.style.map(
            "Admin.TButton",
            background=[("active", "#4E342E")]
        )
        self.style.configure(
            "Admin.Treeview",
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            rowheight=24,
            font=("Arial", 10)
        )
        self.style.configure(
            "Admin.Treeview.Heading",
            font=("Arial", 10, "bold"),
            background="#F5F5F5",
            foreground="#3E2723"
        )

    # Панель с кнопками для переключения
    def create_top_buttons(self):
        top_frame = ttk.Frame(self.main_frame, style="Admin.TFrame")
        top_frame.pack(side="top", fill="x")

        btn_users = ttk.Button(top_frame, text="Пользователи", style="Admin.TButton", command=self.switch_to_users)
        btn_users.pack(side="left", padx=5, pady=5)

        btn_rooms = ttk.Button(top_frame, text="Номера", style="Admin.TButton", command=self.switch_to_rooms)
        btn_rooms.pack(side="left", padx=5, pady=5)

        btn_guests = ttk.Button(top_frame, text="Гости", style="Admin.TButton", command=self.switch_to_guests)
        btn_guests.pack(side="left", padx=5, pady=5)

        btn_staff = ttk.Button(top_frame, text="Персонал", style="Admin.TButton", command=self.switch_to_staff)
        btn_staff.pack(side="left", padx=5, pady=5)

        btn_bookings = ttk.Button(top_frame, text="Бронирования", style="Admin.TButton", command=self.switch_to_bookings)
        btn_bookings.pack(side="left", padx=5, pady=5)

        btn_services = ttk.Button(top_frame, text="Услуги", style="Admin.TButton", command=self.switch_to_services)
        btn_services.pack(side="left", padx=5, pady=5)

    # Пользователи
    def switch_to_users(self):
        self.current_mode = "users"
        # Настройка столбцов
        self.tree["columns"] = ("ID", "Login", "Role", "IsBlocked")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Login", text="Логин")
        self.tree.heading("Role", text="Роль")
        self.tree.heading("IsBlocked", text="Заблокирован")

        self.tree.column("ID", width=50)
        self.tree.column("Login", width=150)
        self.tree.column("Role", width=120)
        self.tree.column("IsBlocked", width=100)

        # Загрузка пользователей
        self.load_users()

        # Кнопки внизу
        self.init_user_buttons()

    def load_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        users = self.user_model.get_all_users()
        for user in users:
            self.tree.insert("", tk.END, values=user)

    def init_user_buttons(self):
        for w in self.buttons_frame.winfo_children():
            w.destroy()

        btn_add = ttk.Button(self.buttons_frame, text="Добавить пользователя", style="Admin.TButton", command=self.on_add_user)
        btn_add.pack(fill="x", pady=2)

        btn_edit = ttk.Button(self.buttons_frame, text="Изменить пользователя", style="Admin.TButton", command=self.on_edit_user)
        btn_edit.pack(fill="x", pady=2)

        btn_unblock = ttk.Button(self.buttons_frame, text="Снять блокировку", style="Admin.TButton", command=self.on_unblock_user)
        btn_unblock.pack(fill="x", pady=2)
        
        btn_block = ttk.Button(self.buttons_frame, text="Заблокировать пользователя", style="Admin.TButton", command=self.on_block_user)
        btn_block.pack(fill="x", pady=2)
        
    def on_block_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите пользователя для блокировки.")
            return

        user_id = self.tree.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("Подтверждение", f"Точно заблокировать пользователя ID={user_id}?")
        if not confirm:
            return

        success, msg = self.user_model.block_user_by_id(user_id)
        if success:
            messagebox.showinfo("Информация", msg)
            self.load_users()
        else:
            messagebox.showerror("Ошибка", msg)


    def on_add_user(self):
        from forms.user_form import UserForm
        form = UserForm(self, user_id=None)  # Режим добавления
        form.grab_set()
        self.wait_window(form)
        self.load_users()  # Обновление таблицы

    def on_edit_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите пользователя для редактирования.")
            return

        user_id = self.tree.item(selected_item)["values"][0] 

        from forms.user_form import UserForm
        form = UserForm(self, user_id=user_id)  # Режим редактирования
        form.grab_set()
        self.wait_window(form)
        self.load_users()
        
    def on_delete_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите пользователя для удаления.")
            return

        user_id = self.tree.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("Подтверждение", f"Точно удалить пользователя ID={user_id}?")
        if not confirm:
            return

        success, msg = self.user_model.delete_user(user_id)
        if success:
            messagebox.showinfo("Информация", msg)
            self.load_users()
        else:
            messagebox.showerror("Ошибка", msg)

    def on_unblock_user(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите пользователя для снятия блокировки.")
            return
        user_id = self.tree.item(selected_item)["values"][0]
        messagebox.showinfo("Информация", f"Снятие блокировки с пользователя ID={user_id}")
        success, msg = self.user_model.unblock_user(user_id)
        if success:
            messagebox.showinfo("Информация", msg)
            self.load_users()
        else:
            messagebox.showerror("Ошибка", msg)

    # Номера
    def switch_to_rooms(self):
        self.current_mode = "rooms"

        self.tree["columns"] = ("ID", "Floor", "Category", "StatusID", "RoomNumber")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Floor", text="Этаж")
        self.tree.heading("Category", text="Категория")
        self.tree.heading("StatusID", text="Статус")
        self.tree.heading("RoomNumber", text="Номер")

        self.tree.column("ID", width=50)
        self.tree.column("Floor", width=60)
        self.tree.column("Category", width=150)
        self.tree.column("StatusID", width=60)
        self.tree.column("RoomNumber", width=100)

        self.load_rooms()
        self.init_room_buttons()

    def load_rooms(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        rooms = self.room_model.get_all_rooms()
        if not rooms:
            return 

        for room in rooms:
            self.tree.insert("", tk.END, values=room)

    def init_room_buttons(self):
        for w in self.buttons_frame.winfo_children():
            w.destroy()

        btn_add = ttk.Button(self.buttons_frame, text="Добавить номер", style="Admin.TButton", command=self.on_add_room)
        btn_add.pack(fill="x", pady=2)

        btn_edit = ttk.Button(self.buttons_frame, text="Изменить номер", style="Admin.TButton", command=self.on_edit_room)
        btn_edit.pack(fill="x", pady=2)

        btn_delete = ttk.Button(self.buttons_frame, text="Удалить номер", style="Admin.TButton", command=self.on_delete_room)
        btn_delete.pack(fill="x", pady=2)

    def on_add_room(self):
        from forms.room_form import RoomForm
        form = RoomForm(self, room_id=None)  # Режим добавления
        form.grab_set()
        self.wait_window(form)
        self.load_rooms()

    def on_edit_room(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите номер для редактирования.")
            return
        room_id = self.tree.item(selected_item)["values"][0]

        from forms.room_form import RoomForm
        form = RoomForm(self, room_id=room_id)  # Режим редактирования
        form.grab_set()
        self.wait_window(form)
        self.load_rooms()

    def on_delete_room(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите номер для удаления.")
            return

        room_id = self.tree.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("Подтверждение", f"Точно удалить номер ID={room_id}?")
        if not confirm:
            return

        success, msg = self.room_model.delete_room(room_id)
        if success:
            messagebox.showinfo("Информация", msg)
            self.load_rooms()
        else:
            messagebox.showerror("Ошибка", msg)

    # Гости
    def switch_to_guests(self):
        self.current_mode = "guests"

        self.tree["columns"] = ("ID", "FullName", "PassportData")
        self.tree.heading("ID", text="ID")
        self.tree.heading("FullName", text="ФИО")
        self.tree.heading("PassportData", text="Паспорт")

        self.tree.column("ID", width=50)
        self.tree.column("FullName", width=200)
        self.tree.column("PassportData", width=120)

        self.load_guests()
        self.init_guest_buttons()
        
    def load_guests(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        guests = self.guest_model.get_all_guests()
        if not guests:
            return

        for guests in guests:
            self.tree.insert("", tk.END, values=guests)

    def init_guest_buttons(self):
        for w in self.buttons_frame.winfo_children():
            w.destroy()

        btn_add = ttk.Button(self.buttons_frame, text="Добавить гостя", style="Admin.TButton", command=self.on_add_guest)
        btn_add.pack(fill="x", pady=2)

        btn_edit = ttk.Button(self.buttons_frame, text="Изменить гостя", style="Admin.TButton", command=self.on_edit_guest)
        btn_edit.pack(fill="x", pady=2)

        btn_delete = ttk.Button(self.buttons_frame, text="Удалить гостя", style="Admin.TButton", command=self.on_delete_guest)
        btn_delete.pack(fill="x", pady=2)
        
    def on_add_guest(self):
        from forms.guests_form import GuestForm
        form = GuestForm(self, guest_id=None)
        form.grab_set()
        self.wait_window(form)
        self.load_guests()

    def on_edit_guest(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите гостя для редактирования.")
            return
        guest_id = self.tree.item(selected_item)["values"][0]

        from forms.guests_form import GuestForm
        form = GuestForm(self, guest_id=guest_id) 
        form.grab_set()
        self.wait_window(form)
        self.load_guests()

    def on_delete_guest(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите гостя для удаления.")
            return

        guest_id = self.tree.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("Подтверждение", f"Точно удалить гостя ID={guest_id}?")
        if not confirm:
            return

        success, msg = self.guest_model.delete_guest(guest_id)
        if success:
            messagebox.showinfo("Информация", msg)
            self.load_guests()
        else:
            messagebox.showerror("Ошибка", msg)
            
    # Персонал
    def switch_to_staff(self):
        self.current_mode = "staff"

        self.tree["columns"] = ("ID", "FullName", "RoleID")
        self.tree.heading("ID", text="ID")
        self.tree.heading("FullName", text="ФИО")
        self.tree.heading("RoleID", text="Роль ID")

        self.tree.column("ID", width=50)
        self.tree.column("FullName", width=200)
        self.tree.column("RoleID", width=80)

        self.load_staff()
        self.init_staff_buttons()

    def load_staff(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        staff = self.staff_model.get_all_staff()
        if not staff:
            return

        for staff in staff:
            self.tree.insert("", tk.END, values=staff)

    def init_staff_buttons(self):
        for w in self.buttons_frame.winfo_children():
            w.destroy()

        btn_add = ttk.Button(self.buttons_frame, text="Добавить сотрудника", style="Admin.TButton", command=self.on_add_staff)
        btn_add.pack(fill="x", pady=2)

        btn_edit = ttk.Button(self.buttons_frame, text="Изменить сотрудника", style="Admin.TButton", command=self.on_edit_staff)
        btn_edit.pack(fill="x", pady=2)

        btn_delete = ttk.Button(self.buttons_frame, text="Удалить сотрудника", style="Admin.TButton", command=self.on_delete_staff)
        btn_delete.pack(fill="x", pady=2)
        
    def on_add_staff(self):
        from forms.staff_form import StaffForm
        form = StaffForm(self, staff_id=None) 
        form.grab_set()
        self.wait_window(form)
        self.load_staff()

    def on_edit_staff(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите работника для редактирования.")
            return
        staff_id = self.tree.item(selected_item)["values"][0]

        from forms.staff_form import StaffForm
        form = StaffForm(self, staff_id=staff_id) 
        form.grab_set()
        self.wait_window(form)
        self.load_staff()

    def on_delete_staff(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите работника для удаления.")
            return

        staff_id = self.tree.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("Подтверждение", f"Точно удалить работника ID={staff_id}?")
        if not confirm:
            return

        success, msg = self.staff_model.delete_staff(staff_id)
        if success:
            messagebox.showinfo("Информация", msg)
            self.load_staff() 
        else:
            messagebox.showerror("Ошибка", msg)

    # Бронирования
    def switch_to_bookings(self):
        self.current_mode = "bookings"

        self.tree["columns"] = ("ID", "RoomID", "GuestID", "CheckinDate", "CheckoutDate")
        self.tree.heading("ID", text="ID")
        self.tree.heading("RoomID", text="Комната")
        self.tree.heading("GuestID", text="Гость")
        self.tree.heading("CheckinDate", text="Заезд")
        self.tree.heading("CheckoutDate", text="Выезд")

        self.tree.column("ID", width=50)
        self.tree.column("RoomID", width=80)
        self.tree.column("GuestID", width=80)
        self.tree.column("CheckinDate", width=100)
        self.tree.column("CheckoutDate", width=100)

        self.load_bookings()
        self.init_booking_buttons()
    
    def load_bookings(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        bookings = self.booking_model.get_all_bookings()
        if not bookings:
            return

        for bookings in bookings:
            self.tree.insert("", tk.END, values=bookings)

    def init_booking_buttons(self):
        for w in self.buttons_frame.winfo_children():
            w.destroy()

        btn_add = ttk.Button(self.buttons_frame, text="Добавить бронирование", style="Admin.TButton", command=self.on_add_booking)
        btn_add.pack(fill="x", pady=2)

        btn_edit = ttk.Button(self.buttons_frame, text="Изменить бронирование", style="Admin.TButton", command=self.on_edit_booking)
        btn_edit.pack(fill="x", pady=2)

        btn_delete = ttk.Button(self.buttons_frame, text="Удалить бронирование", style="Admin.TButton", command=self.on_delete_booking)
        btn_delete.pack(fill="x", pady=2)
        
    def on_add_booking(self):
        from forms.booking_form import BookingForm
        form = BookingForm(self, booking_id=None)
        form.grab_set()
        self.wait_window(form)
        self.load_bookings()

    def on_edit_booking(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите бронирование для редактирования.")
            return
        booking_id = self.tree.item(selected_item)["values"][0]

        from forms.booking_form import BookingForm
        form = BookingForm(self, booking_id=booking_id) 
        form.grab_set()
        self.wait_window(form)
        self.load_bookings()

    def on_delete_booking(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите бронирование для удаления.")
            return

        booking_id = self.tree.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("Подтверждение", f"Точно удалить бронирование ID={booking_id}?")
        if not confirm:
            return

        success, msg = self.booking_model.delete_booking(booking_id)
        if success:
            messagebox.showinfo("Информация", msg)
            self.load_bookings() 
        else:
            messagebox.showerror("Ошибка", msg)

    # Услуги
    def switch_to_services(self):
        self.current_mode = "services"

        self.tree["columns"] = ("ID", "ServiceName", "Price")
        self.tree.heading("ID", text="ID")
        self.tree.heading("ServiceName", text="Услуга")
        self.tree.heading("Price", text="Цена")

        self.tree.column("ID", width=50)
        self.tree.column("ServiceName", width=200)
        self.tree.column("Price", width=80)

        self.load_services()
        self.init_service_buttons()
        
    def load_services(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        services = self.services_model.get_all_services()
        if not services:
            return

        for services in services:
            self.tree.insert("", tk.END, values=services)
        
    def init_service_buttons(self):
        for w in self.buttons_frame.winfo_children():
            w.destroy()

        btn_add = ttk.Button(self.buttons_frame, text="Добавить услугу", style="Admin.TButton", command=self.on_add_service)
        btn_add.pack(fill="x", pady=2)

        btn_edit = ttk.Button(self.buttons_frame, text="Изменить услугу", style="Admin.TButton", command=self.on_edit_service)
        btn_edit.pack(fill="x", pady=2)

        btn_delete = ttk.Button(self.buttons_frame, text="Удалить услугу", style="Admin.TButton", command=self.on_delete_service)
        btn_delete.pack(fill="x", pady=2)
        
    def on_add_service(self):
        from forms.services_form import ServiceForm
        form = ServiceForm(self, service_id=None) 
        form.grab_set()
        self.wait_window(form)
        self.load_services()

    def on_edit_service(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите услугу для редактирования.")
            return
        service_id = self.tree.item(selected_item)["values"][0]

        from forms.services_form import ServiceForm
        form = ServiceForm(self, service_id=service_id)
        form.grab_set()
        self.wait_window(form)
        self.load_services()

    def on_delete_service(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите услугу для удаления.")
            return

        service_id = self.tree.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("Подтверждение", f"Точно удалить услугу ID={service_id}?")
        if not confirm:
            return

        success, msg = self.services_model.delete_service(service_id)
        if success:
            messagebox.showinfo("Информация", msg)
            self.load_services() 
        else:
            messagebox.showerror("Ошибка", msg)