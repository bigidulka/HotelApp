# File path: models/staff.py
import psycopg2

class Staff:
    def __init__(self):
        self.connection_string = "host=localhost port=5432 dbname=hotel user=postgres password=postgres"

    def connect(self):
        try:
            return psycopg2.connect(self.connection_string)
        except psycopg2.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return None

    def get_all_staff(self):
        conn = self.connect()
        if not conn:
            return []

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, fullname, roleid
                    FROM staff
                    ORDER BY id
                """)
                return cur.fetchall()
        finally:
            conn.close()

    def add_staff(self, full_name, role_id):
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                # Пример проверки
                cur.execute("""
                    SELECT COUNT(*) FROM staff
                    WHERE fullname = %s AND roleid = %s
                """, (full_name, role_id))
                if cur.fetchone()[0] > 0:
                    return False, "Такой сотрудник уже существует."

                cur.execute("""
                    INSERT INTO staff (fullname, roleid)
                    VALUES (%s, %s)
                """, (full_name, role_id))
                conn.commit()
                return True, "Сотрудник успешно добавлен."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()

    def update_staff(self, staff_id, full_name, role_id):
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE staff
                    SET fullname = %s,
                        roleid = %s
                    WHERE id = %s
                """, (full_name, role_id, staff_id))
                if cur.rowcount == 0:
                    return False, f"Сотрудник с ID={staff_id} не найден."
                conn.commit()
                return True, "Данные сотрудника обновлены."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()

    def delete_staff(self, staff_id):
        """
        Удаление сотрудника по ID.
        """
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM staff WHERE id = %s", (staff_id,))
                if cur.rowcount == 0:
                    return False, f"Сотрудник с ID={staff_id} не найден."
                conn.commit()
                return True, "Сотрудник успешно удалён."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()
