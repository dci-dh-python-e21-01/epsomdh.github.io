from data import warehouse1, warehouse2
import argparse

parser = argparse.ArgumentParser()
user_name = ""
repeat = True

# Adding optional argument
parser.add_argument("--user_name", help="ENTER YOUR USER NAME")
args = parser.parse_args()

if args.user_name:
  user_name = args.user_name
else:
 user_name= (input("What is your user name?:"))

print("Hello", user_name)

while(repeat):
    print("What would you like to do?")

    action= int(input("1. List items by Warehouse?\n2. Search an item and place an order?\n3. Quit  "))
    if action==1:
        print (warehouse1, warehouse2)

    if action==2:
        item_name= (input("What is the name of the item?"))
        elm_count_1=warehouse1.count(item_name)
        elm_count_2=warehouse2.count(item_name)
        if item_name in warehouse1 and warehouse2:
           print("Location: Both Warehouses", (elm_count_1+elm_count_2))
        elif item_name in warehouse1:
           print("Amount Available:",(elm_count_1))
           print("Location: Warehouse1")
        elif item_name in warehouse2:
           print("Amount Available:",(elm_count_2))
           print("Location: Warehouse2")
        else:
           print(item_name,"is not in stock")

    # Else, if they pick 3
    if action==3:
        repeat = False
        print("Thank you for your visit,",user_name,"!")

#that's all for today!
