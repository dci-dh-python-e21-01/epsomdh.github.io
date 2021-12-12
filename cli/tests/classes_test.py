import unittest  # importing unittest to run tests
import sys

sys.path.append(
    "../"
)  # appending to path the folder one level up, which contains the python files that have our warehouse project

from classes import User, Employee, Item, Warehouse
from query import (
    getUser,
    getOperation,
)  # importing sys(tem) in order to define where the actual classes.py is
from contextlib import contextmanager


@contextmanager
def mock_input(mock):
    # This needed to be changed and function as a dictionary, otherwise
    # we get a 'dict' object has no attribute 'input' error
    original_input = __builtins__["input"]
    __builtins__["input"] = lambda _: mock
    yield
    __builtins__["input"] = original_input


@contextmanager
def mock_output(mock):
    original_print = __builtins__["print"]
    __builtins__["print"] = lambda *value: [mock.append(val) for val in value]
    yield
    __builtins__["print"] = original_print


class test_warehouse(unittest.TestCase):
    def test_class_User(self):
        try:
            User()
        except NameError:  # this means that the class we tried to instantiate does not exist
            self.fail("Class does not exist")

    def test_class_Employee(self):
        try:
            Employee("username", "password")
        except NameError:  # this means that the class we tried to instantiate does not exist
            self.fail("Class does not exist")

    def test_class_Item(self):
        try:
            Item("state", "category", "warehouse", "date_of_stock")
        except NameError:  # this means that the class we tried to instantiate does not exist
            self.fail("Class does not exist")

    def test_class_Warehouse(self):
        try:
            Warehouse("id")
        except NameError:  # this means that the class we tried to instantiate does not exist
            self.fail("Class does not exist")

    # Task 2
    def test_if_user_subclass(self):
        assert issubclass(Employee, User)

    # test 3
    def test_if_user_anonymous(self):
        object = User()
        self.assertFalse(object.is_authenticated)
        self.assertTrue(object._name == "Anonymous")

    def test_if_user_named(self):
        object = User("User_Name")
        self.assertFalse(object.is_authenticated)
        self.assertTrue(object._name == "User_Name")

    def test_if_user_nopass(self):
        object = User("User_Name")
        self.assertFalse(object.is_authenticated)
        self.assertFalse(object.authenticate("Whatever"))

    # test 4

    def test_if_employee_no_credentials(self):
        object = Employee(user_name="Anonymous", password="password")
        self.assertFalse(object.is_authenticated)
        self.assertTrue(object._name == "Anonymous")
        self.assertFalse(object.authenticate("Whatever"))
        self.assertEqual(object.head_of, [])  # check if head_of is an empty list

    def test_if_employee_credentials(self):
        object = Employee(user_name="user", password="password")
        object.authenticate("password")
        self.assertTrue(object.is_authenticated)
        self.assertEqual(object.head_of, [])  # is by default

    def test_if_employee_args(self):
        Employees = Employee("Robert Nono", "1234")
        object = Employee(user_name="user", password="password", head_of=[Employees])
        self.assertEqual(object.head_of, [Employees])

    # test 5

    def test_if_warehouse_created(self):
        object = Warehouse()
        self.assertTrue(object.id == None)

    def test_if_warehouse_sameid(self):
        object = Warehouse("warehouse_id")
        self.assertTrue(object.id == "warehouse_id")

    def test_if_stock_empty_list(self):
        object = Warehouse("warehouse_id")
        self.assertEqual(object.stock, [])

    def test_occupancy_stock_len(self):
        object = Warehouse("warehouse_id")
        # occupancy returns how many items are in the warehouse
        self.assertEqual(len(object.stock), object.occupancy())

    def test_occupancy_stock_add(self):
        object = Warehouse("warehouse_id")
        item = Item("state", "category", "warehouse", "date_of_stock")
        # when warehouse is being created it has 0 items inside
        self.assertEqual(object.occupancy(), 0)
        # adding an item to warehouse
        object.add_item(item)
        # testing if it now has 1 item
        self.assertEqual(object.occupancy(), 1)

    def test_occupancy_stock_search1(self):
        object = Warehouse("warehouse_id")
        item1 = Item("state1", "category1", "warehouse", "date_of_stock")
        item2 = Item("state2", "category2", "warehouse", "date_of_stock")

        object.add_item(item1)
        object.add_item(item2)

        self.assertEqual(
            object.search("state1 category1")[0].__str__(), item1.__str__()
        )

        self.assertEqual(
            object.search("sTatE2 catEgoRy2")[0].__str__(), item2.__str__()
        )

    # test 6

    def test_item_stored(self):
        object = Item("state", "category", "warehouse", "date_of_stock")
        self.assertTrue(object.state == "state")
        self.assertTrue(object.category == "category")
        self.assertTrue(object.date_of_stock == "date_of_stock")

    def test_item_cast_string(self):
        object = Item("state", "category", "warehouse", "date_of_stock")
        self.assertEqual(object.__str__(), "state category")

    # Part 2
    # test 1
    def test_user_is_anonymous(self):
        with mock_input("Anon"):
            user = getUser()
            self.assertEqual(user._name, "Anon")
            self.assertNotEqual(type(user), Employee)
            self.assertEqual(type(user), User)

    def test_user_is_Employee(self):
        with mock_input("Jeremy"):
            user = getUser()
            self.assertEqual(user._name, "Jeremy")
            self.assertEqual(type(user), Employee)
            self.assertTrue(issubclass(type(user), User))

    # test 2
    def test_all_options_exist(self):
        with mock_input(4):
            answer = []
            with mock_output(answer):
                getOperation()
                self.assertEqual(
                    answer[0],
                    "1. List items by Warehouse?\n2. Search an item and place an order?\n3. Browse by category\n4. Quit\n---",
                )

    def test_all_option_correct(self):
        with mock_input(1):
            answer = []
            with mock_output(answer):
                self.assertEqual(getOperation(), 1)
        with mock_input(2):
            answer = []
            with mock_output(answer):
                self.assertEqual(getOperation(), 2)
        with mock_input(3):
            answer = []
            with mock_output(answer):
                self.assertEqual(getOperation(), 3)
        with mock_input(4):
            answer = []
            with mock_output(answer):
                self.assertEqual(getOperation(), 4)

    # test 3
