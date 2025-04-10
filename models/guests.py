# File path: models/guests.py
import psycopg2

class Guest:
    def __init__(self):
        # Замените строку подключения на вашу
        self.connection_string = "host=localhost port=5432 dbname=hotel user=postgres password=postgres"

    def connect(self):
        try:
            return psycopg2.connect(self.connection_string)
        except psycopg2.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return None

    def get_all_guests(self):
        """
        Возвращает список всех гостей (id, fullname, passportdata).
        """
        conn = self.connect()
        if not conn:
            return []

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, fullname, passportdata
                    FROM guests
                    ORDER BY id
                """)
                return cur.fetchall()  # список кортежей (id, fullname, passportdata)
        finally:
            conn.close()

    def add_guest(self, full_name, passport_data):
        """
        Добавление нового гостя.
        """
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                # Пример (опционально): проверяем, нет ли гостя с таким же паспортом
                cur.execute("""
                    SELECT COUNT(*) FROM guests
                    WHERE passportdata = %s
                """, (passport_data,))
                if cur.fetchone()[0] > 0:
                    return False, "Гость с таким паспортом уже существует."

                cur.execute("""
                    INSERT INTO guests (fullname, passportdata)
                    VALUES (%s, %s)
                """, (full_name, passport_data))
                conn.commit()
                return True, "Гость успешно добавлен."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()

    def update_guest(self, guest_id, full_name, passport_data):
        """
        Обновление данных о госте по ID.
        """
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE guests
                    SET fullname = %s,
                        passportdata = %s
                    WHERE id = %s
                """, (full_name, passport_data, guest_id))
                if cur.rowcount == 0:
                    return False, f"Гость с ID={guest_id} не найден."
                conn.commit()
                return True, "Данные гостя обновлены."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()

    def delete_guest(self, guest_id):
        """
        Удаление гостя по ID.
        """
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM guests WHERE id = %s", (guest_id,))
                if cur.rowcount == 0:
                    return False, f"Гость с ID={guest_id} не найден."
                conn.commit()
                return True, "Гость успешно удалён."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()