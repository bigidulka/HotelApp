# File path: models/rooms.py
import psycopg2

class Room:
    def __init__(self):
        # Установите свою строку подключения к PostgreSQL (как в User)
        self.connection_string = "host=localhost port=5432 dbname=hotel user=postgres password=postgres"

    def connect(self):
        try:
            return psycopg2.connect(self.connection_string)
        except psycopg2.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return None

    def get_all_rooms(self):
        """
        Возвращает список всех номеров (id, floor, category, statusid, roomnumber).
        """
        conn = self.connect()
        if not conn:
            return []

        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, floor, category, statusid, roomnumber FROM rooms ORDER BY id")
                return cur.fetchall()  # список кортежей
        finally:
            conn.close()

    def add_room(self, floor, category, statusid, roomnumber):
        """
        Добавление нового номера.
        Проверяем, нет ли уже такого roomnumber при том же этаже (или любой другой вашей логики).
        """
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                # Пример простой проверки на существующий roomnumber:
                cur.execute("""
                    SELECT COUNT(*) FROM rooms WHERE roomnumber = %s AND floor = %s
                """, (roomnumber, floor))
                if cur.fetchone()[0] > 0:
                    return False, "Номер с таким номером и этажом уже существует."

                cur.execute("""
                    INSERT INTO rooms (floor, category, statusid, roomnumber)
                    VALUES (%s, %s, %s, %s)
                """, (floor, category, statusid, roomnumber))
                conn.commit()
                return True, "Номер успешно добавлен."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()

    def update_room(self, room_id, floor, category, statusid, roomnumber):
        """
        Обновление данных конкретного номера (по id).
        """
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                # Проверка на дубликаты (например, тот же roomnumber/floor, исключая текущий room_id)
                cur.execute("""
                    SELECT COUNT(*) FROM rooms
                    WHERE roomnumber = %s AND floor = %s AND id != %s
                """, (roomnumber, floor, room_id))
                if cur.fetchone()[0] > 0:
                    return False, "Такой номер (этаж + номер комнаты) уже существует."

                cur.execute("""
                    UPDATE rooms
                    SET floor = %s,
                        category = %s,
                        statusid = %s,
                        roomnumber = %s
                    WHERE id = %s
                """, (floor, category, statusid, roomnumber, room_id))
                conn.commit()
                return True, "Данные номера обновлены."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()

    def delete_room(self, room_id):
        """
        Удаление номера (по id).
        """
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM rooms WHERE id = %s", (room_id,))
                conn.commit()
                return True, "Номер успешно удалён."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()
