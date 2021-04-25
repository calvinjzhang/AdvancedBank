import sqlite3

conn = None
accounts = {}
transactions = {}

def create_table(sql_create_table):
    try:
        c = conn.cursor()
        c.execute(sql_create_table)
    except sqlite3.Error as e:
        print(e)

def init():
    global conn
    db_file = "bankdatabase.db"
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    sql_create_table_accounts = """CREATE TABLE IF NOT EXISTS accounts (
                name text PRIMARY KEY,
                password text NOT NULL,
                balance real NOT NULL,
                status integer NOT NULL
            );"""
    create_table(sql_create_table_accounts)

    sql_create_table_transactions = """CREATE TABLE IF NOT EXISTS transactions (
                transaction_id integer PRIMARY KEY,
                name text NOT NULL,
                action text NOT NULL,
                amount real NOT NULL,
                balance real NOT NULL,
                status integer NOT NULL
            );"""
    create_table(sql_create_table_transactions)

    queryAccounts()
    queryTransactions()

def queryAccounts():
    global accounts
    cur = conn.cursor()
    cur.execute("SELECT * FROM accounts")

    rows = cur.fetchall()
    accounts.clear()
    
    for row in rows:
        accounts[row[0]] = (row[1], row[2], row[3])

def queryTransactions():
    global transactions
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions")

    rows = cur.fetchall()
    transactions.clear()
    
    for row in rows:
        transactions[row[0]] = (row[1], row[2], row[3], row[4], row[5])

def create_account(name, password):
    sql_add_account = """INSERT INTO accounts (name, password, balance, status) VALUES (?,?,?,?)"""
    para = (name, password, 0, 1)
    try:
        conn.execute(sql_add_account, para)
    except sqlite3.IntegrityError:
        return "Name " + name + " already exists! Please choose another name."
    except sqlite3.Error as e:
        return str(e)
    conn.commit()
    queryAccounts()
    return

def user_exists(name):
    accounts = get_accounts()
    if name in accounts:
        return True
    return False

def is_user(name, password):
    accounts = get_accounts()
    if name in accounts:
        if accounts[name][0] == password:
            return True
    return False

def get_status(name):
    accounts = get_accounts()
    if accounts[name][2] == 1:
        return True
    return False

def get_password(name):
    accounts = get_accounts()
    return accounts[name][0]

def delete_account(name):
    queryAccounts()
    sql_del_account = """DELETE FROM accounts WHERE name = ?"""
    para = (name,)
    try:
        conn.execute(sql_del_account, para)
    except sqlite3.Error as e:
        return str(e)
    conn.commit()
    queryAccounts()
    return

def disable_account(name):
    queryAccounts()
    sql_modify_account = """UPDATE accounts SET status = ? WHERE name = ?"""
    para = (0, name)
    try:
        conn.execute(sql_modify_account, para)
    except sqlite3.Error as e:
        return str(e)
    conn.commit()
    queryAccounts()
    return "Account disabled."

def enable_account(name):
    queryAccounts()
    sql_modify_account = """UPDATE accounts SET status = ? WHERE name = ?"""
    para = (1, name)
    try:
        conn.execute(sql_modify_account, para)
    except sqlite3.Error as e:
        return str(e)
    conn.commit()
    queryAccounts()
    return "Account enabled."

def modify_account(name, password, new_name, new_password):
    queryAccounts()
    if new_name == None:
        new_name = name
    if new_password == None:
        new_password= password
    sql_modify_account = """UPDATE accounts SET name = ?, password = ? WHERE name = ?"""
    para = (new_name, new_password, name)
    try:
        conn.execute(sql_modify_account, para)
    except sqlite3.Error as e:
        return str(e)
    conn.commit()
    queryAccounts()
    return

def create_transaction(name,action,amount):
    transaction_id = get_next_transaction_id()
    balance = get_user_balance(name)
    sql_add_transaction = """INSERT INTO transactions (transaction_id, name, action, amount, balance, status) VALUES (?,?,?,?,?,?)"""
    para = (transaction_id,name, action, amount, balance, 1)
    try:
        conn.execute(sql_add_transaction, para)
    except sqlite3.IntegrityError:
        return "Integrity Error"
    except sqlite3.Error as e:
        return str(e)
    conn.commit()
    queryTransactions()
    return

def get_transaction(transaction_id):
    transactions = get_transactions()
    try:
        return transactions[transaction_id]
    except:
        return None

def get_user_balance(name):
    accounts = get_accounts()
    return accounts[name][1]

def get_user_transactions():
    user_transactions = {}
    return

def get_next_transaction_id():
    return len(get_transactions())+1

def withdraw(name):
    queryAccounts()
    if get_status(name):
        while True:
            amount = input("What amount would you like to withdraw? ")
            try:
                amount = float(amount)
                if amount < 0:
                    print("Must be non-negative!")
                else:
                    break
            except:
                pass
    else:
        print("Account is disabled right now!")
        return
    balance = get_user_balance(name)
    balance -= amount
    if balance < 0:
        print("Withdrawing too much!")
        return
    sql_modify_account = """UPDATE accounts SET balance = ? WHERE name = ?"""
    para = (balance, name)
    try:
        conn.execute(sql_modify_account, para)
    except sqlite3.Error as e:
        return str(e)
    conn.commit()
    queryAccounts()

    create_transaction(name, "withdraw", amount)
    print("Transaction completed!")
    return

def deposit(name):
    queryAccounts()
    if get_status(name):
        while True:
            amount = input("What amount would you like to deposit? ")
            try:
                amount = float(amount)
                if amount < 0:
                    print("Must be non-negative!")
                else:
                    break
            except:
                pass
    else:
        print("Account is disabled right now!")
        return
    balance = get_user_balance(name)
    balance += amount
    sql_modify_account = """UPDATE accounts SET balance = ? WHERE name = ?"""
    para = (balance, name)
    try:
        conn.execute(sql_modify_account, para)
    except sqlite3.Error as e:
        return str(e)
    conn.commit()
    queryAccounts()

    create_transaction(name, "deposit", amount)
    print("Transaction completed!")
    return

def modify_transaction(id):
    return

def get_accounts():
    global accounts
    queryAccounts()
    return accounts

def get_transactions():
    global transactions
    queryTransactions()
    return transactions