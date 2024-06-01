import database
from tkinter import messagebox

def save_version(author, code):
    database.save_version(author, code)
    messagebox.showinfo('Сохранено!', 'Версия кода успешно сохранена!')