# File path: models/user.py
import psycopg2
import bcrypt
from datetime import datetime, timedelta

class User:
    def __init__(self):
        self.connection_string = "host=localhost port=5432 dbname=hotel user=postgres password=postgres"

    def connect(self):
        try:
            return psycopg2.connect(self.connection_string)
        except psycopg2.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return None
        
    def get_roles(self):
        conn = self.connect()
        if not conn:
            return []

        try:
            with conn.cursor() as cur:
                cur.execute("SELECT \"RoleId\", rolename FROM Roles")
                return cur.fetchall()
        finally:
            conn.close()

    def verify_user(self, login, password):
        conn = self.connect()
        if not conn:
            return None, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                cur.execute("SELECT u.Password, r.rolename, u.IsBlocked, u.LastLogin, u.PasswordChanged, u.FailedLoginAttempts "
                            "FROM Users u JOIN Roles r ON u.\"RoleID\" = r.\"RoleId\" WHERE u.Login = %s", (login,))
                user = cur.fetchone()
                if not user:
                    return None, "Вы ввели неверный логин или пароль. Пожалуйста, проверьте ещё раз введённые данные."

                stored_password, role, is_blocked, last_login, password_changed, failed_attempts = user

                if not stored_password.startswith('$2b$'):
                    return None, "Некорректный формат хэша пароля в базе данных. Обратитесь к администратору."

                if is_blocked:
                    return None, "Вы заблокированы. Обратитесь к администратору."

                if last_login and (datetime.now() - last_login).days > 30:
                    self.block_user(login)
                    return None, "Вы заблокированы. Обратитесь к администратору."

                if not bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    failed_attempts += 1
                    if failed_attempts >= 3:
                        self.block_user(login)
                        return None, "Вы заблокированы. Обратитесь к администратору."
                    else:
                        self.update_failed_attempts(login, failed_attempts)
                        return None, "Вы ввели неверный логин или пароль. Пожалуйста, проверьте ещё раз введённые данные."

                self.update_failed_attempts(login, 0)
                self.update_last_login(login)
                return {
                    'login': login,
                    'role': role,
                    'password_changed': password_changed
                }, None
        except psycopg2.Error as e:
            return None, f"Ошибка базы данных: {e}"
        finally:
            conn.close()

    def block_user(self, login):
        conn = self.connect()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("UPDATE Users SET IsBlocked = TRUE WHERE Login = %s", (login,))
                    conn.commit()
            finally:
                conn.close()
                
    def block_user_by_id(self, user_id):
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                cur.execute("UPDATE Users SET IsBlocked = TRUE WHERE UserID = %s", (user_id,))
                conn.commit()
                return True, "Пользователь успешно заблокирован."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()

    def update_failed_attempts(self, login, attempts):
        conn = self.connect()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("UPDATE Users SET FailedLoginAttempts = %s WHERE Login = %s", (attempts, login))
                    conn.commit()
            finally:
                conn.close()

    def update_last_login(self, login):
        conn = self.connect()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("UPDATE Users SET LastLogin = CURRENT_TIMESTAMP WHERE Login = %s", (login,))
                    conn.commit()
            finally:
                conn.close()

    def change_password(self, login, current_password, new_password):
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                # Проверка текущего пароля
                cur.execute("SELECT Password FROM Users WHERE Login = %s", (login,))
                stored_password = cur.fetchone()[0]
                if not bcrypt.checkpw(current_password.encode('utf-8'), stored_password.encode('utf-8')):
                    return False, "Неверный текущий пароль."

                # Обновление пароля
                hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                cur.execute("UPDATE Users SET Password = %s, PasswordChanged = TRUE WHERE Login = %s",
                           (hashed_new_password.decode('utf-8'), login))
                conn.commit()
                return True, "Пароль успешно изменён."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()

    def get_all_users(self):
        conn = self.connect()
        if not conn:
            return []

        try:
            with conn.cursor() as cur:
                cur.execute("SELECT u.UserID, u.Login, r.rolename, u.IsBlocked "
                            "FROM Users u JOIN Roles r ON u.\"RoleID\" = r.\"RoleId\"")
                return cur.fetchall()
        finally:
            conn.close()
                
    def add_role(self, rolename):
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM Roles WHERE rolename = %s", (rolename,))
                if cur.fetchone()[0] > 0:
                    return False, "Такая роль уже существует."
                cur.execute("INSERT INTO Roles (rolename) VALUES (%s)", (rolename,))
                conn.commit()
                return True, "Роль успешно добавлена."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()


    def add_user(self, login, password, role_id):
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                # Проверка на существование логина
                cur.execute("SELECT COUNT(*) FROM Users WHERE Login = %s", (login,))
                if cur.fetchone()[0] > 0:
                    return False, "Пользователь с таким логином уже существует."

                # Добавление пользователя
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                cur.execute("INSERT INTO Users (Login, Password, \"RoleID\") VALUES (%s, %s, %s)",
                            (login, hashed_password.decode('utf-8'), role_id))
                conn.commit()
                return True, "Пользователь успешно добавлен."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()

    def update_user(self, user_id, login, password, role_id):
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                # Проверка на существование логина (кроме текущего пользователя)
                cur.execute("SELECT COUNT(*) FROM Users WHERE Login = %s AND UserID != %s", (login, user_id))
                if cur.fetchone()[0] > 0:
                    return False, "Пользователь с таким логином уже существует."

                # Обновление данных
                if password:
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    cur.execute("UPDATE Users SET Login = %s, Password = %s, \"RoleID\" = %s WHERE UserID = %s",
                                (login, hashed_password.decode('utf-8'), role_id, user_id))
                else:
                    cur.execute("UPDATE Users SET Login = %s, \"RoleID\" = %s WHERE UserID = %s",
                                (login, role_id, user_id))
                conn.commit()
                return True, "Данные пользователя обновлены."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()

    def unblock_user(self, user_id):
        conn = self.connect()
        if not conn:
            return False, "Ошибка подключения к базе данных"

        try:
            with conn.cursor() as cur:
                cur.execute("UPDATE Users SET IsBlocked = FALSE, FailedLoginAttempts = 0 WHERE UserID = %s", (user_id,))
                conn.commit()
                return True, "Блокировка снята."
        except psycopg2.Error as e:
            return False, f"Ошибка базы данных: {e}"
        finally:
            conn.close()