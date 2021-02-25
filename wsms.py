# CSC 339-02 Spring 2021
# Program 1
# Name: Thomas Truong
import csv
import os
import sys
inventory = {}
pull = {}
csvCounter = 1
inventoryCounter = 1

def load_stock(filename):
    # Reads filename and adds contents to inventory
    # Additionally, checks for headers to have 'item' and 'qty'
    binCounter = 1
    try:
        with open (filename, newline = '') as csvfile:
            orderReader = csv.DictReader(csvfile)
            for row in orderReader:
                bin = {binCounter:None}
                inventory.update(bin)
                inventory[binCounter] = {row['item']:row['qty']}
                binCounter += 1
            print(inventory)
    except KeyError:
        print("CSV formated wrong! Check headers.")

def check_stock(item):
    # Returns the in stock quantity of an item
    # Additionally, checks to see if argument passed is an integer
    if isinstance(item, int):
        for key in inventory:
            if str(item) in inventory[key]:
                print("Currently ", item, " has ", inventory[key][str(item)])
    else:
        print("Error! Item is not in an integer format.")

def add_stock(item,qty):
    # Increments the stock of the item by qty
    # Additionally, checks to see if arguments passed are integers
    if isinstance(item, int) and isinstance(qty, int):
        print("Checking for item number. Will not do anything if not in inventory.")
        for key in inventory:
            if str(item) in inventory[key]:
                temp = qty
                newQty = int(inventory [key][str(item)])
                newQty += temp
                inventory [key][str(item)] = str(newQty)
                print(item, " now has ", inventory[key][str(item)])
    else:
        print("Error! Item or Quantity is not in an integer format.")

def remove_stock(item,qty):
    # Decrements the stock of the item by qty
    # Additionally, checks to see if arguments passed are integers
    if isinstance(item, int) and isinstance(qty, int):
        print("Checking for item number. Will not do anything if not in inventory.")
        for key in inventory:
            if str(item) in inventory[key]:
                temp = int(qty)
                newQty = int(inventory [key][str(item)])
                # Checks to see if user is trying to remove more than what is in the inventory
                if temp <= newQty:
                    newQty -= temp
                    inventory[key][str(item)] = str(newQty)
                    print(item, " now has ", inventory[key][str(item)])
                else:
                    print("Cannot remove more than what is in the inventory!")
    else:
        print("Error! Item or Quantity is not in an integer format.")

def pull_order(filename):
    # Reserves the order specified by filename
    # outputs the ordered bin pull list
    binCounter = 1
    try:
        with open (filename, newline = '') as csvfile:
            pullNum = {}
            pullReader = csv.DictReader(csvfile)
            for row in pullReader:
                for key in inventory:
                    if row['item'] in inventory[key]:
                        pullTemp = int(row['qty'])
                        invTemp = int(inventory[key][row['item']])
                        # Checks to see if user is trying to remove more than what is in the inventory
                        if pullTemp <= invTemp:
                            remove_stock(int(row['item']),int(row['qty']))
                            bin = {binCounter:None}
                            pull.update(bin)
                            pull[binCounter] = {row['item']:row['qty']}
                            binCounter += 1
        # Calls a function to make a csv file for the pull order and clears the pull list for next pull order
        csv_maker(pull)
        pull.clear()
    except KeyError:
        print("CSV formated wrong! Check headers.")

def csv_maker(dict):
    # Makes a unique csv file using the dictionary as an argument
    # csv file will contain bin numbers
    global csvCounter
    filename = "pull_" + str(csvCounter) + ".csv"
    with open(filename, 'w', newline = '') as csvfile:
        csv_columns = ['bin', 'item', 'qty']
        pullWriter = csv.DictWriter(csvfile, fieldnames=csv_columns)
        pullWriter.writeheader()
        for bin, item in pull.items():
            for key in item:
                pullWriter.writerow({'bin': bin, 'item': key, 'qty': item[key]})
    print('\nCSV File: ' + filename)
    print('Use this for fill_order or restock_order')
    csvCounter += 1

def exit_inventory(dict):
    # Exit function used to create a csv file of current inventory for next session
    global inventoryCounter
    filename = "inventory_" + str(inventoryCounter) + ".csv"
    with open(filename, 'w', newline = '') as csvfile:
        inventory_columns = ['item', 'qty']
        inventoryWriter = csv.DictWriter(csvfile, fieldnames=inventory_columns)
        inventoryWriter.writeheader()
        for bin, item in inventory.items():
            for key in item:
                inventoryWriter.writerow({'item': key, 'qty': item[key]})
        print('\Inventory File: ' + filename)
        print('Use this for the next session when loading csv file.')
        inventoryCounter += 1

def exit_stock():
    # Exit function to call another function that will make a csv and then exit the program
    exit_inventory(inventory)
    sys.exit()

def fill_order(filename):
    # Deletes the specified pull list from the system
    os.remove(filename)

def restock_order(filename):
    # Reads the given pull list to reverse the order
    # Deletes the pull list from the system
    with open (filename, newline = '') as csvfile:
        restockReader = csv.DictReader(csvfile)
        for row in restockReader:
            for key in inventory:
                if row['item'] in inventory[key]:
                    add_stock(row['item'],row['qty'])
    fill_order(filename)

def print_stock():
    # Prints the stock of each bin
    for key, value in inventory.items():
        print(key, " : ", value)
