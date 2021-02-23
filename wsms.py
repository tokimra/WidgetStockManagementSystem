# CSC 339-02 Spring 2021
# Program 1
# Name: Thomas Truong
import csv
inventory = {}
pull = {}

def load_stock(filename):
    # Reads filename and adds contents to inventory
    binCounter = 0
    bin = {binCounter:None}
    with open (filename, newline = '') as csvfile:
        orderReader = csv.DictReader(csvfile)
        for row in orderReader:
            inventory.update(bin)
            inventory[binCounter] = {row['item']:row['qty']}
            binCounter += 1
        print(inventory)

def check_stock(item):
    # Returns the in stock quantity of an item
    for key in inventory:
        if item in inventory[key]:
            print("Currently ", item, " has ", inventory[x][item])

def add_stock(item,qty):
    # Increments the stock of the item by qty
    if item in inventory:
        temp = int(qty)
        newQty = int(inventory [item])
        newQty += temp
        inventory [item] = str(newQty)
        print(item, " now has ", inventory[item])
    else:
        print("Invalid item number!")

def remove_stock(item,qty):
    # Decrements the stock of the item by qty
    if item in inventory:
        temp = int(qty)
        newQty = int(inventory [item])
        if temp <= newQty:
            newQty -= temp
            inventory [item] = str(newQty)
            print(item, " now has ", inventory[item])
        else:
            print("Cannot remove more than what is in the inventory!")
    else:
        print("Invalid item number!")

def pull_order(filename):
    # Reserves the order specified by filename
    # outputs the ordered bin pull list
    with open (filename, newline = '') as csvfile:
        pullNum = {}
        pullReader = csv.DictReader(csvfile)
        for row in pullReader:
            if row['item'] in inventory:
                pullTemp = int(row['qty'])
                invTemp = int(inventory[row['item']])
                if pullTemp <= invTemp:
                    remove_stock(row['item'],row['qty'])
                    pullNum = {row['item']:row['qty']}
                else:
                    print(row['item']," Cannot reserve more than inventory!")
            else:
                print(row['item'], " is not in inventory to reserve")
    with open('pullorder.csv', 'w', newline = '') as f:
        fieldnames = ['item', 'quantity']
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        thewriter.writeheader()
        for row in pullNum:
            thewriter.writerow({row['item'] : item, row['quantity'] : qty})

def fill_order(filename):
    # Deletes the specified pull list from the system
    with open (filename, newline = '') as csvfile:
        fillReader = csv.DictReader(csvfile)
        for row in fillReader:
            if row['item'] in pull:
                del pull[row['item']]
            else:
                print(row['item'], " is not in pull list to fill")
        print("Pull list", pull)

def restock_order(filename):
    # Reads the given pull list to reverse the order
    # Deletes the pull list from the system
    with open (filename, newline = '') as csvfile:
        restockReader = csv.DictReader(csvfile)
        for row in restockReader:
            if row['item'] in pull:
                add_stock(row['item'], row['qty'])
                del pull[row['item']]
            else:
                print(row['item'], " is not in list to restock")
        print("Pull list", pull)

def print_stock():
    # Prints the stock of each bin
    for key, value in inventory.items():
        print(key, " : ", value)
    pass
