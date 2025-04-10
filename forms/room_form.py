# File path: forms/room_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.rooms import Room

class RoomForm(tk.Toplevel):
    def __init__(self, parent, room_id=None):
        """
        :param parent: Родительское окно (AdminForm).
        :param room_id: Если None -> добавляем номер, иначе редактируем номер с таким ID.
        """
        super().__init__(parent)
        self.room_model = Room()
        self.room_id = room_id  # None или int

        # Определяем заголовок окна в зависимости от режима
        if self.room_id is None:
            self.title("Добавление номера")
        else:
            self.title("Редактирование номера")

        self.geometry("400x350")
        self.minsize(400, 350)
        self.resizable(True, True)

        self.style = ttk.Style(self)
        self.configure_styles()

        self.main_frame = ttk.Frame(self, style="FormArea.TFrame")
        self.main_frame.pack(fill="both", expand=True)

        self.create_form()

        # Если room_id не None, загружаем существующие данные номера
        if self.room_id is not None:
            self.load_room_data()

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

        # Этаж
        ttk.Label(fields_frame, text="Этаж:", style="Regular.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.txt_floor = ttk.Entry(fields_frame, style="Regular.TEntry")
        self.txt_floor.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # Категория
        ttk.Label(fields_frame, text="Категория:", style="Regular.TLabel").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.txt_category = ttk.Entry(fields_frame, style="Regular.TEntry")
        self.txt_category.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # Статус (ID)
        ttk.Label(fields_frame, text="Статус (ID):", style="Regular.TLabel").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.txt_status = ttk.Entry(fields_frame, style="Regular.TEntry")
        self.txt_status.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        # Номер комнаты
        ttk.Label(fields_frame, text="Номер комнаты:", style="Regular.TLabel").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.txt_roomnumber = ttk.Entry(fields_frame, style="Regular.TEntry")
        self.txt_roomnumber.grid(row=3, column=1, padx=5, pady=5, sticky="we")

        # Кнопка "Сохранить" (или "Добавить")
        if self.room_id is None:
            btn_text = "Добавить"
        else:
            btn_text = "Сохранить изменения"

        btn_save = ttk.Button(fields_frame, text=btn_text, style="SaveButton.TButton", command=self.on_save)
        btn_save.grid(row=4, column=0, columnspan=2, pady=15)

        fields_frame.columnconfigure(1, weight=1)

    def load_room_data(self):
        """
        Загружаем существующие данные о номере, если room_id не None.
        (Если нужно, лучше иметь метод get_room_by_id, но можно обойтись get_all_rooms + фильтрация).
        """
        all_rooms = self.room_model.get_all_rooms()
        room_data = next((r for r in all_rooms if r[0] == self.room_id), None)
        if not room_data:
            messagebox.showerror("Ошибка", f"Номер с ID={self.room_id} не найден.")
            self.destroy()
            return

        # room_data = (id, floor, category, statusid, roomnumber)
        self.txt_floor.insert(0, room_data[1])       # floor
        self.txt_category.insert(0, room_data[2])    # category
        self.txt_status.insert(0, room_data[3])      # statusid
        self.txt_roomnumber.insert(0, room_data[4])  # roomnumber

    def on_save(self):
        """
        1) Считываем поля
        2) Если self.room_id is None -> add_room, иначе update_room
        3) Если успех -> закрываем окно
        """
        floor_str = self.txt_floor.get().strip()
        category = self.txt_category.get().strip()
        status_str = self.txt_status.get().strip()
        roomnumber_str = self.txt_roomnumber.get().strip()

        if not floor_str or not category or not status_str or not roomnumber_str:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения.")
            return

        try:
            floor = int(floor_str)
            status_id = int(status_str)
            room_number = int(roomnumber_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Этаж, статус и номер комнаты должны быть числами.")
            return

        if self.room_id is None:
            # Режим добавления
            success, msg = self.room_model.add_room(floor, category, status_id, room_number)
        else:
            # Режим редактирования
            success, msg = self.room_model.update_room(self.room_id, floor, category, status_id, room_number)

        if success:
            messagebox.showinfo("Информация", msg)
            self.destroy()
        else:
            messagebox.showerror("Ошибка", msg)