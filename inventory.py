# Import modules.

import csv
import os
from tabulate import tabulate

#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = int(cost)
        self.quantity = int(quantity)

    def get_country(self):
        return self.country

    def get_code(self):
        return self.code

    def get_product(self):
        return self.product

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def get_value(self):
        return self.cost * self.quantity

    def get_dic(self):
        return {"Country": self.country, "Code": self.code, "Product Name": self.product, "Cost in ZAR": self.cost, "Quantity": self.quantity}

    def __str__(self):
        return f"Country: {self.country}, Code: {self.code}, Product Name: {self.product}, Cost in ZAR: {self.cost}, Quantity: {self.quantity}"
    
    # This class return the sum of the quantity of two shoes.
    def __add__(self, new):

        if isinstance(new, Shoe):
            self.quantity = int(self.quantity) + int(new.quantity)
        elif isinstance(new, int):
            self.quantity = int(self.quantity) + new
        elif isinstance(new, str):
            try:
                self.quantity = int(self.quantity) + int(new)
            except:
                pass
        return self


def main():
    os.system("clear")
    shoe_list = []

    # Read shoe list from file.
    shoe_list = read_shoes_data()
    
    #==========Main Menu=============

    menu = "Choose from the options below:\n\n"
    menu += "   C - Capture shoe\n"
    menu += "  VA - View All\n"
    menu += "   R - Re-stock shoe\n"
    menu += "   S - Search shoe\n"
    menu += "   V - Value per item\n"
    menu += "   H - Highest Quantity in stock\n"
    menu += "Exit - to terminate the program\n\n"

    while True:
        choice = input(menu).lower()

        if choice == "c":
            new_shoe = capture_shoes(shoe_list)
            same_shoe = False

            for shoe in shoe_list:

                if shoe.get_country()==new_shoe.get_country() and shoe.get_code()==new_shoe.get_code():
                    shoe = shoe + new_shoe
                    print(f"\n *** Shoe already existing ***\n\n{new_shoe.get_quantity()} items added to stock:\n\n{shoe}\n")
                    same_shoe = True
            
            if same_shoe:
                pass
            else:
                shoe_list.append(new_shoe)
                print(f"\n *** New shoe recorded ***\n\n{new_shoe}\n")

            save_shoes_data(shoe_list)

        # If the variable shoe_list is empty the program returns to the main menu.
        elif shoe_list == []:
            os.system("clear")
            print(" *** Shoe list is empty *** \n")
            continue

        elif choice == "va":
            os.system("clear")
            output = view_all(shoe_list)
            if output:
                print(tabulate(output, headers="keys", tablefmt="pretty"))
            else:
                os.system("clear")

        elif choice == "r":
            os.system("clear")
            output = re_stock(shoe_list)
            if output:
                shoe_list = read_shoes_data()
                print(tabulate(view_all(shoe_list), headers="keys", tablefmt="pretty"))

        elif choice == "s":
            os.system("clear")
            output = search_shoe(shoe_list)
            if isinstance(output, list):
                print(tabulate(output, headers="keys", tablefmt="pretty"))

        elif choice == "v":
            os.system("clear")
            output = value_per_item(shoe_list)
            if isinstance(output, list):
                print(tabulate(output, headers="keys", tablefmt="pretty"))

        elif choice == "h":
            os.system("clear")
            print(highest_qty(shoe_list))

        elif choice == "exit":
            os.system("clear")
            print("Good bye!\n")
            exit()

        else:
            print("Invalid choice...\n")
            continue
        

#==========Functions outside the class==============
def read_shoes_data():
    """
    This function opens the file 'inventory.txt',
    reads the data from this file, then creates a shoe object with this data,
    and append this object into the shoes list.
    One line in this file represents data to create one object of shoes.
    """

    shoe_list = []
    try:
        with open("inventory.txt", encoding="utf-8") as openfile:
            inventory = csv.DictReader(openfile)

            for row in inventory:
                shoe_list.append(Shoe(*(row[key] for key in row.keys())))
    except FileNotFoundError:
        pass
    
    return shoe_list


