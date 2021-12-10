import unittest  # importing unittest to run tests
import sys  # importing sys(tem) in order to define where the actual classes.py is

sys.path.append(
    "../"
)  # appending to path the folder one level up, which contains the python files that have our warehouse project
from classes import User, Employee, Item, Warehouse
from unittest.case import TestCase


class test_warehouse(unittest.TestCase):
    def test_class_User(self):
        try:
            User()
        except NameError:  # this means that the class we tried to instanciate does not exist
            self.fail("Class does not exist")

    def test_class_Employee(self):
        try:
            Employee("username", "password")
        except NameError:  # this means that the class we tried to instanciate does not exist
            self.fail("Class does not exist")

    def test_class_Item(self):
        try:
            Item("state", "category", "warehouse", "date_of_stock")
        except NameError:  # this means that the class we tried to instanciate does not exist
            self.fail("Class does not exist")

    def test_class_Warehouse(self):
        try:
            Warehouse("id")
        except NameError:  # this means that the class we tried to instanciate does not exist
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
        pass
