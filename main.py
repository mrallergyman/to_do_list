import tkinter as tk
from tkinter import ttk
import tempfile
import base64
import zlib
import json


# прозрачная иконка приложения
ICON = zlib.decompress(base64.b64decode(
    "eJxjYGAEQgEBBiDJwZDBysAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF\
    /ykEAFXxQRc="))

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, "wb") as icon_file:
    icon_file.write(ICON)

# Словарь для хранения цветов элементов
selected_tasks: set[int] = set()


# добавляем новую задачу
def add_task():
    task = entry.get()
    entry.delete(first=0, last=tk.END)
    size = listbox.size()
    if task:
        listbox.insert(size, task)


# удаляем задачу
def del_task():
    indexes = listbox.curselection()
    # print(indexes)
    if indexes:
        for x in reversed(indexes):  # Удаляем с конца списка
            listbox.delete(x)
            if x in selected_tasks:
                selected_tasks.remove(x)


# очищаем список задач
def clear_tasks():
    listbox.delete(0, 'end')
    selected_tasks.clear()


def double_click(event):
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        if index in selected_tasks:
            listbox.itemconfig(index, fg='black')
            selected_tasks.remove(index)
        else:
            # Перезаписываем элемент с новым цветом
            listbox.itemconfig(index, fg='grey')
            selected_tasks.add(index)


# читаем файл JSON при открытии программы и добавляем задачи в список
def read_from_json_file():
    try:
        global selected_tasks
        with open('tasks.json', 'r', encoding='utf-8') as f:
            content = f.read()

            if not content.strip():
                return [], set()

            data = json.loads(content)

            if isinstance(data, dict):
                tasks = data.get('tasks', [])
                selected = data.get('selected', [])
                return tasks, selected
    except (json.JSONDecodeError, IOError) as e:
        print("Ошибка чтения JSON:", e)
        return [], []


# добавляем задачи в JSON файл при закрытии окна
def add_to_json_file():
    tasks_list = listbox.get(0, tk.END)
    # превращаем set в list
    to_json = {'tasks': tasks_list, 'selected': list(selected_tasks)}
    with open('tasks.json', 'w', encoding='utf-8') as f:
        json.dump(to_json, f, indent=2, ensure_ascii=False)

    root.destroy()
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

# загружаем задачи и выбранные индексы
tasks, selected_tasks = read_from_json_file()
selected_tasks = set(selected_tasks)  # на всякий случай

# переменная задач
tasks_dict = tk.StringVar(value=tasks)

# создаем поле ввода
entry = ttk.Entry(font=("Tahoma", 10))
entry.grid(column=0, row=0, padx=6, pady=6, sticky="ew")

# создаем кнопку "Добавить задачу" из пакета ttk
btn_add = ttk.Button(text="Add Task", command=add_task)
btn_add.grid(column=1, row=0, padx=6, pady=6)  # размещаем кнопку в окне


# создаем список задач
listbox = tk.Listbox(selectmode="multiple", listvariable=tasks_dict)
listbox.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
listbox.bind("<Double-ButtonPress-1>", double_click)

# применяем серый цвет к нужным элементам
for i in selected_tasks:
    try:
        listbox.itemconfig(i, fg='grey')
    except tk.TclError:
        pass  # если индекс вне диапазона

# создаем полосу прокрутки для списка задач
scrollbar = ttk.Scrollbar(orient="vertical", command=listbox.yview)
scrollbar.grid(row=1, column=2, sticky='ns')
listbox.config(yscrollcommand=scrollbar.set)

# создаем кнопку "Очистить список" из пакета ttk
btn_clear = ttk.Button(text="Clear tasks", command=clear_tasks)
# размещаем кнопку в окне
btn_clear.grid(column=0, row=2, padx=6, pady=6, sticky='w')

# создаем кнопку "Удалить задачу" из пакета ttk
btn_del = ttk.Button(text="Del Task", command=del_task)
btn_del.grid(column=1, row=2, padx=6, pady=6)  # размещаем кнопку в окне

# при закрытии окна вызывать функцию add_to_json_file
root.protocol("WM_DELETE_WINDOW", add_to_json_file)

# Запускаем приложение
root.mainloop()
