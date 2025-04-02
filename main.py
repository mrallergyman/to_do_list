import tkinter as tk
from tkinter import ttk
import tempfile
import base64
import zlib


# прозрачная иконка приложения
ICON = zlib.decompress(base64.b64decode(
    "eJxjYGAEQgEBBiDJwZDBysAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF\
    /ykEAFXxQRc="))

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, "wb") as icon_file:
    icon_file.write(ICON)


# добавляем новую задачу
def add_task():
    task = entry.get()
    if task:
        listbox.insert(0, task)


# удаляем задачу
def del_task():
    indexes = listbox.curselection()
    print(indexes)
    listbox.delete(indexes[0])


# добавляем задачи в JSON файл при закрытии окна
def add_to_json_file():
    root.destroy()  # ручное закрытие окна и всего приложения
    print("Закрытие приложения")


# Создаём главное окно
root = tk.Tk()
root.title("To-Do List")
root.geometry("300x250")
root.iconbitmap(default=ICON_PATH)
root.columnconfigure(index=0, weight=4, )
root.columnconfigure(index=1, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=3)
root.rowconfigure(index=2, weight=1)
# root.attributes("-alpha", 0.5) # полупрозрачность

# TODO создаем текстовую метку
# label = ttk.Label(text="To-Do List", font=("Tahoma", 12), padding=20)
# label.pack()    # размещаем метку в окне

# создаем поле ввода
entry = ttk.Entry(font=("Tahoma", 10))
entry.grid(column=0, row=0, padx=6, pady=6, sticky="ew")

# создаем кнопку "Добавить задачу" из пакета ttk
btn_add = ttk.Button(text="Add Task", command=add_task)
btn_add.grid(column=1, row=0, padx=6, pady=6)  # размещаем кнопку в окне

# создаем список задач
listbox = tk.Listbox()
listbox.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

# создаем кнопку "Удалить задачу" из пакета ttk
btn_del = ttk.Button(text="Del Task", command=del_task)
btn_del.grid(column=1, row=2, padx=6, pady=6)  # размещаем кнопку в окне

# при закрытии окна вызывать функцию add_to_json_file
root.protocol("WM_DELETE_WINDOW", add_to_json_file)

# Запускаем приложение
root.mainloop()
