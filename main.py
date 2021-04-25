import db

db.init()

# execute on start
def on_start_ui():
    # start menu
    actions = ["log in","create account","console"]
    print("""
    ================================================================================
    Welcome to the bank! Please type in one of the following actions to continue.
    ================================================================================

    +----------------+
    |     Log in     |
    +----------------+
    | Create Account |
    +----------------+
    |     Console    |
    +----------------+
    """)
    while True:
        while True:
            choice = input().lower()
            if choice in actions:
                break
        if choice == "log in":
            log_in_ui()
            break
        elif choice == "create account":
            create_account_ui()
            break
        elif choice == "console":
            console_ui()
            break

# log into existing bank account
def log_in_ui():
    name = input("Username: ")
    password = input("Password: ")
    if db.is_user(name, password):
        user_ui(name)
    else:
        print("Wrong username or password!")

# user ui once logged in
def user_ui(name):
    actions = ["balance","withdraw","deposit","modify","disable","enable","delete","transactions","log out"]
    print(f"""
    ================================================================================
    Welcome {name}!

""" + "\n".join(actions) + """
    ================================================================================
    """)
    while True:
        # get action
        while True:
            action = input("Action: ").lower()
            if action in actions:
                break
        if action == "log out":
            break
        elif action == "delete":
            while True:
                password = input("Enter password: ")
                if db.is_user(name,password):
                    break
                else:
                    print("Incorrect password.")
            confirmation = input("Confirm action? ").lower()
            if confirmation == "yes":
                db.delete_account(name)
                break
        elif action == "disable":
            if db.get_status(name):
                print(db.disable_account(name))
            else:
                print("Account already disabled!")
        elif action == "enable":
            if not db.get_status(name):
                print(db.enable_account(name))
            else:
                print("Account already enabled!")
        elif action == "modify":
            while True:
                password = input("Password:")
                if db.is_user(name, password):
                    new_name = input("New name (put none if no new name): ")
                    while True:
                        new_password = input("New password (put none if no new password): ")
                        confirm_password = input("Confirm password (put none if no new password): ")
                        if new_password != confirm_password:
                            print("Password does not match!")
                        else:
                            break
                    if new_name == "none":
                        new_name = None
                    if new_password == "none":
                        new_password = None
                    db.modify_account(name, password, new_name, new_password)
                    print("Changes saved.")
                    break
                else:
                    print("Incorrect password.")
        elif action == "withdraw":
            db.withdraw(name)
        elif action == "deposit":
            db.deposit(name)
        elif action == "balance":
            print(db.get_user_balance(name))

# create bank account
def create_account_ui():
    while True:
        name = input("Enter username: ")
        accounts = db.get_accounts()
        if name in accounts:
            print("Name already taken!")
        else:
            break
    while True:
        password = input("Enter password: ")
        confirm_password = input("Confirm password: ")
        if password != confirm_password:
            print("Passwords do not match!")
        else:
            break
    db.create_account(name, password)
    print("Account created! Please proceed by logging in.")
    return

def input_existing_user():
    while True:
        name = input("User: ")
        if db.user_exists(name):
            break
    return name

# admin access to bank
def console_ui():
    actions = ["add","remove","enable","disable","transaction","transactions","accounts","delete","modify","cancel","process","exit"]

    print(f"""
    ================================================================================
    Welcome Admin!
    
""" + "\n".join(actions) + """
    ================================================================================
    """)

    while True:
        # get action
        while True:
            action = input("Action: ").lower()
            if action in actions:
                break
        
        if action == "transactions":
            print(db.get_transactions())
        elif action == "exit":
            break
        elif action == "transaction":
            transaction_id = input("ID: ")
            transaction_id = int(transaction_id)
            print(db.get_transaction(transaction_id))
        elif action == "accounts":
            print(db.get_accounts())
        elif action == "add":
            name = input_existing_user()
            db.deposit(name)
        elif action == "remove":
            name = input_existing_user()
            db.withdraw(name)
        elif action == "delete":
            name = input_existing_user()
            confirm = input("Confirm action? ").lower()
            if confirm == "yes":
                db.delete_account(name)
        elif action == "enable":
            name = input_existing_user()
            if not db.get_status(name):
                db.enable_account(name)
            else:
                print("Account already enabled!")
        elif action == "disable":
            name = input_existing_user()
            if not db.get_status(name):
                db.enable_account(name)
        elif action == "modify":
            name = input_existing_user()
            password = db.get_password(name)
            new_name = input("New name (put none if no new name): ")
            while True:
                new_password = input("New password (put none if no new password): ")
                confirm_password = input("Confirm password (put none if no new password): ")
                if new_password != confirm_password:
                    print("Password does not match!")
                else:
                    break
            if new_name == "none":
                new_name = None
            if new_password == "none":
                new_password = None
            db.modify_account(name, password, new_name, new_password)
            print("Changes saved.")
            break

# main loop
while True:
    on_start_ui()