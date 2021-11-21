class User:
    def __init__(self, user_name = "Anonymous"):
        self._name = user_name
        self.is_authenticated = False
    
    def authenticate(self, password) -> bool:
        return False

    def is_named(self, name) -> bool:
        return self._name == name

    def greet(self):
        print("\nHello,", self._name, "!")
        print("Welcome to our Warehouse Database.")
        print("If you don't find what you are looking for,")
        print("please ask one of our staff members to assist you.\n")

    def bye(self, actions):
        print("\nThank you for your visit", self._name, "!")

class Employee(User):
    def __init__(self, user_name, password, head_of = []):
        super().__init__(user_name)
        self.__password = password
        self.head_of = head_of

    def authenticate(self, password):
        if self.__password == password:
            self.is_authenticated = True
        
        return self.is_authenticated

    def order(self, item, amount):
        print("Ordered", amount, "of", item)

    def greet(self):
        print("\nHello,", self._name, "!")
        print("If you experience a problem with the system,")
        print("please contact technical support.\n")

    def bye(self, actions):
        super().bye(actions)
        print("\nIn this session you have:")

        action_count = 1
        for action in actions:
            print(action_count, ".", action)
            action_count += 1
        
        print("Safe travels,", self._name, "!")

class Item:
    def __init__(self, state, category, warehouse, date_of_stock):
        self.state = state
        self.category = category
        self.date_of_stock = date_of_stock

    def __str__(self) -> str:
        return self.state + " " + self.category

class Warehouse:
    def __init__(self, warehouse_id):
        self.id = warehouse_id
        self.stock = []
        
    def occupancy(self) -> int:
        return len(self.stock)

    def add_item(self, item):
        self.stock.append(item)

    def search(self, search_term) -> list:
        found = []

        for item in self.stock:
            full_item_name = item.state + " " + item.category
            if search_term.lower() == full_item_name.lower():
                found.append(item)

        return found