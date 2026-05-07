import unittest
from main import ExpenseManager


class TestExpenseManager(unittest.TestCase):

    def setUp(self):
        self.manager = ExpenseManager()

    def test_add_expense(self):
        self.manager.add_expense("Їжа", 200, "Продукти")

        self.assertEqual(len(self.manager.expenses), 1)
        self.assertEqual(self.manager.expenses[0]["назва"], "Їжа")

    def test_total_amount(self):
        self.manager.add_expense("Їжа", 200, "Продукти")
        self.manager.add_expense("Таксі", 150, "Транспорт")

        self.assertEqual(self.manager.get_total(), 350)

    def test_filter_by_category(self):
        self.manager.add_expense("Їжа", 200, "Продукти")
        self.manager.add_expense("Автобус", 50, "Транспорт")

        results = self.manager.get_by_category("Транспорт")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["назва"], "Автобус")

    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense("Помилка", -100, "Інше")


if __name__ == "__main__":
    unittest.main()