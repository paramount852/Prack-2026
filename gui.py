import tkinter as tk
from tkinter import messagebox
from main import ExpenseManager

manager = ExpenseManager("expenses.json")

root = tk.Tk()
root.title("Менеджер витрат")
root.geometry("800x700")
root.resizable(False, False)

# Функції

def refresh_expenses():
    filter_text = filter_entry.get().strip().lower()
    expenses = manager.show_expenses()
    if filter_text:
        expenses = [
            expense for expense in expenses
            if expense["категорія"].lower() == filter_text
        ]
    expenses_listbox.delete(0, tk.END)
    for expense in expenses:
        expenses_listbox.insert(
            tk.END,
            f"{expense['назва']} — {expense['сума']} грн — {expense['категорія']}"
        )
    total = sum(expense["сума"] for expense in expenses)
    total_label.config(text=f"Загальна сума: {total} грн")


def add_expense():
    name = name_entry.get().strip()
    amount_text = amount_entry.get().strip()
    category = category_entry.get().strip()

    if not name or not amount_text or not category:
        messagebox.showwarning("Помилка", "Заповніть усі поля")
        return

    try:
        amount = float(amount_text)
    except ValueError:
        messagebox.showwarning("Помилка", "Сума має бути числом")
        return

    try:
        manager.add_expense(name, amount, category)
    except ValueError as error:
        messagebox.showwarning("Помилка", str(error))
        return

    name_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    refresh_expenses()


def apply_filter():
    refresh_expenses()


def clear_filter():
    filter_entry.delete(0, tk.END)
    refresh_expenses()

# Інтерфейс

frame_top = tk.Frame(root, padx=12, pady=12)
frame_top.pack(fill=tk.X)

label_title = tk.Label(frame_top, text="Менеджер витрат", font=(None, 18, "bold"))
label_title.pack(anchor=tk.W)

label_name = tk.Label(frame_top, text="Назва")
label_name.pack(anchor=tk.W, pady=(12, 0))
name_entry = tk.Entry(frame_top, width=40)
name_entry.pack(fill=tk.X)

label_amount = tk.Label(frame_top, text="Сума")
label_amount.pack(anchor=tk.W, pady=(8, 0))
amount_entry = tk.Entry(frame_top, width=40)
amount_entry.pack(fill=tk.X)

label_category = tk.Label(frame_top, text="Категорія")
label_category.pack(anchor=tk.W, pady=(8, 0))
category_entry = tk.Entry(frame_top, width=40)
category_entry.pack(fill=tk.X)

add_button = tk.Button(frame_top, text="Додати витрату", command=add_expense, bg="#4CAF50", fg="white")
add_button.pack(fill=tk.X, pady=(12, 0))

frame_filter = tk.Frame(root, padx=12, pady=12)
frame_filter.pack(fill=tk.X)

filter_label = tk.Label(frame_filter, text="Фільтр за категорією")
filter_label.pack(anchor=tk.W)
filter_entry = tk.Entry(frame_filter, width=30)
filter_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

filter_button = tk.Button(frame_filter, text="Показати", command=apply_filter)
filter_button.pack(side=tk.LEFT, padx=(8, 0))
clear_button = tk.Button(frame_filter, text="Скинути", command=clear_filter)
clear_button.pack(side=tk.LEFT, padx=(8, 0))

frame_list = tk.Frame(root, padx=12, pady=12)
frame_list.pack(fill=tk.BOTH, expand=True)

expenses_listbox = tk.Listbox(frame_list, width=80, height=14)
expenses_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame_list, command=expenses_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
expenses_listbox.config(yscrollcommand=scrollbar.set)

frame_bottom = tk.Frame(root, padx=12, pady=12)
frame_bottom.pack(fill=tk.X)

total_label = tk.Label(frame_bottom, text="Загальна сума: 0 грн", font=(None, 12, "bold"))
total_label.pack(anchor=tk.W)

refresh_expenses()
root.mainloop()
