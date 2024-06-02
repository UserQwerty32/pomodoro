import tkinter as tk
import sqlite3

# Создаем экземпляр базы данных
conn = sqlite3.connect('helpdesk.db')
cursor = conn.cursor()

# Функция для очистки формы
def clear_form():
    """Очищает все поля ввода."""

    for widget in window.children.values():
        if isinstance(widget, (tk.Entry, tk.Text)):
            widget.delete(0, tk.END)

# Функция для добавления нового запроса
def add_request():
    """Добавляет новый запрос в базу данных."""

    # Получаем данные из полей ввода
    request_number = request_number_entry.get()
    date_added = date_added_entry.get()
    equipment = equipment_entry.get()
    fault_type = fault_type_entry.get()
    problem_description = problem_description_text.get("1.0", tk.END)
    client_name = client_name_entry.get()
    employee_name = employee_name_entry.get()
    status = status_entry.get()

    # Проверяем, заполнены ли все обязательные поля
    if not request_number or not date_added or not equipment or not fault_type or not problem_description or not client_name or not employee_name or not status:
        tk.messagebox.showerror("Ошибка", "Заполните все обязательные поля.")
        return

    # Получаем идентификаторы клиента и сотрудника по их именам
    client_id = get_client_id(client_name)
    employee_id = get_employee_id(employee_name)

    # Если клиент или сотрудник не найдены, выдаем ошибку
    if client_id is None or employee_id is None:
        tk.messagebox.showerror("Ошибка", "Клиент или сотрудник не найдены.")
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
            EmployeeID,
            Status
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (request_number, date_added, equipment, fault_type, problem_description, client_id, employee_id, status))
    conn.commit()

    # Очищаем форму
    clear_form()

    # Выводим сообщение об успешном добавлении запроса
    tk.messagebox.showinfo("Успешно", "Запрос успешно добавлен.")

# Функция для получения идентификатора клиента по его имени
def get_client_id(client_name):
    """Возвращает идентификатор клиента по его имени."""

    cursor.execute("""
        SELECT ClientID 
        FROM Clients 
        WHERE ClientName = ?
    """, (client_name,))
    result = cursor.fetchone()
    if result is None:
        return None
    else:
        return result[0]

# Функция для получения идентификатора сотрудника по его имени
def get_employee_id(employee_name):
    """Возвращает идентификатор сотрудника по его имени."""

    cursor.execute("""
        SELECT ID 
        FROM Employees 
        WHERE EmployeeName = ?
    """, (employee_name,))
    result = cursor.fetchone()
    if result is None:
        return None
    else:
        return result[0]

# Создаем главное окно
window = tk.Tk()
window.title("Helpdesk")

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

# Запускаем главное окно
window.mainloop()
