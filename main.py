import tkinter as tk
from tkinter import ttk
import tempfile, base64, zlib


# прозрачная иконка приложения
ICON = zlib.decompress(base64.b64decode(\
    "eJxjYGAEQgEBBiDJwZDBysAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF\
    /ykEAFXxQRc="))

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, "wb") as icon_file:
    icon_file.write(ICON)


def add_to_json_file():  # добавляем задачи в JSON файл при закрытии окна
    root.destroy()  # ручное закрытие окна и всего приложения
    print("Закрытие приложения")


# Создаём главное окно
root = tk.Tk()
root.title("To-Do List")
root.geometry("400x500")
root.iconbitmap(default=ICON_PATH)
# root.attributes("-alpha", 0.5) # полупрозрачность

label = tk.Label(text="Hello METANIT.COM")  # TODO создаем текстовую метку
label.pack()    # размещаем метку в окне

btn_add = ttk.Button(text="Add Task", )  # создаем кнопку "Добавить задачу" из пакета ttk
btn_add.pack()  # размещаем кнопку в окне

root.protocol("WM_DELETE_WINDOW", add_to_json_file)  # при закрытии окна вызывать функцию add_to_json_file

# Запускаем приложение
root.mainloop()
