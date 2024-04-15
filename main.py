class Table:
    def __init__(self):
        self.waiters = []
        self.customers = 0
        self.orders = []

    def getWaiter(self):
        return self.waiters

    def addWaiter(self, waiter):
        if waiter is not None and waiter not in self.waiters:
            self.waiters.append(waiter)

    def getCustomers(self):
        return self.customers

    def setCustomers(self, customers):
        self.customers = customers

    def getOrders(self):
        return self.orders

    def addOrder(self, item, quantity):
        self.orders.append((item, quantity))

    def clearOrders(self):
        self.orders = []
    
class CashRegister:
    def __init__(self):
        self.sales = []
        self.salesByItem = {}
        self.salesByWaiter = {}

    def add_sale(self, saleAmount, item, waiter):
        self.sales.append(saleAmount)
        self._update_salesByItem(item)
        self._update_salesByWaiter(waiter, saleAmount)

    def calculate_totalIncome(self):
        return sum(self.sales)

    def clear_daily_total(self):
        self.sales = []
        self.salesByItem = {}
        self.salesByWaiter = {}

    def get_salesByItem(self):
        return self.salesByItem

    def get_salesByWaiter(self):
        return self.salesByWaiter

    def _update_salesByItem(self, item):
        if item in self.salesByItem:
            self.salesByItem[item] += 1
        else:
            self.salesByItem[item] = 1

    def _update_salesByWaiter(self, waiter, saleAmount):
        if waiter in self.salesByWaiter:
            self.salesByWaiter[waiter] += saleAmount
        else:
            self.salesByWaiter[waiter] = saleAmount

