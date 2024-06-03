import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
from datetime import datetime

# Укажите путь к папке, где будут сохраняться файлы базы данных
save_directory = "databases"

# Создаем папку, если она не существует
if not os.path.exists(save_directory):
    os.makedirs(save_directory)


# Функция для создания базы данных и таблиц, если они не существуют
def create_database(filename):
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Clients (
                ClientID INTEGER PRIMARY KEY AUTOINCREMENT,
                ClientName TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Employees (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                EmployeeName TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Requests (
                RequestID INTEGER PRIMARY KEY AUTOINCREMENT,
                RequestNumber TEXT NOT NULL,
                DateAdded TEXT NOT NULL,
                Equipment TEXT NOT NULL,
                FaultType TEXT NOT NULL,
                ProblemDescription TEXT NOT NULL,
                ClientID INTEGER NOT NULL,
                AssignedTo INTEGER NOT NULL,
                Status TEXT NOT NULL,
                FOREIGN KEY (ClientID) REFERENCES Clients (ClientID),
                FOREIGN KEY (AssignedTo) REFERENCES Employees (ID)
            )
        """)
        conn.commit()

        # Добавляем тестовые данные, если таблицы пусты
        cursor.execute("SELECT COUNT(*) FROM Clients")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO Clients (ClientName) VALUES ('Клиент1'), ('Клиент2')")

        cursor.execute("SELECT COUNT(*) FROM Employees")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO Employees (EmployeeName) VALUES ('Сотрудник1'), ('Сотрудник2')")

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Ошибка при создании базы данных: {e}")


# Функция для очистки формы
def clear_form():
    """Очищает все поля ввода."""
    for widget in window.children.values():
        if isinstance(widget, tk.Entry):
            widget.delete(0, tk.END)
        elif isinstance(widget, tk.Text):
            widget.delete("1.0", tk.END)


# Функция для добавления нового запроса
def add_request():
    """Добавляет новый запрос в базу данных."""
    try:
        # Генерируем уникальное имя файла базы данных
        now = datetime.now()
        filename = os.path.join(save_directory, f"helpdesk_{now.strftime('%Y%m%d_%H%M%S')}.db")

        # Создаем базу данных
        create_database(filename)

        # Подключаемся к новой базе данных
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()

        # Получаем данные из полей ввода
        request_number = request_number_entry.get()
        date_added = date_added_entry.get()
        equipment = equipment_entry.get()
        fault_type = fault_type_entry.get()
        problem_description = problem_description_text.get("1.0", tk.END).strip()
        client_name = client_name_entry.get()
        employee_name = employee_name_entry.get()
        status = status_entry.get()

        # Проверяем, заполнены ли все обязательные поля
        if not request_number or not date_added or not equipment or not fault_type or not problem_description or not client_name or not employee_name or not status:
            messagebox.showerror("Ошибка", "Заполните все обязательные поля.")
            return

        # Получаем идентификаторы клиента и сотрудника по их именам
        client_id = get_client_id(client_name, cursor)
        employee_id = get_employee_id(employee_name, cursor)

        # Если клиент или сотрудник не найдены, выдаем ошибку
        if client_id is None or employee_id is None:
            messagebox.showerror("Ошибка", "Клиент или сотрудник не найдены.")
            return
            # Вставляем новый запрос в базу данных
        cursor.execute("""
            INSERT INTO Requests (
                RequestNumber,
                DateAdded,
                Equipment,
                FaultType,
                ProblemDescription,
                ClientID,
                AssignedTo,
                Status
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (request_number, date_added, equipment, fault_type, problem_description, client_id, employee_id, status))
        conn.commit()
        conn.close()

        # Очищаем форму
        clear_form()

        # Выводим сообщение об успешном добавлении запроса
        messagebox.showinfo("Успешно", f"Запрос успешно добавлен и сохранен в {filename}.")
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при добавлении запроса: {e}")


# Функция для получения идентификатора клиента по его имени
def get_client_id(client_name, cursor):
    """Возвращает идентификатор клиента по его имени."""
    cursor.execute("""
        SELECT ClientID 
        FROM Clients 
        WHERE ClientName = ?
    """, (client_name,))
    result = cursor.fetchone()
    if result is None:
        print(f"Клиент не найден: {client_name}")
        return None
    else:
        return result[0]


# Функция для получения идентификатора сотрудника по его имени
def get_employee_id(employee_name, cursor):
    """Возвращает идентификатор сотрудника по его имени."""
    cursor.execute("""
        SELECT ID 
        FROM Employees 
        WHERE EmployeeName = ?
    """, (employee_name,))
    result = cursor.fetchone()
    if result is None:
        print(f"Сотрудник не найден: {employee_name}")
        return None
    else:
        return result[0]


# Функция для открытия основного окна
def open_main_window():
    auth_window.withdraw()
    window.deiconify()

# Функция для возврата к окну авторизации
def go_back_to_auth():
    window.withdraw()
    auth_window.deiconify()

# Создаем окно авторизации
auth_window = tk.Tk()
auth_window.title("Авторизация")

login_label = tk.Label(auth_window, text="Логин")
login_entry = tk.Entry(auth_window)

password_label = tk.Label(auth_window, text="Пароль")
password_entry = tk.Entry(auth_window, show="*")

def login():
    # Здесь добавьте вашу логику авторизации
    username = login_entry.get()
    password = password_entry.get()
    if username == "login1" and password == "password1":  # Простая проверка, замените на свою
        open_main_window()
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")

login_button = tk.Button(auth_window, text="Войти", command=login)
login_label.grid(row=0, column=0)
login_entry.grid(row=0, column=1)
password_label.grid(row=1, column=0)
password_entry.grid(row=1, column=1)
login_button.grid(row=2, column=1)

# Создаем главное окно
window = tk.Toplevel(auth_window)
window.title("Helpdesk")
window.withdraw()  # Скрываем главное окно до успешной авторизации

# Создаем поля ввода
request_number_label = tk.Label(window, text="Номер заявки")
request_number_entry = tk.Entry(window)

date_added_label = tk.Label(window, text="Дата добавления")
date_added_entry = tk.Entry(window)

equipment_label = tk.Label(window, text="Оборудование")
equipment_entry = tk.Entry(window)

fault_type_label = tk.Label(window, text="Тип неисправности")
fault_type_entry = tk.Entry(window)

problem_description_label = tk.Label(window, text="Описание проблемы")
problem_description_text = tk.Text(window, height=5)

client_name_label = tk.Label(window, text="Имя клиента")
client_name_entry = tk.Entry(window)

employee_name_label = tk.Label(window, text="Имя сотрудника")
employee_name_entry = tk.Entry(window)

status_label = tk.Label(window, text="Статус")
status_entry = tk.Entry(window)

# Создаем кнопку для добавления нового запроса
add_request_button = tk.Button(window, text="Добавить заявку", command=add_request)

# Создаем кнопку для возврата к окну авторизации
back_button = tk.Button(window, text="Назад", command=go_back_to_auth)
# Размещаем виджеты на окне
request_number_label.grid(row=0, column=0)
request_number_entry.grid(row=0, column=1)

date_added_label.grid(row=1, column=0)
date_added_entry.grid(row=1, column=1)

equipment_label.grid(row=2, column=0)
equipment_entry.grid(row=2, column=1)

fault_type_label.grid(row=3, column=0)
fault_type_entry.grid(row=3, column=1)

problem_description_label.grid(row=4, column=0)
problem_description_text.grid(row=4, column=1)

client_name_label.grid(row=5, column=0)
client_name_entry.grid(row=5, column=1)

employee_name_label.grid(row=6, column=0)
employee_name_entry.grid(row=6, column=1)

status_label.grid(row=7, column=0)
status_entry.grid(row=7, column=1)

add_request_button.grid(row=8, column=1)
back_button.grid(row=9, column=1)

# Запускаем окно авторизации
auth_window.mainloop()
