from data import stock #stock is a list of dictionaries
from datetime import datetime

'''
This method searches in a stocklist an item that is found
in a warehouse with a provided number and then prints the item and 
the warehouse that it's found
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

def availabilityAnditemDaysInStock(stocklist, item_to_search) :
    count_warehouse1 = 0
    count_warehouse2 = 0

    for x in stocklist:
        full_item_name = x["state"] + " " + x["category"]
        if(full_item_name.lower() == item_to_search.lower()): #the .lower makes search case insensitive
            if x["warehouse"] == 1:
                count_warehouse1 += 1
            if x["warehouse"] == 2:
                count_warehouse2 += 1

    print("Amount available", count_warehouse1 + count_warehouse2)
    if (count_warehouse1 + count_warehouse2) != 0:
        print("Location:")

        for x in stocklist:
            full_item_name = x["state"] + " " + x["category"]
            if(full_item_name.lower() == item_to_search.lower()): #the .lower makes search case insensitive
                start_date = datetime.today()
                end_date = datetime.strptime(x["date_of_stock"], "%Y-%m-%d %H:%M:%S")
                days_in_stock = (start_date - end_date)
                print("- Warehouse", x["warehouse"], "(in stock for", days_in_stock.days , "days)")
        print()

        if count_warehouse1 > count_warehouse2:
            print("Maximum availability:", count_warehouse1, "in Warehouse 1")
        elif count_warehouse2 > count_warehouse1:
            print("Maximum availability:", count_warehouse2, "in Warehouse 2")
        else:
            print("Product exists in same quantities in both warehouses")
    else:
        print("Location: Not in stock")
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")

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
    category_to_browse = int(input("Type the number of the category to browse: "))
    print("List of",categoryList[category_to_browse-1],"available:")#in reality the nth item is the -1 index,
                                                                    #from categorylist[number of category to browse]
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
    for x in stocklist:
        if x["category"] == categoryList[category_to_browse-1]:
            print(x["state"],x["category"],", Warehouse:",x["warehouse"])
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")

## - Part where we define the user name
# first asking the username from the user to start
user_name = (input("What is your user name?: "))

# if the user didnt provide a username, we put 'stranger'
if user_name == "":# if user name was not provided we set it to 'stranger'
    user_name = "stranger"

print("Greetings", user_name, "!")
## - End of part where we handle user name

## - Part where we handle the program main loop
repeat = True # we will do the main loop until this is set to false
while(repeat):
    print("How can I be of service?")

    action= int(input("1. List items by Warehouse?\n2. Search an item and place an order?\n3. Browse by category\n4. Quit\n--- Type the number of the operation:  "))
    if action == 1:
        ## - Part where we handle Action 1 - 
        # defined in https://github.com/dci-dh-python-e21-01/python-projects-individual.V1.0/tree/main/2_Python-Basics
        '''
        If the user picked 1,
        the script should print each of the items in each of the warehouses
        (first all items from a warehouse and then all items from the other).
        When printing the list of items, and at the end of the whole list,
        print the total amount of items in stock on each warehouse
        '''
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        printWarehouseItems(stock, 1)

        input("Press any key to continue to warehouse #2")
        printWarehouseItems(stock, 2)

        countWarehouseItems(stock, 1)
        countWarehouseItems(stock, 2)

    elif action == 2:
        item_to_search = (input("What is the name of the item?: "))
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        availabilityAnditemDaysInStock(stock, item_to_search)
        ## Part where we handle the order making

        print("Would you like to place an order for this item?")
        order_action = int(input("1.Yes \n2.No\n: --- Type the number of the operation:  "))
        if order_action == 1:
            item_number = int(input("How many items would you like?:  "))
            #checking if we have enough items
            count_warehouse1 = searchWarehouseHowMany(stock, 1, item_to_search)
            count_warehouse2 = searchWarehouseHowMany(stock, 2, item_to_search)

            if item_number <= (count_warehouse1 + count_warehouse2): #if yes
                print("An order of",item_number,item_to_search,"has been placed") #make order
            else:#if not
                print("There are not this many items available.The maximum amount that can be ordered is ",(count_warehouse1 + count_warehouse2))#say we don't have that many items
                max_order = int(input("Would you like to order the maximum amount available?,\n1.Yes\n2.No\n:--- Type the number of the operation:  "))#ask if they want to order what we have
                if max_order == 1:#if yes
                    print("An order of",(count_warehouse1 + count_warehouse2),item_to_search,"has been placed")#print that order is placed
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        ## End of part where we place order
    elif action == 3:
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        printCategories(stock)
    elif action == 4:
        # End the while loop by setting repeat to False
        repeat = False
        print("Safe travels,", user_name,"!")
    else:
        print("Invalid Action")
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")