# ---- Waiter Login System ----
def WaiterLogin(waiterSessions):
    # Check if waiter session exists
    if waiterSessions:
        print("You are already logged in.")
        username = input("Please Enter Username: ")
        if username in waiterSessions:
            loggedInWaiter = username
            print("Login successful.")
            return loggedInWaiter

    # Store the Waiters
    loginCredentials = {}
    # Open Login.txt file to get username and password
    with open('Login.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split(',')
            loginCredentials[username] = password

    # Logic for the login Menu
    while True:
        # Login or Exit to get to Main Program Menu or Quit Program
        try:
            print("1. Login \n2. Exit")
            choice = int(input("Enter Option: "))
            if choice == 1 or choice == 2:
                # Logging In Options
                if choice == 1:
                    print("\nUser Login:\n")
                    username = input("Please Enter Username: ")
                    password = input("Please Enter Password: ")

                    if username in loginCredentials and password == loginCredentials[username]:
                        loggedInWaiter = username
                        print("Login successful.")
                        return loggedInWaiter
                    else:
                        print("Invalid username or password. Please try again.\n")
                # Exiting program completely
                elif choice == 2:
                    exit()
        except ValueError:
            print("Invalid!!! Try again")

# ---- Loading in Items ----
def load_menu_items():
    menuItems = {}
    # Open the Stock.txt file to get the Items
    with open('Stock.txt', 'r') as file:
        for line in file:
            item, price = line.strip().split(',')
            menuItems[item] = float(price)
    return menuItems

# ---- Assigning Tables ----
def AssignTable(loggedInWaiter, tables):
    # Waiter Logged In to get Assigned to a Table
    if loggedInWaiter:
        while True:
            print("Table Status:")
            for table, tableObject in tables.items():
                waiters = tableObject.getWaiter()
                customers = tableObject.getCustomers()
                print(f"Table {table}: Waiters: {', '.join(waiters)}, Customers: {customers}")

            # Input to Assign waiter to a table
            table = int(input("Enter the table number: "))
            if table in tables:
                # Allows waiter to Assign Customers to Table
                customers = int(input("Enter the number of customers: "))
                if customers > 0:
                    tableObject = tables[table]
                    if loggedInWaiter in tableObject.getWaiter():
                        print(f"{loggedInWaiter} is already assigned to Table {table}.")
                        break

                    if len(tableObject.getWaiter()) > 0:
                        print(f"A waiter is already assigned to Table {table}.")
                        break
                    
                    # Adding Waiter and Customers
                    tableObject.addWaiter(loggedInWaiter)
                    tableObject.setCustomers(customers)
                    print(f"Table {table} assigned to {loggedInWaiter}.")
                    print(f"{customers} customers added to Table {table}.")
                    break
                else:
                    print("Invalid number of customers. Please enter a positive integer.")
            else:
                print("Invalid table number.")
    else:
        print("Please log in first.")

# ---- Customers Logic ----
def Customers(loggedInWaiter, tables):
    if loggedInWaiter:
        assignedTables = []

        # Find Tables Assigned to the Waiter
        for table, tableObject in tables.items():
            waiters = tableObject.getWaiter()
            if loggedInWaiter in waiters:
                assignedTables.append(table)

        if assignedTables:
            print(f"Tables assigned to {loggedInWaiter}: {', '.join(str(t) for t in assignedTables)}")
            table = int(input("Enter the table number: "))

            if table in assignedTables:
                customers = int(input("Enter the number of customers: "))
                if customers > 0:
                    tableObject = tables[table]
                    tableObject.setCustomers(customers)
                    print(f"{customers} customers added to Table {table}.")
                else:
                    print("Invalid number of customers. Please enter a positive integer.")
            else:
                print("Invalid table number.")
        else:
            print(f"{loggedInWaiter} is not assigned to any table.")
    else:
        print("Please log in first.")

# ---- Adding an Order ----
def AddOrder(loggedInWaiter, tables, menuItems):
    if loggedInWaiter:
        assignedTables = []

        # Find Tables Assigned to the Waiter
        for table, tableObject in tables.items():
            waiters = tableObject.getWaiter()
            if loggedInWaiter in waiters:
                assignedTables.append(table)

        if assignedTables:
            print(f"Tables assigned to {loggedInWaiter}: {', '.join(str(t) for t in assignedTables)}")
            table = int(input("Enter the table number: "))

            if table in assignedTables:
                print(f"Current table for {loggedInWaiter}: Table {table}")
                print("Menu Items:")
                for i, (item, price) in enumerate(menuItems.items()):
                    print(f"{i + 1}. {item} - R{price}")

                while True:
                    orderNum = int(input("Enter the number of the item to add: "))
                    if orderNum in range(1, len(menuItems) + 1):
                        item = list(menuItems.keys())[orderNum - 1]
                        quantity = int(input("Enter the quantity: "))
                        if quantity > 0:
                            if table in tables:
                                tableObject = tables[table]
                                tableObject.addOrder(item, quantity)
                            else:
                                tableObject = Table()
                                tableObject.addWaiter(loggedInWaiter)
                                tableObject.addOrder(item, quantity)
                                tables[table] = tableObject

                            print(f"{quantity} {item} added to the order at Table {table}.")

                            choice = input("Do you want to add another item? (yes/no): ")
                            if choice.lower() == "no" or choice.lower() == "n":
                                break
                            elif choice.lower() == "yes" or choice.lower() == "y":
                                continue
                            else:
                                print("Invalid choice. Assuming 'no'.")
                                break
                        else:
                            print("Invalid quantity. Please enter a positive integer.")
                    else:
                        print("Invalid item number.")
            else:
                print("Invalid table number.")
        else:
            print(f"{loggedInWaiter} is not assigned to any table.")
    else:
        print("Please log in first.")

# ---- Bill ----
def Bill(loggedInWaiter, tables, menuItems):
    if loggedInWaiter:
        assignedTables = []

        # Find Tables Assigned to the Waiter
        for table, tableObject in tables.items():
            waiters = tableObject.getWaiter()
            if loggedInWaiter in waiters:
                assignedTables.append(table)

        if assignedTables:
            print(f"Tables assigned to {loggedInWaiter}: {', '.join(str(t) for t in assignedTables)}")
            tableNumber = int(input("Enter the table number for which you want to print the bill: "))

            if tableNumber in assignedTables:
                tableObject = tables[tableNumber]
                waiters = tableObject.getWaiter()
                orders = tableObject.getOrders()
                if waiters:
                    # Display for the Bill
                    waiterName = waiters[0]
                    print("\nBill Receipt:")
                    print("---------------------------------------")
                    print("Item\t\tQuantity\tPrice")
                    total = 0
                    for item, quantity in orders:
                        price = menuItems[item]
                        itemTotal = price * quantity
                        total += itemTotal
                        print(f"{item:<16}{quantity:<16}R{price:.2f}")
                    print(f"Total:\t\t\t\t\tR{total:.2f}")
                    print(f"You were helped by {waiterName}\n")
                    print("---------------------------------------\n")

                    tableObject.addWaiter(None)
                else:
                    print(f"No waiter assigned to Table {tableNumber}.")
            else:
                print("Invalid table number.")
        else:
            print(f"{loggedInWaiter} is not assigned to any table.")
    else:
        print("Please log in first.")
        
# ---- Sales ----
def Sales(cashRegister, tables, menuItems):
    if cashRegister is not None:
        # Tracking Total Sales at a Table
        totalSales = 0

        # Display all available Tables
        print("Available Tables:", ", ".join(map(str, tables.keys())))

        # Select a Table
        tableNumber = int(input("Enter the table number to view sales: "))

        if tableNumber in tables:
            tableObject = tables[tableNumber]
            waiters = tableObject.getWaiter()
            orders = tableObject.getOrders()
            customers = tableObject.getCustomers()

            print("\nSales for Table", tableNumber)
            print("Waiters:", ", ".join(waiters))
            print("Customers:", customers)
            print("---------------------------------------")
            print("Item\t\tQuantity\tPrice")
            totalPrice = 0
            for item, quantity in orders:
                price = menuItems[item]
                itemTotal = price * quantity
                totalPrice += itemTotal
                print(f"{item:<16}{quantity:<16}R{price:.2f}")
                # Update Sales amount
                totalSales += itemTotal
            print(f"Total:\t\t\t\t\tR{totalPrice:.2f}")
            print("---------------------------------------\n")

            # Update the cashRegister with Sales made from the Table
            for waiter in waiters:
                cashRegister.add_sale(totalSales, item, waiter)

            # Save Sales to File
            filename = input("Enter a file name to save the sales report (e.g., sales_report.txt): ")

            try:
                with open(filename, "w") as file:
                    file.write(f"Sales report for Table {tableNumber}\n")
                    file.write("Waiters: " + ", ".join(waiters) + "\n")
                    file.write("Customers: " + str(customers) + "\n")
                    file.write("---------------------------------------\n")
                    file.write("Item\t\tQuantity\tPrice\n")
                    for item, quantity in orders:
                        price = menuItems[item]
                        itemTotal = price * quantity
                        file.write(f"{item:<16}{quantity:<16}R{price:.2f}\n")
                    file.write("---------------------------------------\n")
                    file.write(f"Total:\t\t\t\t\tR{totalPrice:.2f}\n")

                print(f"\nSales report for Table {tableNumber} saved to {filename}")

                # Clear values for the Table
                tableObject.clearOrders()
                tableObject.setCustomers(0)
                for waiter in waiters:
                    tableObject.getWaiter().remove(waiter)

            except IOError:
                print("An error occurred while saving the sales report.")
        else:
            print("Invalid table number.")

    else:
        print("Please log in first.")
        
# ---- Cash Up ----
def CashUp(cashRegister, tables, menuItems):
    totalIncome = cashRegister.calculate_totalIncome()
    print(f"Total Income: R{totalIncome:.2f}")

    # Calculate Total Sales from all Orders
    totalSales = 0
    for tableObject in tables.values():
        orders = tableObject.getOrders()
        for item, quantity in orders:
            price = menuItems[item]
            itemTotal = price * quantity
            totalSales += itemTotal

    print(f"Total Sales: R{totalSales:.2f}")

    clearTotal = input("Do you want to clear the daily total? (yes/no): ")
    if clearTotal.lower() == "yes" or clearTotal.lower() == "y":
        cashRegister.clear_daily_total()

    return totalIncome

# ---- Logout ----
def Logout(waiterSessions, loggedInWaiter, cashRegister, tables, menuItems):
    # Store waiter's Login and Session
    waiterSessions[loggedInWaiter] = True
    print("Logged out successfully.")

    # Perform the cash-up
    totalIncome = CashUp(cashRegister, tables, menuItems)
    print(f"Total Income: R{totalIncome:.2f}")

# ---- Main Menu ----
def MainMenu(tables):
    cashRegister = CashRegister()
    menuItems = load_menu_items()
    waiterSessions = {}

    #Main Program Loop
    while True:
        print("Welcome to Highland Café")
        loggedInWaiter = WaiterLogin(waiterSessions)

        while True:
            try:
                print("Main Menu\n")
                print("1. Assign Table \n2. Add customers \n3. Add to Order \n4. Prepare bill \n5. Complete Sale "
                      "\n6. Cash up \n0. Log Out")
                choice = int(input("Enter an Option: "))
                # Main Menu Choices
                if choice >= 0 and choice <= 6:
                    if choice == 0:
                        Logout(waiterSessions, loggedInWaiter, cashRegister, tables, menuItems)
                        break
                    elif choice == 1:
                        AssignTable(loggedInWaiter, tables)
                    elif choice == 2:
                        Customers(loggedInWaiter, tables)
                    elif choice == 3:
                        AddOrder(loggedInWaiter, tables, menuItems)
                    elif choice == 4:
                        Bill(loggedInWaiter, tables, menuItems)
                    elif choice == 5:
                        Sales(cashRegister, tables, menuItems)
                    elif choice == 6:
                        totalIncome = CashUp(cashRegister, tables, menuItems)
                        print(f"Total Income: R{totalIncome:.2f}")
                        logout = input("Do you want to log out? (yes/no): ")
                        if logout.lower() == "yes" or logout.lower() == "y":
                            Logout(waiterSessions, loggedInWaiter, cashRegister, tables, menuItems)
                            break
            except ValueError:
                print("Invalid!!! Try again")
     
tables = {
    1: Table(),
    2: Table(),
    3: Table(),
    4: Table(),
    5: Table(),
    6: Table(),
}

MainMenu(tables)