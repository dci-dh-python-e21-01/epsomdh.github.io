from datetime import datetime
from classes import User
from classes import Employee
from loader import Loader

personnel = Loader(model="personnel")
stock = Loader(model="stock")
user = User()

actions = list()

### Fourth Iteration version

'''
Print the list of items
'''
def printWarehouseItems(warehouse):
    print("Items in Warehouse", warehouse.id, ":")
    for item in warehouse.stock:
        print ("-", item)

    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
    print("End of list of items in Warehouse #", warehouse.id)
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")

def countWarehouseItems(warehouse):
    print("Total items in Warehouse", warehouse.id, ":", warehouse.occupancy())
    addAction("Listed " + str(warehouse.occupancy()) + " Items in Warehouse " + str(warehouse.id))
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")

def availabilityAnditemDaysInStock(stocklist, item_to_search) :
    counts = {}

    for warehouse in stocklist:
        counts.setdefault("warehouse " + warehouse.id, 0)
        counts["warehouse " + warehouse.id] = len(warehouse.search(item_to_search))

    print("Amount available", sum(counts.values()))
    if sum(counts.values()) != 0:
        print("Location:")

        for warehouse in stocklist:
            for item in warehouse.stock:
                if(item.__str__().lower() == item_to_search.lower()): #the .lower makes search case insensitive
                    start_date = datetime.today()
                    end_date = datetime.strptime(item.date_of_stock, "%Y-%m-%d %H:%M:%S")
                    days_in_stock = (start_date - end_date)
                    print("- Warehouse", warehouse.id, "(in stock for", days_in_stock.days , "days)")
        print()

        print("Maximum availability:", max(counts.values()), "in", max(counts, key=counts.get))
    else:
        print("Location: Not in stock")
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
    addAction("Searched for " + item_to_search)
    return counts

def  printCategories(stocklist):
    categoryDictionary = {} # Creating a new, empty dictionary
    for warehouse in stocklist:
        for x in warehouse.stock:
            categoryDictionary.setdefault(x.category, 0)#imagine this as an empty vase with 0 items inside
            categoryDictionary[x.category] += 1 # increasing the count of the items in this category(vase), instead of creating a new category

    count = 1#just prints 1.2.3...
    categoryList = []#preparing an empty lists to add the categories in an ordered way
    for key, value in categoryDictionary.items():
        print(count, ".", key, "(", value, ")")
        categoryList.append(key)#adding the category name into the list
        count += 1

    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")

    try:
        category_to_browse = int(input("Type the number of the category to browse: "))
        print("List of", categoryList[category_to_browse-1], "available:") # in reality the nth item is the -1 index,
                                                                     # from categorylist[number of category to browse]
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        for warehouse in stocklist:
            for item in warehouse.stock:
                if item.category == categoryList[category_to_browse-1]:
                    print(item, ", Warehouse:", warehouse.id)

        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        addAction("Printed Categories for " + categoryList[category_to_browse-1] + " Items")
    except:
        print("Please Only Enter a number.")


'''
Get the user name
'''
def getUser():
    ## - Part where we define the user name
    # first asking the username from the user to start
    global user
    user_name = (input("What is your user name?: "))

    user = findUser(personnel, user_name)
    if user == None:
        user = User(user_name)

    addAction("Provided user name " + user_name)

def findUser(personnel, user_name):
    for person in personnel:
        if person.is_named(user_name):
            return person # If we found the user, return as we dont have to seach any more

    # As a last action we have to see if someone is an subordinate of another person
    # according to the instuctions, these persons shoudl also be able to order.
    for person in personnel:
        if person.head_of:
            for subordinate in person.head_of:
                subordinate.setdefault("head_of", []) # setting a default head_of on the data.py list of dictionaries so that we can use it for creating a new Employee object
                subUser = Employee(subordinate["user_name"] , subordinate["password"], subordinate["head_of"]) # Creating a new Employee object, based on the items inside the current list
                foundUser = findUser([subUser], user_name) # searching recursively on the new Object to find a perosn that we could be heads off
                if foundUser != None: # if we didnt find anything we should return None
                    return foundUser # otherwise we return the user found

    return None


'''
 Get the operation selected
'''
def getOperation():
    print("How can I be of service?")

    action = int(input("1. List items by Warehouse?\n2. Search an item and place an order?\n3. Browse by category\n4. Quit\n--- Type the number of the operation:  "))
    return action
            
'''
Add action to history
'''
def addAction(action_string):
    actions.append(action_string) 


#######################################################################################################################################################################
## - Part where we handle the program main loop
#######################################################################################################################################################################

repeat = True # we will do the main loop until this is set to false

getUser()
user.greet()
warehouses = len(list(stock))

## - End of part where we handle user name
while(repeat):
    
    action = getOperation()
    if action == 1:
        ## - Part where we handle Action 1 - 
        # Print the list of Items
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")

        for warehouse in stock:
            printWarehouseItems(warehouse)
            input("Press any key to continue to next warehouse")
        
        for warehouse in stock:
            countWarehouseItems(warehouse)

    elif action == 2:

        if user.is_authenticated == False:
            password = input("Please input your password in order to do this action: ")
            user.authenticate(password)

        while user.is_authenticated == False:
            print("You are not allowed to perform this action until you are Authenticated as an Employee.")
            addAction("Tried to order as User")

            new_choice = int(input("Please select an option :\n1. login.\n2. Go back to main menu "))

            if new_choice == 1:
                print("Please enter you Employee Credentials: ")
                getUser()
                password = input("Please input your password in order to do this action: ")
                user.authenticate(password)
                user.greet()

            else:
                break

        if user.is_authenticated:
            item_to_search = (input("What is the name of the item?: "))
            print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
            counts = availabilityAnditemDaysInStock(stock, item_to_search)
            ## Part where we handle the order making

            print("Would you like to place an order for this item?")
            order_action = int(input("1.Yes \n2.No\n: --- Type the number of the operation:  "))

            if order_action == 1:
                item_number = int(input("How many items would you like?:  "))

                if item_number <= sum(counts.values()): #if yes
                    print("An order of", item_number, item_to_search, "has been placed") #make order
                    addAction("Made an order for " + str(item_number) + " of " + item_to_search)
                else:#if not
                    print("There are not this many items available.The maximum amount that can be ordered is ", sum(counts.values()))#say we don't have that many items
                    max_order = int(input("Would you like to order the maximum amount available?,\n1.Yes\n2.No\n:--- Type the number of the operation:  "))#ask if they want to order what we have
                    if max_order == 1:#if yes
                        print("An order of", sum(counts.values()), item_to_search, "has been placed")#print that order is placed
                        addAction("Made a maximum order for " + str(sum(counts.values())) + " of " + item_to_search)
            print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
            ## End of part where we place order
        else:
            addAction("Tried to order as User")
    elif action == 3:
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        printCategories(stock)
    elif action == 4:
        # End the while loop by setting repeat to False
        repeat = False
        user.bye(actions)

    else:
        print("Invalid Action")
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")

#######################################################################################################################################################################
## - End program main loop
#######################################################################################################################################################################
