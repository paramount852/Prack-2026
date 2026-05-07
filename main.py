import json
import os

class ExpenseManager:
    def __init__(self, storage_file=None):
        self.storage_file = storage_file
        self.expenses = []
        if storage_file:
            self.load_expenses()

    def load_expenses(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    self.expenses = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.expenses = []

    def save_expenses(self):
        if not self.storage_file:
            return
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self.expenses, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def add_expense(self, name, amount, category):
        if amount < 0:
            raise ValueError("Сума не може бути від'ємною")

        expense = {
            "назва": name,
            "сума": amount,
            "категорія": category
        }

        self.expenses.append(expense)
        self.save_expenses()

    def get_total(self):
        return sum(expense["сума"] for expense in self.expenses)

    def get_by_category(self, category):
        return [
            expense for expense in self.expenses
            if expense["категорія"] == category
        ]

    def show_expenses(self):
        return self.expenses


if __name__ == "__main__":
    manager = ExpenseManager("expenses.json")

    while True:
        print("\n--- Менеджер витрат ---")
        print("1. Додати витрату")
        print("2. Показати витрати")
        print("3. Загальна сума")
        print("4. Пошук за категорією")
        print("5. Вихід")

        choice = input("Оберіть дію: ")

        if choice == "1":
            name = input("Назва витрати: ")
            amount = float(input("Сума: "))
            category = input("Категорія: ")

            manager.add_expense(name, amount, category)
            print("Витрату додано!")

        elif choice == "2":
            expenses = manager.show_expenses()

            if not expenses:
                print("Список порожній")
            else:
                for expense in expenses:
                    print(expense)

        elif choice == "3":
            print(f"Загальна сума: {manager.get_total()} грн")

        elif choice == "4":
            category = input("Введіть категорію: ")
            results = manager.get_by_category(category)

            if not results:
                print("Нічого не знайдено")
            else:
                for expense in results:
                    print(expense)

        elif choice == "5":
            print("Завершення роботи")
            break

        else:
            print("Невірний вибір")