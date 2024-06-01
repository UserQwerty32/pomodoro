import tkinter as tk
import save_version, show_versions, rollback_version

root = tk.Tk()
root.title('Система контроля версий')

author_label = tk.Label(root, text='Автор:')
author_label.pack()
author_entry = tk.Entry(root)
author_entry.pack()

code_label = tk.Label(root, text='Код:')
code_label.pack()
code_text = tk.Text(root, height=10, width=50)
code_text.pack()

save_button = tk.Button(root, text='Сохранить версию', command=lambda: save_version.save_version(author_entry.get(), code_text.get('1.0', 'end-1c')))
save_button.pack()

show_button = tk.Button(root, text='Показать предыдущие версии', command=lambda: show_versions.show_versions(root))
show_button.pack()

rollback_button = tk.Button(root, text='Откатить версию', command=lambda: rollback_version.rollback_version(code_text))
rollback_button.pack()

root.mainloop()