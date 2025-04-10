# File path: models/booking.py
import psycopg2

class Booking:
    def __init__(self):
        self.connection_string = "host=localhost port=5432 dbname=hotel user=postgres password=postgres"

    def connect(self):
        try:
            return psycopg2.connect(self.connection_string)
        except psycopg2.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return None

    def get_all_bookings(self):
        """
        Возвращает список всех бронирований (id, roomid, guestid, checkindate, checkoutdate).
        """
        conn = self.connect()
        if not conn:
            return []

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, roomid, guestid, checkindate, checkoutdate
                    FROM bookings
                    ORDER BY id
                """)
                return cur.fetchall()
        finally:
            conn.close()

    def add_booking(self, room_id, guest_id, checkin_date, checkout_date):
        """
        Добавляем новое бронирование.
        """
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"
        try:
            with conn.cursor() as cur:
                # Пример: можно проверить пересечения дат, занятость комнаты и т.д.
                cur.execute("""
                    INSERT INTO bookings (roomid, guestid, checkindate, checkoutdate)
                    VALUES (%s, %s, %s, %s)
                """, (room_id, guest_id, checkin_date, checkout_date))
                conn.commit()
                return True, "Бронирование успешно добавлено."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()

    def update_booking(self, booking_id, room_id, guest_id, checkin_date, checkout_date):
        """
        Обновление бронирования по ID.
        """
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE bookings
                    SET roomid = %s,
                        guestid = %s,
                        checkindate = %s,
                        checkoutdate = %s
                    WHERE id = %s
                """, (room_id, guest_id, checkin_date, checkout_date, booking_id))
                if cur.rowcount == 0:
                    return False, f"Бронирование с ID={booking_id} не найдено."
                conn.commit()
                return True, "Данные бронирования обновлены."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()

    def delete_booking(self, booking_id):
        """
        Удаление бронирования по ID.
        """
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
                if cur.rowcount == 0:
                    return False, f"Бронирование с ID={booking_id} не найдено."
                conn.commit()
                return True, "Бронирование успешно удалено."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()
