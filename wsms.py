# CSC 339-02 Spring 2021
# Program 1
# Name: Thomas Truong
import csv
import os
inventory = {}
pull = {}
csvCounter = 1
binCounter = 1

def load_stock(filename):
    # Reads filename and adds contents to inventory
    global binCounter
    with open (filename, newline = '') as csvfile:
        orderReader = csv.DictReader(csvfile)
        for row in orderReader:
            bin = {binCounter:None}
            inventory.update(bin)
            inventory[binCounter] = {row['item']:row['qty']}
            binCounter += 1
        print(inventory)

def check_stock(item):
    # Returns the in stock quantity of an item
    for key in inventory:
        if item in inventory[key]:
            print("Currently ", item, " has ", inventory[key][item])

def add_stock(item,qty):
    # Increments the stock of the item by qty
    for key in inventory:
        if item in inventory[key]:
            temp = int(qty)
            newQty = int(inventory [key][item])
            newQty += temp
            inventory [key][item] = str(newQty)
            print(item, " now has ", inventory[key][item])

def remove_stock(item,qty):
    # Decrements the stock of the item by qty
    for key in inventory:
        if item in inventory[key]:
            temp = int(qty)
            newQty = int(inventory[key][item])
            if temp <= newQty:
                newQty -= temp
                inventory[key][item] = str(newQty)
                print(item, " now has ", inventory[key][item])
            else:
                print("Cannot remove more than what is in the inventory!")

def pull_order(filename):
    # Reserves the order specified by filename
    # outputs the ordered bin pull list
    binCounter = 1
    with open (filename, newline = '') as csvfile:
        pullNum = {}
        pullReader = csv.DictReader(csvfile)
        for row in pullReader:
            for key in inventory:
                if row['item'] in inventory[key]:
                    pullTemp = int(row['qty'])
                    invTemp = int(inventory[key][row['item']])
                    if pullTemp <= invTemp:
                        remove_stock(row['item'],row['qty'])
                        bin = {binCounter:None}
                        pull.update(bin)
                        pull[binCounter] = {row['item']:row['qty']}
                        binCounter += 1
        csv_maker(pull)
        pull.clear()
def csv_maker(dict):
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
    pass
