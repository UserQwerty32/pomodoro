import database
from tkinter import messagebox

def rollback_version(code_text):
    author, code = database.get_previous_version()
    if code:
        code_text.delete('1.0', 'end')
        code_text.insert('1.0', code)
        messagebox.showinfo('Откат выполнен!', f'Версия кода от {author} успешно восстановлена!')
    else:
        messagebox.showerror('Ошибка!', 'Недостаточно версий для отката!')