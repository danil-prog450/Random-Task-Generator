import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
import git

class TaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("600x400")  # Увеличиваем размер окна
        self.root.configure(bg="#f0f0f0")  # Устанавливаем цвет фона

        self.tasks = {
            "учёба": ["Прочитать главу учебника", "Решить задачу по математике", "Посмотреть обучающее видео"],
            "спорт": ["Сделать зарядку", "Пойти на пробежку", "Потренироваться в зале"],
            "работа": ["Ответить на письма", "Запланировать задачи на день", "Поработать над проектом"],
            "другое": ["Позвонить другу", "Почитать книгу", "Погулять на свежем воздухе"]
        }
        self.history = []
        self.history_file = "task_history.json"

        self.load_history()

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Frame для генерации задач
        self.generate_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        self.generate_frame.pack(pady=10)

        self.generate_button = tk.Button(self.generate_frame, text="Сгенерировать задачу", command=self.generate_task, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.generate_button.pack(pady=10)

        # Frame для отображения задачи
        self.task_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        self.task_frame.pack()

        self.task_label = tk.Label(self.task_frame, text="", wraplength=500, font=("Arial", 14), bg="#f0f0f0") # Добавляем wraplength
        self.task_label.pack()

        # Frame для добавления задач
        self.add_task_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        self.add_task_frame.pack()

        self.task_entry_label = tk.Label(self.add_task_frame, text="Добавить задачу:", bg="#f0f0f0")
        self.task_entry_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.task_entry = tk.Entry(self.add_task_frame, width=40)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.task_type_label = tk.Label(self.add_task_frame, text="Тип задачи:", bg="#f0f0f0")
        self.task_type_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.task_type_var = tk.StringVar(value="учёба")
        self.task_type_combobox = ttk.Combobox(self.add_task_frame, textvariable=self.task_type_var, values=list(self.tasks.keys()), width=37)
        self.task_type_combobox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.add_task_button = tk.Button(self.add_task_frame, text="Добавить задачу", command=self.add_task, bg="#2196F3", fg="white", font=("Arial", 10))
        self.add_task_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Frame для истории
        self.history_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        self.history_frame.pack(fill=tk.BOTH, expand=True)

        self.filter_label = tk.Label(self.history_frame, text="Фильтр по типу:", bg="#f0f0f0")
        self.filter_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.filter_var = tk.StringVar(value="Все")
        self.filter_combobox = ttk.Combobox(self.history_frame, textvariable=self.filter_var, values=["Все"] + list(self.tasks.keys()), width=15)
        self.filter_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.filter_combobox.bind("<<ComboboxSelected>>", self.update_history_list)

        self.history_listbox = tk.Listbox(self.history_frame, height=10, width=60, font=("Arial", 10), bg="white")
        self.history_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW) # Используем sticky для растягивания

        self.update_history_list()

        # Настройка растягивания для history_frame
        self.history_frame.columnconfigure(1, weight=1)  # Растягиваем второй столбец
        self.history_frame.rowconfigure(1, weight=1)  # Растягиваем строку с Listbox

    def generate_task(self):
        task_type = random.choice(list(self.tasks.keys()))
        task = random.choice(self.tasks[task_type])
        self.task_label.config(text=f"Задача: {task} ({task_type})")
        self.history.append({"task": task, "type": task_type})
        self.update_history_list()
        self.save_history()

    def add_task(self):
        new_task = self.task_entry.get().strip()
        task_type = self.task_type_var.get()

        if not new_task:
            messagebox.showerror("Ошибка", "Пожалуйста, введите задачу.")
            return

        if task_type not in self.tasks:
            self.tasks[task_type] = []

        self.tasks[task_type].append(new_task)
        self.task_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", "Задача добавлена.")
        self.save_history() # Сохраняем после добавления новой задачи
        self.update_history_list()

    def update_history_list(self, event=None):
        self.history_listbox.delete(0, tk.END)
        filter_type = self.filter_var.get()

        for item in self.history:
            if filter_type == "Все" or item["type"] == filter_type:
                self.history_listbox.insert(tk.END, f"{item['task']} ({item['type']})")

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except json.JSONDecodeError:
                print("Ошибка при загрузке истории из JSON.  Файл поврежден или пуст.")
                self.history = []

    def save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGenerator(root)
    root.mainloop()
