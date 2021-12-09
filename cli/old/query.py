from data import warehouse1, warehouse2
import argparse

parser = argparse.ArgumentParser()
user_name = ""  # setting empty user name for argument parse
repeat = True  # setting the loop variable

# Adding optional argument
parser.add_argument("--user_name", help="ENTER YOUR USER NAME")
args = parser.parse_args()

if (
    args.user_name
):  # if I  put --user name when I start the program , it takes the name from the argument
    user_name = args.user_name
else:
    user_name = input("What is your user name?: ")

if user_name == "":  # if user name was not provided we set it to 'stranger'
    user_name = "stranger"

print("Greetings", user_name, "!")

# start of main loop. This loop allows the user to continue using the menu of the program instead of running it from start
while repeat:
    print("How can I be of service?")

    action = int(
        input(
            "1. List items by Warehouse?\n2. Search an item and place an order?\n3. Quit\n---Type the number of the operation:  "
        )
    )
    # start of action1
    if action == 1:
        print("Warehouse1:")
        for i in warehouse1:
            print("- ", i)
        print("warehouse2")
        for i in warehouse2:
            print("- ", i)
    # end of action 1
    # start of action 2
    elif action == 2:
        item_name = input("What is the name of the item?: ")
        elm_count_1 = warehouse1.count(item_name)
        elm_count_2 = warehouse2.count(item_name)
        # printing availability
        if item_name in warehouse1 and warehouse2:
            print("Location: Both Warehouses")
            print("Amount Available:", (elm_count_1 + elm_count_2))
            if elm_count_1 > elm_count_2:
                print("Maximum availability:", (elm_count_1), "in Warehouse 1")
            elif elm_count_1 < elm_count_2:
                print("Maximum availability:", (elm_count_2), "in Warehouse 2")
            else:
                print(
                    "Product exists in similar quantities in both warehouses:",
                    elm_count_1,
                    "in warehouse1 ",
                    "and",
                    elm_count_2,
                    "in warehouse2",
                )

        elif item_name in warehouse1:
            print("Amount Available:", (elm_count_1))
            print("Location: Warehouse1")
        elif item_name in warehouse2:
            print("Amount Available:", (elm_count_2))
            print("Location: Warehouse2")
        else:
            print(item_name, "is not in stock")
            continue  # resets the loop
        # end of printing availability
        # start of placind order

        print("Would you like to place an order for this item?")
        order_action = int(
            input("1.Yes \n2.No\n: ---Type the number of the operation:  ")
        )
        if order_action == 1:
            item_number = int(input("How many items would you like?:  "))
            # checking if we have enough items
            if item_number <= (elm_count_1 + elm_count_2):  # if yes
                print(
                    "An order of",
                    (elm_count_1 + elm_count_2),
                    item_name,
                    "has been placed",
                )  # make order
            else:  # if not
                print(
                    "There are not this many items available.The maximum amount that can be ordered is ",
                    (elm_count_1 + elm_count_2),
                )  # say we don't have that many items
                max_order = int(
                    input(
                        "Would you like to order the maximum amount available?,\n1.Yes\n2.No\n:---Type the number of the operation:  "
                    )
                )  # ask if they want to order what we have
                if max_order == 1:  # if yes
                    print(
                        "An order of",
                        (elm_count_1 + elm_count_2),
                        item_name,
                        "has been placed",
                    )  # print that order is placed

    # rnd of placing order
    # end of action2
    # start of action3
    elif action == 3:
        repeat = False
        print("Safe travels,", user_name, "!")
    else:
        print("type a valid operator!")


# that's all folks!