def capture_shoes(shoe_list):
    """
    This function allows a user to capture data
    about a shoe and uses this data to create a shoe object
    then appends this object inside the shoe list.
    """    
    code_list = []
    product_list = []
    cost_list = []

    for shoe in shoe_list:
        code_list.append(shoe.code)
        product_list.append(shoe.product)
        cost_list.append(shoe.cost)
    
    country = input("\nPlease enter the country: ").title()
    code = input("Enter the shoe code: ").upper()
    
    if code in code_list:
        product = product_list[(code_list.index(code))]
        print(f"\nThe code '{code}' corrispond to the model '{product}'\n")
        cost = cost_list[(code_list.index(code))]
    else:
        product = input("Enter the product name: ").title()
        while True:
            try:
                cost = int(input("Enter the cost: "))
                break
            except ValueError:
                print("\n *** Invalid input *** \nPlease enter integers only.\n")

    while True:
        try:
            quantity = int(input("Enter the quantity: "))
            break
        except ValueError:
            print("\n *** Invalid input *** \nPlease enter integers only.\n")

    new_shoe = Shoe(country, code, product, cost, quantity)
    return new_shoe


def view_all(shoe_list):
    """
    This function iterates over the shoes list and
    returns the details of the shoes to be printed in a table
    """
    tab = []

    for shoe in shoe_list:
        tab.append(shoe.get_dic())

    return tab


def re_stock(shoe_list):
    """
    This function finds the shoe object with the lowest quantity,
    Ask the user if they want to re-stock this shoe
    Then updates the file with the new quantity.
    """
    stock = []
    for shoe in shoe_list:
        stock.append(shoe.get_quantity())
    
    index = stock.index(min(stock))
    
    print(f"You are running low on this article:\n\n{shoe_list[index]}\n")
    choice = input("Would you like to re-stock it? [y/n]")
    
    while True:
        
        if choice == "y":
            while True:
                try:
                    to_order = int(input("How many would you like to order? "))
                    break
                except ValueError:
                    print("\n *** Invalid input *** \nPlease enter integers only.")

            shoe_list[index] = shoe_list[index] + to_order
            save_shoes_data(shoe_list)
            return True

        elif choice == "n":
            os.system("clear")
            return False
        else:
            choice = input("\n *** Invalid choice *** \n\nPlease enter:\n'y' if you want to re-stock the shoe\n'n' if you don't want to re-stock it.\n")


def search_shoe(shoe_list):
    """
    This function searches for a shoe from the list
    using the shoe code and returns this object to be printed.
    """
    codes = []
    for shoe in shoe_list:
        codes.append(shoe.get_code())
    while True:
        to_search = input("Enter the shoe code you are looking for: ").upper()
        print()
        count = 0
        shoes = []
        for shoe in shoe_list:
            if shoe.get_code() == to_search:
                shoes.append(shoe.get_dic())
                count += 1
            else:
                pass
        
        if count > 0:
            return shoes

        choice = input(f"\n *** The code {to_search} does not match any registered shoe *** \n\nWould you like to enter a new code? [y/n]\n")
        while True:
            if choice == "y":
                break
            elif choice == "n":
                os.system("clear")
                return
            else:
                choice = input("\n *** Invalid choice *** \n\nPlease enter:\n'y' if you want to search for another code\n'n' if you want to stop the search.\n")
                continue


def value_per_item(shoe_list):
    """
    This function calculates the total value for each item,
    then returns the list of values to be printed in a table.
    """
    new_list = []
    items = []

    for shoe in shoe_list:
        product = shoe.get_product()
        value = shoe.get_value()

        if product in items:
            value += shoe_list[items.index(product)].get_value()
            new_list[items.index(product)].update({"Product": product, "Value": value})
        else:
            items.append(product)
            new_list.append({"Product Name": product, "Value in ZAR": value})

    return new_list    


def highest_qty(shoe_list):
    """
    This function finds the product with the highest quantity and
    prints this shoe as being for sale.
    """
    stock = []
    for shoe in shoe_list:
        stock.append(shoe.get_quantity())
    
    index = stock.index(max(stock))
    
    to_print = "The following shoe is for sale:\n\n"
    to_print += f"Model ·········· : {shoe_list[index].get_product()}\n"
    to_print += f"Price ·········· : {shoe_list[index].get_cost()} ZAR\n"
    to_print += f"Availability ··· : {shoe_list[index].get_quantity()} pairs\n"

    return to_print
    

def save_shoes_data(shoe_list):
    """
    This function write the data to the file 'inventory.txt'.
    """
    with open("inventory.txt", "w+", encoding="utf-8") as writefile:
        writefile.write("Country,Code,Product,Cost,Quantity\n")

        for shoe in shoe_list:
            writefile.write(f"{shoe.get_country()},{shoe.get_code()},{shoe.get_product()},{shoe.get_cost()},{shoe.get_quantity()}\n")


if __name__ == "__main__":
    main()