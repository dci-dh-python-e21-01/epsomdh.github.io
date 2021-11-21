from data import stock, personnel #stock and pesonnel is a list of dictionaries
from datetime import datetime

actions = list()

### Third Iteration version

'''
1. Need functions for the following :

    Search and order an item
    Browse by category
'''


'''
This method searches in a stocklist an item that is found
in a warehouse with a provided number and then prints the item and
the warehouse that it's found

Print the list of items
'''
def printWarehouseItems(stocklist, warehouse_number):
    # first time we call with stock, 1
    # so it is like there are two lines that say :
    # stocklist = stock ( first argument )
    # warehouse_number = 1 ( second argument )
    print("Items in Warehouse", warehouse_number, ":")
    for x in stocklist:
        if x["warehouse"] == warehouse_number:
            print ("-", x["state"], x["category"])
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
    print("End of list of items in Warehouse #", warehouse_number)
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")


def countWarehouses(stocklist):
    # first we count the warehouses
    warehouses = set()

    for x in stocklist:
        warehouses.add(x["warehouse"])

    return warehouses

def countWarehouseItems(stocklist, warehouse_number):
    # first time we call with stock, 1
    # so it is like there are two lines that say :
    # stocklist = stock ( first argument )
    # warehouse_number = 1 ( second argument )
    count = 0#this will hold the amount of times
    for x in stocklist:
        if x["warehouse"] == warehouse_number:
            count+=1

    print("Total items in Warehouse",warehouse_number,":",count)
    addAction("Listed " + str(count) + " Items in Warehouse " + str(warehouse_number))
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")

'''
Returns how many items exist
'''
def searchWarehouseHowMany(stocklist, warehouse_number, item_to_search):
    count = 0
    for x in stocklist:
        if x["warehouse"] == warehouse_number:
            full_item_name = x["state"] + " " + x["category"]
            if(full_item_name.lower() == item_to_search.lower()):#the .lower makes search case insensitive
                count+=1

    return count

def availabilityAnditemDaysInStock(stocklist, item_to_search, warehouses) :
    counts = {}

    for warehouse in warehouses:
        counts.setdefault("warehouse " + str(warehouse), 0)
        counts["warehouse " + str(warehouse)] = searchWarehouseHowMany(stocklist, int(warehouse), item_to_search)

    print("Amount available", sum(counts.values()))
    if sum(counts.values()) != 0:
        print("Location:")

        for x in stocklist:
            full_item_name = x["state"] + " " + x["category"]
            if(full_item_name.lower() == item_to_search.lower()): #the .lower makes search case insensitive
                start_date = datetime.today()
                end_date = datetime.strptime(x["date_of_stock"], "%Y-%m-%d %H:%M:%S")
                days_in_stock = (start_date - end_date)
                print("- Warehouse", x["warehouse"], "(in stock for", days_in_stock.days , "days)")
        print()

        print("Maximum availability:", max(counts.values()), "in", max(counts, key=counts.get))
    else:
        print("Location: Not in stock")
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
    addAction("Searched for " + item_to_search)
    return counts

def  printCategories(stocklist):
    categoryDictionary = {} # Creating a new, empty dictionary
    for x in stocklist: # for each item in stock
        # if the key named by the item category exists 'setdefault' will do nothing
        # if the key named by the item category does not exist, it will be appended to the dictionary with the initial value 0
        categoryDictionary.setdefault(x["category"], 0)#imagine this as an empty vase with 0 items inside
        categoryDictionary[x["category"]] += 1 # increasing the count of the items in this category(vase), instead of creating a new category

    count = 1#just prints 1.2.3...
    categoryList = []#preparing an empty lists to add the categories in an ordered way
    for key, value in categoryDictionary.items():
        print(count, ".", key, "(", value, ")")
        categoryList.append(key)#adding the category name into the list
        count += 1

    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")

    try:
        category_to_browse = int(input("Type the number of the category to browse: "))
        print("List of",categoryList[category_to_browse-1],"available:") # in reality the nth item is the -1 index,
                                                                     # from categorylist[number of category to browse]
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        for x in stocklist:
            if x["category"] == categoryList[category_to_browse-1]:
                print(x["state"],x["category"],", Warehouse:",x["warehouse"])

        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        addAction("Printed Categories for all Items")
    except:
        print("Please Only Enter a number.")


'''
Get the user name
'''
def getUsername():
    ## - Part where we define the user name
    # first asking the username from the user to start
    user_name = (input("What is your user name?: "))

    # if the user didn't provide a username, we put 'stranger'
    if user_name == "":# if user name was not provided we set it to 'stranger'
        user_name = "stranger"
    addAction("Provided user name " + user_name)
    return user_name

'''
Greet the user
'''
def greetUser(user_name):

    print("Greetings", user_name, "!")


'''
 Get the operation selected
'''
def getOperation():
    print("How can I be of service?")

    action = int(input("1. List items by Warehouse?\n2. Search an item and place an order?\n3. Browse by category\n4. Quit\n--- Type the number of the operation:  "))
    return action

'''
Check Password
'''
def checkForUserPassword(user_name, password, personnel_file):
    for person in personnel_file:
        if person["user_name"] == user_name and person["password"] == password:
            return True

        if "head_of" in person:
            if checkForUserPassword(user_name, password, person["head_of"]):
                return True

    return False


'''
Add action to history
'''

def addAction(action_string):
    actions.append(action_string)


#######################################################################################################################################################################
## - Part where we handle the program main loop
#######################################################################################################################################################################

repeat = True # we will do the main loop until this is set to false

user_name = getUsername()
greetUser(user_name)
warehouses = countWarehouses(stock)

## - End of part where we handle user name
while(repeat):

    action = getOperation()
    if action == 1:
        ## - Part where we handle Action 1 -
        # Print the list of Items
        '''
            If the user picked 1,
            the script should print each of the items in each of the warehouses
            (first all items from a warehouse and then all items from the other).
            When printing the list of items, and at the end of the whole list,
            print the total amount of items in stock on each warehouse
        '''
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")

        for warehouse in warehouses:
            printWarehouseItems(stock, int(warehouse))
            input("Press any key to continue to next warehouse", )

        for warehouse in warehouses:
            countWarehouseItems(stock, int(warehouse))

    elif action == 2:

        password = input("Please input your password in order to do this action: ")
        while checkForUserPassword(user_name,password,personnel) == False:
            print("You are not allowed to perform this action.")
            addAction("Tried to order as user " + user_name)
            new_choice = int(input("Please select an option :\n1. login as another user and try again.\n2. Go back to main menu "))
            if new_choice == 1:
                user_name = getUsername()
                greetUser(user_name)
                password = input("Please input your password in order to do this action: ")
            else:
                break

        if checkForUserPassword(user_name,password,personnel):
            item_to_search = (input("What is the name of the item?: "))
            print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
            counts = availabilityAnditemDaysInStock(stock, item_to_search, warehouses)
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
            addAction("Tried to order as user " + user_name)
    elif action == 3:
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        printCategories(stock)
    elif action == 4:
        # End the while loop by setting repeat to False
        repeat = False

        print("Thank you for your visit", user_name, "!")
        print("In this session you have:")
        action_count = 1
        for action in actions:
            print(action_count, ".", action)
            action_count += 1

        print("Safe travels,", user_name,"!")
    else:
        print("Invalid Action")
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")

#######################################################################################################################################################################
## - End program main loop
#######################################################################################################################################################################
