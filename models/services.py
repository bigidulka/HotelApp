# File path: models/services.py
import psycopg2

class Services:
    def __init__(self):
        self.connection_string = "host=localhost port=5432 dbname=hotel user=postgres password=postgres"

    def connect(self):
        try:
            return psycopg2.connect(self.connection_string)
        except psycopg2.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return None

    def get_all_services(self):
        """
        Возвращает список всех услуг (id, servicename, price).
        """
        conn = self.connect()
        if not conn:
            return []

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, servicename, price
                    FROM services
                    ORDER BY id
                """)
                return cur.fetchall()
        finally:
            conn.close()

    def add_service(self, service_name, price):
        """
        Добавление новой услуги.
        """
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                # Пример проверки: нет ли услуги с таким именем
                cur.execute("""
                    SELECT COUNT(*) FROM services
                    WHERE servicename = %s
                """, (service_name,))
                if cur.fetchone()[0] > 0:
                    return False, "Услуга с таким названием уже существует."

                cur.execute("""
                    INSERT INTO services (servicename, price)
                    VALUES (%s, %s)
                """, (service_name, price))
                conn.commit()
                return True, "Услуга успешно добавлена."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()

    def update_service(self, service_id, service_name, price):
        """
        Обновление услуги по ID.
        """
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE services
                    SET servicename = %s,
                        price = %s
                    WHERE id = %s
                """, (service_name, price, service_id))
                if cur.rowcount == 0:
                    return False, f"Услуга с ID={service_id} не найдена."
                conn.commit()
                return True, "Данные услуги обновлены."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()

    def delete_service(self, service_id):
        """
        Удаление услуги по ID.
        """
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM services WHERE id = %s", (service_id,))
                if cur.rowcount == 0:
                    return False, f"Услуга с ID={service_id} не найдена."
                conn.commit()
                return True, "Услуга успешно удалена."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()
