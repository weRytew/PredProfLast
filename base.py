import sqlite3
import uuid
import hashlib
import os

def MakeHash(data):
    return hashlib.sha256(data.encode())

def AddEaters(username, password, tel):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    password = MakeHash(password).hexdigest()
    cursor.execute("INSERT INTO eaters (username, password, tel, attendance, allergens, payment, history, balans) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (username, password, tel, "", "", "", "", 0))
    dataBase.commit()
    dataBase.close()

def getDataEters(username):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute("SELECT * FROM eaters WHERE username = ?", (username,))
    dataUsers = cursor.fetchall()
    if dataUsers != []:
        return dataUsers[0]
    return None

def chengEters(username, whatCheng, newValue):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute("SELECT * FROM eaters WHERE username = ?", (username,))
    cursor.execute(f"UPDATE eaters SET {whatCheng} = ? WHERE username = ?", (newValue, username))
    dataBase.commit()
    dataBase.close()

def ChekUserCreatForReg(username):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute(f"SELECT * FROM eaters WHERE username = ?", (username,))
    dataUsers = cursor.fetchall()
    cheker = True
    if dataUsers != []:
        cheker = False
    cursor.execute(f"SELECT * FROM admins WHERE username = ?", (username,))
    dataUsers = cursor.fetchall()
    if dataUsers != []:
        cheker = False
    cursor.execute(f"SELECT * FROM cooks WHERE username = ?", (username,))
    dataUsers = cursor.fetchall()
    if dataUsers != []:
        cheker =  False
    return cheker

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
    password = MakeHash(password).hexdigest()
    cursor = dataBase.cursor()
    cursor.execute(f"DELETE FROM {where} WHERE username = ? AND password = ?", (username, password))
    cursor.execute(f"INSERT INTO {where} (username, password) VALUES (?, ?)", (username, password))
    dataBase.commit()
    dataBase.close()

def findUser(username, password, where):
    dataBase = sqlite3.connect("mydb.sql")
    password = MakeHash(password).hexdigest()
    cursor = dataBase.cursor()
    cursor.execute(f"SELECT * FROM {where} WHERE username = ? AND password = ?", (username, password))
    dataUsers = cursor.fetchall()
    if dataUsers != []:
        return True
    return False

def findUserCook(username):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute(f"SELECT * FROM cooks WHERE username = ?", (username,))
    dataUsers = cursor.fetchall()
    if dataUsers != []:
        return True
    return False

def getData(what):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute(f"SELECT * FROM {what}")
    data = cursor.fetchall()
    return data

def AddFood(day, meal, food, cost, col, costForstol):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute(f"SELECT * FROM manuOnweek WHERE day = ? AND meal = ?", (day, meal))
    dataMenu = cursor.fetchall()
    if dataMenu == []:
        cursor.execute("INSERT INTO manuOnweek (day, meal, food, cost, col, colpistart, costForstol) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (day, meal, food, cost, col, col, costForstol))
        dataBase.commit()
        dataBase.close()
        return True
    elif dataMenu != []:
        cursor.execute("DELETE FROM manuOnweek WHERE day = ? AND meal = ?", (day, meal))
        cursor.execute(
            "INSERT INTO manuOnweek (day, meal, food, cost, col, colpistart, costForstol) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (day, meal, food, cost, col, col, costForstol))
        dataBase.commit()
        dataBase.close()
        return True
    return False

def delFood(day, meal):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute(f"SELECT * FROM manuOnweek WHERE day = ? AND meal = ?", (day, meal))
    dataMenu = cursor.fetchall()
    if dataMenu != []:
        cursor.execute("DELETE FROM manuOnweek WHERE day = ? AND meal = ?", (day, meal))
        dataBase.commit()
        dataBase.close()
        return True
    return False

def payFood(day, meal):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute("SELECT * FROM manuOnweek WHERE day = ? AND meal = ?", (day, meal))
    data = cursor.fetchall()
    cost =  data[0][3]
    cursor.execute("SELECT * FROM pribForWeek")
    pribBefore = cursor.fetchall()[0]
    cursor.execute("UPDATE pribForWeek SET prib = ?, opl = ?", (pribBefore[0] + int(cost), pribBefore[1] + " " + day))
    cursor.execute(f"UPDATE manuOnweek SET col = ? WHERE day = ? AND meal = ?", (int(data[0][4])-1 ,day, meal))
    dataBase.commit()
    dataBase.close()

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
        return data
    except:
        return None

def getAllEaters():
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    try:
        cursor.execute(f"SELECT * FROM eaters")
        data = cursor.fetchall()
        return data
    except:
        return None


def attendanceEters(username, attend):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    try:
        attendP = (getDataEters(username))[0][3]
        an = attendP + attend
        cursor.execute(f"UPDATE eaters SET attendance = ? WHERE username = ?", (an, username))
        dataBase.commit()
        dataBase.close()
    except Exception as e:
        print(e)

def vidat(what):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute("SELECT * FROM chtoWidano")
    data = cursor.fetchall()
    i = 0
    if what == "Z":
        i = 0
    elif what == "O":
        i = 1
    cursor.execute(f"UPDATE chtoWidano SET {what} = ?", (int(data[0][i])+1,))
    dataBase.commit()
    dataBase.close()



def newWeek():
    print("dddd")
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute("SELECT * FROM chtoWidano")
    cursor.execute(f"UPDATE chtoWidano SET Z = ?, O = ?", (0, 0))
    cursor.execute("SELECT * FROM eaters")
    cursor.execute(f"UPDATE eaters SET attendance = ?", ("",))
    cursor.execute("SELECT * FROM eaters")
    cursor.execute("SELECT * FROM manuOnweek")
    data = cursor.fetchall()
    for i in range(len(data)):
        cursor.execute(f"UPDATE manuOnweek SET col = ? WHERE day = ? and meal = ?", (data[i][5], data[i][0], data[i][1]))
    dataBase.commit()
    dataBase.close()
    startPrib()
    print("s")

def addPurchaseRequests(who, value):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    ID = uuid.uuid4()
    cursor.execute("INSERT INTO purchaseRequests (who, value, status, ID) VALUES (?, ?, ?, ?)",
                   (who, value, "ожидание", str(ID)))
    dataBase.commit()
    dataBase.close()

def cengePurchaseRequests(ID):
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute("UPDATE purchaseRequests SET status = ? WHERE ID = ?", ("одобрено", ID))
    dataBase.commit()
    dataBase.close()

def startPrib():
    print("aaaa")
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    allFood = getData("manuOnweek")
    prib = 0
    for i in allFood:
        print(i)
        prib -= int(i[-1])*int(i[4])
    cursor.execute("UPDATE pribForWeek SET prib = ?, opl= ?", (prib, ""))
    dataBase.commit()
    dataBase.close()

def startAddAdminsAndCook():
    filePathAdmins = os.path.join('data', 'admins.txt')
    with open(filePathAdmins, 'r', encoding='utf-8') as f:
        for i in f:
            dataAdmin = i.split()
            AddCookAndAdmin(dataAdmin[0], dataAdmin[1], "admins")
    filePathCooks = os.path.join('data', 'cooks.txt')
    with open(filePathCooks, 'r', encoding='utf-8') as f:
        for i in f:
            dataCooks = i.split()
            AddCookAndAdmin(dataCooks[0], dataCooks[1], "cooks")


def Start():
    dataBase = sqlite3.connect("mydb.sql")
    cursor = dataBase.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS eaters (username TEXT, password TEXT, tel TEXT, attendance TEXT, allergens TEXT, payment TEXT, history TEXT, balans INTEGER)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS admins (username TEXT, password TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS cooks (username TEXT, password TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS manuOnweek (day TEXT, meal TEXT ,food TEXT, cost TEXT, col INTEGER, colpistart INTEGER, costForstol INTEGER)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS purchaseRequests (who TEXT, value TEXT, status TEXT, ID TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS comments (who TEXT, value TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS chtoWidano (Z INTEGER, O INTEGER)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS pribForWeek (prib INTEGER, opl TEXT)""")
    cursor.execute("SELECT * FROM chtoWidano")
    data = cursor.fetchall()
    if data == []:
        cursor.execute("INSERT INTO chtoWidano (Z, O) VALUES (?, ?)",
                       (0, 0))
    cursor.execute("SELECT * FROM pribForWeek")
    data2 = cursor.fetchall()
    if data2 == []:
        cursor.execute("INSERT INTO pribForWeek (prib, opl) VALUES (?, ?)",
                       (0, ""))
    dataBase.commit()
    dataBase.close()