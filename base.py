import sqlite3

# что-то с пользователями
# def AddUser(username, password, tel):
#     dataBase = sqlite3.connect("mydb.sql")
#     cursor = dataBase.cursor()
#     cursor.execute("INSERT INTO users (username, password, tel) VALUES (?, ?, ?)", (username, password, tel))
#     dataBase.commit()
#     dataBase.close()

def AddEaters(username, password, tel):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute("INSERT INTO eaters (username, password, tel, attendance, allergens, payment, balans) VALUES (?, ?, ?, ?, ?, ?, ?)", (username, password, tel, "", "", "", 0))
    dataBase.commit()
    dataBase.close()

# def ChekUserEnter(username, password):
#     dataBase = sqlite3.connect("mydb.sql")
#     cursor = dataBase.cursor()
#     cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
#     dataUsers = cursor.fetchall()
#     if dataUsers != []:
#         return True
#     return False
def getDataEters(username, password):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    # cursor.execute(
    #     """CREATE TABLE IF NOT EXISTS eaters (username TEXT, password TEXT, tel TEXT, attendance TEXT, attendance TEXT, payment TEXT, balans TEXT)""")
    cursor.execute("SELECT * FROM eaters WHERE username = ? AND password = ?", (username, password))
    dataUsers = cursor.fetchall()
    print(dataUsers)
    if dataUsers != []:
        return dataUsers[0]
    return None



def chengEters(username, password, whatCheng, newValue):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute("SELECT * FROM eaters WHERE username = ? AND password = ?", (username, password))
    cursor.execute(f"UPDATE eaters SET {whatCheng} = ? WHERE username = ?", (newValue, username))
    dataBase.commit()
    dataBase.close()

def ChekUserCreat(username, where):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute(f"SELECT * FROM {where} WHERE username = ?", (username,))
    dataUsers = cursor.fetchall()
    if dataUsers != []:
        return True
    return False

def AddCookAndAdmin(username, password, where):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute(f"DELETE FROM {where} WHERE username = ? AND password = ?", (username, password))
    cursor.execute(f"INSERT INTO {where} (username, password) VALUES (?, ?)", (username, password))
    dataBase.commit()
    dataBase.close()

def findUser(username, password, where):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute(f"SELECT * FROM {where} WHERE username = ? AND password = ?", (username, password))
    dataUsers = cursor.fetchall()
    if dataUsers != []:
        return True
    return False

# что-то с меню
def getData(what):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute(f"SELECT * FROM {what}")
    dataMenu = cursor.fetchall()
    return dataMenu

def AddFood(day, meal, food, cost, col):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute(f"SELECT * FROM manuOnweek WHERE day = ? AND meal = ?", (day, meal))
    dataMenu = cursor.fetchall()
    if dataMenu == []:
        cursor.execute("INSERT INTO manuOnweek (day, meal, food, cost, col, colpistart) VALUES (?, ?, ?, ?, ?, ?)",
                       (day, meal, food, cost, col, col))
        dataBase.commit()
        dataBase.close()
        return True  # добавлено
    return False # уже существует

def payFood(day, meal):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute("SELECT * FROM manuOnweek WHERE day = ? AND meal = ?", (day, meal))
    data = cursor.fetchall()
    print(data, data[-1])
    cursor.execute(f"UPDATE manuOnweek SET col = ? WHERE day = ? AND meal = ?", (int(data[0][-1])-1 ,day, meal))
    dataBase.commit()
    dataBase.close()

def ChengFoodForManu(day, meal, food, cost, col):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute(f"SELECT * FROM manuOnweek WHERE day = ? AND meal = ?", (day, meal))
    dataMenu = cursor.fetchall()
    if dataMenu != []:
        cursor.execute("DELETE FROM manuOnweek WHERE day = ? AND meal = ?", (day, meal))
        cursor.execute("INSERT INTO manuOnweek (day, meal, food, cost, col, colpistart) VALUES (?, ?, ?, ?, ?, ?)",
                       (day, meal, food, cost, col, col))
        dataBase.commit()
        dataBase.close()
        return True  # изменено
    return False # не существует

def addComments(userName, text):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    try:
        cursor.execute("INSERT INTO comments (who, value) VALUES (?, ?)",
                       (userName, text))
        dataBase.commit()
        dataBase.close()
        return True
    except:
        dataBase.commit()
        dataBase.close()
        return False

def getAllComments():
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    try:
        cursor.execute(f"SELECT * FROM comments")
        data = cursor.fetchall()
        print(data, "gggggg")
        return data
    except:
        return None

def vidat(what):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute("SELECT * FROM chtoWidano")
    data = cursor.fetchall()
    # if data == []:
    #     cursor.execute("INSERT INTO chtoWidano (Z, O) VALUES (?, ?)",
    #                    (0, 0))
    print(data)
    i = 0
    if what == "Z":
        i = 0
    elif what == "O":
        i = 1
    cursor.execute(f"UPDATE chtoWidano SET {what} = ?", (int(data[0][i])+1,))
    dataBase.commit()
    dataBase.close()

def newWeek():
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute("SELECT * FROM chtoWidano")
    cursor.execute(f"UPDATE chtoWidano SET Z = ? AND O = ?", (0, 0))
    cursor.execute("SELECT * FROM eaters")
    cursor.execute(f"UPDATE eaters SET payment = ?", ("",))
    cursor.execute("SELECT * FROM manuOnweek")
    data = cursor.fetchall()
    for i in range(len(data)):
        cursor.execute(f"UPDATE manuOnweek SET col = ?, WHERE day = ? and meal = ?", (data[i][-1], data[i][0], data[i][1]))
    dataBase.commit()
    dataBase.close()

def addPurchaseRequests(who, value):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute("SELECT * FROM purchaseRequests")
    data = cursor.fetchall()
    cursor.execute("INSERT INTO purchaseRequests (who, value) VALUES (?, ?)",
                   (who, value))
    dataBase.commit()
    dataBase.close()
def Start():
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()

    # cursor.execute("""CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, tel TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS eaters (username TEXT, password TEXT, tel TEXT, attendance TEXT, allergens TEXT, payment TEXT, balans INTEGER)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS admins (username TEXT, password TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS cooks (username TEXT, password TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS manuOnweek (day TEXT, meal TEXT ,food TEXT, cost TEXT, col INTEGER, colpistart INTEGER)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS purchaseRequests (who TEXT, value TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS comments (who TEXT, value TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS chtoWidano (Z INTEGER, O INTEGER)""")
    cursor.execute("SELECT * FROM chtoWidano")
    data = cursor.fetchall()
    if data == []:
        cursor.execute("INSERT INTO chtoWidano (Z, O) VALUES (?, ?)",
                       (0, 0))

    dataBase.commit()
    dataBase.close()