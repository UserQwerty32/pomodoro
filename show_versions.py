import database
import tkinter as tk

def show_versions(root):
    versions_window = tk.Toplevel(root)
    versions_window.title('Предыдущие версии кода')
    rows = database.get_versions()
    for row in rows:
        version_label = tk.Label(versions_window, text=f'Автор: {row[1]}\nКод:\n{row[2]}\n')
        version_label.pack()