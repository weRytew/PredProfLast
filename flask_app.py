from flask import Flask, send_file, render_template, request, jsonify, url_for, session, redirect, abort, flash
import os
import base
from flask_apscheduler import APScheduler
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "defrtyres4j43ms"
app.permanent_session_lifetime = datetime.timedelta(minutes=1440)
scheduler = APScheduler()

def NewWeek():
    base.newWeek()

scheduler.init_app(app)
scheduler.add_job(id='NewWeek', func=NewWeek, trigger='cron', day_of_week='mon', hour=0, minute=0, timezone='Europe/Moscow')
scheduler.start()


@app.route('/', methods=['GET', 'POST'])
def enter():
    if request.method == "GET":
        if "userLogged" in session and base.ChekUserCreat(session["userLogged"], "eaters"):
            return redirect(url_for("profile", name=session["userLogged"]))
        return render_template('MainEnterAndLinkToReg.html')
    elif request.method == 'POST':
        name = request.form["name"]
        password = request.form["password"]
        if base.findUser(name, password, "eaters"):
            if "userLogged" in session:
                return jsonify({'message': 'Success!', 'nextPage': f'/profile/{session["userLogged"]}'}), 200
            else:
                session.permanent = True
                session["userLogged"] = name
                return jsonify({'message': 'Success!', 'nextPage': f'/profile/{name}'}), 200
        elif base.findUser(name, password, "cooks"):
            if "userLogged" in session:
                return jsonify({'message': 'Success!', 'nextPage': f'/cook/{session["userLogged"]}'}), 200
            else:
                session.permanent = True
                session["userLogged"] = name
                return jsonify({'message': 'Success!', 'nextPage': f'/cook/{name}'}), 200
        elif base.findUser(name, password, "admins"):
            if "userLogged" in session:
                return jsonify({'message': 'Success!', 'nextPage': f'/admin/{session["userLogged"]}'}), 200
            else:
                session.permanent = True
                session["userLogged"] = name
                return jsonify({'message': 'Success!', 'nextPage': f'/admin/{name}'}), 200
        return jsonify({'message': 'error'}), 400

def GoodOrBadPassword(password, minsum):
    if len(password) < 4:
        return False
    else:
        number = 0
        uperBukv = 0
        burw = 0
        for i in password:
            if i in "- @#%$;:'*)(!+=&^":
                return False
            if i in "1234567890":
                number = 1
            if i in "AQAZWSXEDCRFVTGBYHNUJMIKLOP":
                uperBukv = 1
            if i in "qazwsxedcrfvtgbyhnujmikolp":
                burw = 1
        if burw + number + uperBukv >= minsum:
            return True

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == "GET":
        return render_template('Registration.html')
    elif request.method == "POST":
        data = request.json
        name = data["name"]
        if GoodOrBadPassword(name, 1):
            if base.ChekUserCreatForReg(name):
                password = data["password"]
                if GoodOrBadPassword(password, 2):
                    tel = data["tel"]
                    base.AddEaters(name, password, tel)
                    session.permanent = True
                    session["userLogged"] = name
                    return jsonify({'message': 'Success!', 'nextPage': f'/profile/{name}'})
                else:
                    return jsonify({'message': 'error', "error": "некорректное пароль. в пароле должны быть только английских букв и цифр"}), 400
            else:
                return jsonify({'message': 'error', "error": "этот username уже занят"})
        return jsonify({'message': 'error', "error": "некоректное имя. имя не должно содержать ничего кроме английских букв и цифр"})

def chekPay(paymant):
    p = []
    for i in paymant:
        print(i)
        if i != [""]:
            p.append(i)
    return p

@app.route('/profile/<name>', methods=['GET'])
def profile(name):
    if "userLogged" not in session:
        return redirect(url_for("enter"))
    elif session["userLogged"] != name:
        return redirect(url_for("enter"))
    elif request.method == "GET":
        dataUser = base.getDataEters(session["userLogged"])
        if dataUser == None:
            return redirect(url_for("enter"))

        balans = dataUser[7]
        allergens = dataUser[4]
        if allergens == "":
            allergens = ["тут пока ничего нет"]
        else:
            allergens = allergens.split()

        payment = dataUser[5]
        payment = payment.split(",")
        for i in range(len(payment)):
            payment[i] = payment[i].split("-")
        payment = chekPay(payment)
        nothing = ""
        if len(payment) == 0:
            nothing = "тут пока ничего нет"
        history = dataUser[6]
        if history == "":
            history = ["тут пока ничего нет"]
        else:
            history = dataUser[6][:-1].split(",")
        return render_template('UserProfile.html', payment=payment, balans=int(balans),
                               allergens=allergens,
                               comments="/comments", history=history, nothing=nothing, abonimentCost=abonementCost())

@app.route('/noteOnReceivingFood', methods=['POST'])
def getFoodPoint():
    if "userLogged" not in session:
        return redirect(url_for("enter"))
    if request.method == "POST":
        k = []
        for i in request.form.items():
            k.append(i[0])
        arrayWithIDday = ["monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        arrayWithTrans = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
        data = (base.getDataEters(session["userLogged"]))
        payment = data[5]
        payment = payment[:-1].split(",")
        for i in range(len(payment)):
            payment[i] = payment[i].split("-")

        history = data[6]
        paymentN = payment.copy()
        attendance = data[3]
        for i in k:
            for j in range(len(payment)):
                if i in payment[j]:
                    a = []
                    attendance += " " + arrayWithTrans[arrayWithIDday.index(i[:-1])]
                    ind = paymentN.index(payment[j])
                    paymentN.pop(ind)
                    f = i[-1]
                    base.attendanceEters(session["userLogged"], i[:-1])
                    base.vidat(f)
                    payment[j][2] = "получено"
                    history += f"{payment[j][0]} {payment[j][2]} {datetime.date.today()},"


    for i in range(len(paymentN)):
        paymentN[i] = (("-".join(paymentN[i])) + ",").strip()
    paymentN = " ".join(paymentN)
    base.chengEters(session["userLogged"], "payment", paymentN)
    base.chengEters(session["userLogged"], "history", history)
    base.chengEters(session["userLogged"], "attendance", attendance)
    return redirect(url_for("profile", name=session["userLogged"]))

@app.route('/pay', methods=['POST'])
def pay():
    if "userLogged" not in session:
        return redirect(url_for("enter"))
    if request.method == "POST":
        dataUser = base.getDataEters(session["userLogged"])
        a = request.form.items()
        k = []
        for i in a:
            k.append(i[0])
        payment = countThePrice(k, dataUser, 1)
        manu = base.getData("manuOnweek")
        if type(payment) is not str and len(payment) == 1:
            flash("выбран уже купленный товар")
        elif type(payment) is not str and len(payment) == 2:
            flash("выбран товар которого нет в наличии")
        elif type(payment) is not str and len(payment) == 3:
            flash("недостаточно средств для покупки")
        return redirect(url_for("profile", name=session["userLogged"]))

def countThePrice(tochtokupili, dataUser, modify):
    arrayWithIDday = ["monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    arrayWithTrans = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    manu = base.getData("manuOnweek")
    chena = 0
    k = []
    for i in tochtokupili:
        meal = "обед"
        ruday = arrayWithTrans[arrayWithIDday.index(i[:len(i)-1])]
        if i[-1] == "Z":
            meal = "завтрак"
        elif i[-1] == "O":
            meal = "обед"
        for j in manu:
            if ruday in j and meal in j:
                if (ruday + " " + meal) in dataUser[5]:
                    return [False]
                if int(j[4]) == 0:
                    return (False, False)
                k.append([ruday, meal])
                chena += int(j[3])
    chena = chena * modify
    payment = ""
    status = "не получено"
    if int(dataUser[-1]) - chena < 0:
        return (False, False, False)
    for i in k:
        meal = i[1]
        bukva = "Z"
        if meal == "завтрак":
            bukva = "Z"
        if meal == "обед":
            bukva = "O"
        ruday = i[0]
        ind = arrayWithIDday[arrayWithTrans.index(ruday)]
        for j in manu:
            if ruday in j and meal in j:
                payment = payment + ruday + " " + meal + "-" + ind + bukva + "-" + status + ","
    base.chengEters(session["userLogged"], "balans", int(dataUser[-1]) - chena)
    base.chengEters(session["userLogged"], "payment", dataUser[5] + payment)
    for i in k:
        base.payFood(i[0], i[1])
    return payment

@app.route('/payaboniment', methods=['POST'])
def payAboniment():
    if "userLogged" not in session:
        return redirect(url_for("enter"))
    if request.method == "POST":
        dataUser = base.getDataEters(session["userLogged"])
        arrayWithIDday = ["monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        arrayWithTrans = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
        manu = base.getData("manuOnweek")
        k = []
        for i in manu:
            day = arrayWithIDday[arrayWithTrans.index(i[0])]
            if i[1] == "завтрак":
                mil = "Z"
            elif i[1] == "обед":
                mil = "O"
            k.append(day + mil)

        payment = countThePrice(k, dataUser, 0.9)
        manu = base.getData("manuOnweek")
        if type(payment) is not str and len(payment) == 1:
            flash("выбран уже купленный товар")
        elif type(payment) is not str and len(payment) == 2:
            flash("в наличии нет товара который входит в абонимент")
        elif type(payment) is not str and len(payment) == 3:
            flash("недостаточно средств для покупки")
        return redirect(url_for("profile", name=session["userLogged"]))

def abonementCost():
    manu = base.getData("manuOnweek")
    cost = 0
    for i in manu:
        cost += int(i[3])
    return int(cost * 0.9 + 1)

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == "GET":
        comments = base.getAllComments()
        return render_template('comments.html', comments=comments)
    if request.method == "POST":
        if "userLogged" not in session:
            return redirect(url_for("enter"))
        base.addComments(session["userLogged"], request.form["text"])
        comments = base.getAllComments()
        if comments == None:
            comments = ["тут пок нечего нет"]
        return redirect(url_for('comments'))

@app.route("/addAlergens", methods=["POST"])
def addAlergens():
    if request.method == "POST":
        if "userLogged" not in session:
            return redirect(url_for("enter"))
        beforCheng = base.getDataEters(session["userLogged"])
        allergens = beforCheng[4] + " " + request.form["alergens"]
        base.chengEters(session["userLogged"], "allergens", allergens)
        return redirect(url_for("profile", name=session["userLogged"]))

@app.route('/getMany/', methods=['POST'])
def getMany():
    if request.method == "POST":
        if "userLogged" not in session:
            return redirect(url_for("enter"))
        else:
            plasMany = 0
            try:
                plasMany = int(request.form["colMoney"])
            except:
                flash("введино не число")
                return redirect(url_for("profile", name=session["userLogged"]))
            if plasMany < 0:
                flash("введите положительное число")
                return redirect(url_for("profile", name=session["userLogged"]))
            beforCheng = base.getDataEters(session["userLogged"])
            newValue = beforCheng[-1] + plasMany
            base.chengEters(session["userLogged"], "balans", newValue)
            return redirect(url_for("profile", name=session["userLogged"]))


@app.route('/manu/value', methods=['GET'])
def manuValue():
    if request.method == "GET":
        return jsonify({'manu': base.getData("manuOnweek")}), 200

@app.route('/cook/<name>', methods=['GET'])
def cookPage(name):
    if "userLogged" not in session or session["userLogged"] != name:
        return redirect(url_for("enter"))
    if request.method == "GET":
        ZO = (base.getData("chtoWidano"))[0]
        NV = [0, 0]

        food = base.getData("manuOnweek")
        for i in food:
            NV[1] += i[5]
        NV[0] = NV[1] - ZO[0] - ZO[1]
        data = base.getData("purchaseRequests")
        return render_template('Cook.html', ZO=ZO, NV=NV, application=data)

@app.route("/purchaseRequests", methods=["POST"])
def sendPurchaseRequests():
    if "userLogged" not in session or not base.findUserCook(session["userLogged"]):
        return redirect(url_for("enter"))
    if request.method == "POST":
        base.addPurchaseRequests(session["userLogged"], request.form["applications"])
        return redirect(url_for("cookPage", name=session["userLogged"]))

def chekthatAllOk(listChengeManu):
    arrayWithIDday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    arrayWithTrans = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    for i in listChengeManu:
        if listChengeManu[i]["ZorO"] == "Nothing":
            if listChengeManu[i]["ZorOD"] == False:
                if listChengeManu[i][i + "Meal"] == "":
                    if listChengeManu[i][i + "Col"] == "" or listChengeManu[i]["MondayCol"] == 0:
                        if listChengeManu[i][i + "FirstCost"] == "" or listChengeManu[i]["MondayFirstCost"] == 0:
                            if listChengeManu[i][i + "Cost"] == "" or listChengeManu[i]["MondayCost"] == 0:
                                continue
        if (listChengeManu[i]["ZorO"] == "O" or listChengeManu[i]["ZorO"] == "Z") and listChengeManu[i]["ZorOD"]:
            continue
        if i not in arrayWithIDday:
            return False, "такого дня не существует"
        try:
            if int(listChengeManu[i][i + "Col"]) < 0:
                return False, "количество товара не может быть меньше 0"
            fc = int(listChengeManu[i][i + "FirstCost"])
            c = int(listChengeManu[i][i + "Cost"])
            if fc < 0 or c < 0:
                return False, "цены должны быть положительными числами"
            if c < fc:
                return False, "себе стоимось не должна быть выше цены продажи(руководство такое не одобрит)"
        except:
            return False, "цены должны быть числами"

        if listChengeManu[i]["ZorOD"] and listChengeManu[i]["ZorO"] != "Nothing":
            return False, "для удаления выбери завтрак или обед"
        if (listChengeManu[i]["ZorO"] != "Z" or listChengeManu[i]["ZorO"] != "O") and not listChengeManu[i]["ZorOD"]:
            if (listChengeManu[i][i + "Meal"] == "" or listChengeManu[i][i + "FirstCost"] == "" or listChengeManu[i][i + "Cost"] == "" or listChengeManu[i][i + "Col"] == "") and listChengeManu[i]["ZorOD"] == False:
                return False, "для добавления заполните все поля"
            if (listChengeManu[i][i + "Meal"] != "" or listChengeManu[i][i + "FirstCost"] != "" or listChengeManu[i][i + "Cost"] != "" or listChengeManu[i][i + "Col"] != "") and listChengeManu[i]["ZorOD"] == False and listChengeManu[i]["ZorO"] == "Nothing":
                return False, "для добавления заполните все поля"
    return True, "ok"



@app.route("/addFood1", methods=["POST"])
def addFood():
    if "userLogged" not in session or not base.findUserCook(session["userLogged"]):
        return redirect(url_for("enter"))
    if request.method == "POST":
        data = request.json
        rez = chekthatAllOk(data)
        print(rez)
        if rez[0]:
            arrayWithIDday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            arrayWithTrans = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
            try:
                for i in data:
                    if data[i]["ZorO"] == "Nothing":
                        continue
                    else:
                        day = arrayWithTrans[arrayWithIDday.index(i)]
                        food = data[i][i + "Meal"]
                        col = data[i][i + "Col"]
                        firsCost = data[i][i + "FirstCost"]
                        cost = data[i][i + "Cost"]
                        if data[i]["ZorO"] == "Z":
                            if data[i]["ZorOD"]:
                                base.delFood(day, "завтрак")
                            else:
                                base.AddFood(day, "завтрак", food, cost, col, firsCost)
                        elif data[i]["ZorO"] == "O":
                            if data[i]["ZorOD"]:
                                base.delFood(day, "обед")
                            else:
                                base.AddFood(day, "обед", food, cost, col, firsCost)
                return redirect(url_for("cookPage", name=session["userLogged"]))
            except:
                return jsonify({'message': 'error', "error": "что-то пошло не так"})
        else:
            return jsonify({'message': 'error', "error": rez[1]})

@app.route('/admin/<name>', methods=['GET'])
def adminPage(name):
    if "userLogged" not in session or session["userLogged"] != name:
        return redirect(url_for("enter"))
    if request.method == "GET":
        a = getStatistikAboutAttendense()
        p = getStatistikAboutPayment()
        AttendAndPaymant = obedAP(a, p)
        application = base.getData("purchaseRequests")
        return render_template('Admin.html', AttendAndPaymant=AttendAndPaymant, application=application)

@app.route('/gerte', methods=['POST'])
def adminWorkWithApplication():
    if "userLogged" not in session:
        return redirect(url_for("enter"))
    elif request.method == "POST":
        chekP = []
        for i in request.form.items():
            chekP.append(i[0])
        allApplication = base.getData("purchaseRequests")
        for i in range(len(allApplication)):
            if allApplication[i][-1] in chekP:
                base.cengePurchaseRequests(allApplication[i][-1])
        return redirect(url_for("adminPage", name=session["userLogged"]))

def obedAP(a, p):
    arrayWithTrans = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    aAndPList = []
    for i in arrayWithTrans:
        k = [i, 0, 0]
        if i in a:
            k[1] = a[i]
        if i in p:
            k[2] = p[i]
        aAndPList.append(k)
    return aAndPList

def getStatistikAboutAttendense():
    dataEaters = base.getAllEaters()
    attend = {}
    for i in dataEaters:
        at = i[3].split()
        s = ""
        for j in at:
            if j not in attend and j not in s:
                s += " " + j
                attend[j] = 1
            elif j in attend and j not in s:
                s += " " + j
                f = attend[j]
                attend[j] = f + 1
    return attend

def getStatistikAboutPayment():
    dataEaters = (base.getData("pribForWeek")[0][1]).split()
    attend = {}
    for i in dataEaters:
        if i not in attend:
            attend[i] = 1
        elif i in attend:
            s = attend[i]
            attend[i] = s + 1
    return attend

@app.route("/createOtchet", methods=['GET'])
def otchot():
    if "userLogged" not in session:
        return redirect(url_for("enter"))
    ZO = (base.getData("chtoWidano"))[0]
    print(ZO)
    NV = [0, 0]
    food = base.getData("manuOnweek")
    print(food)
    for i in food:
        NV[1] += i[5]
    NV[0] = NV[1] - ZO[0] - ZO[1]
    print(NV)

    filePath = os.path.join('data', 'otchet.txt')
    base.startPrib()
    with open(filePath, 'w', encoding='utf-8') as file:
        file.write(f"количество выданных завтраков: {ZO[0]}\n")
        file.write(f"количество выданных обедов: {ZO[1]}\n")
        file.write(f"количество не выданных завтраков и обедов: {NV[0]}\n")
        file.write(f"всего завтраков и обедов приготовлено: {NV[1]}\n\n")
        file.write(f"статистика оплат и посещаемости\n")
        a = getStatistikAboutAttendense()
        p = getStatistikAboutPayment()
        AttendAndPaymant = obedAP(a, p)
        for i in AttendAndPaymant:
            file.write(f"{i[0]}: посещаемость: {i[1]} оплаты: {i[2]}\n")
        pr = base.getData("pribForWeek")[0][0]
        file.write(f"прибыль за неделю на {datetime.date.today()} = {pr} \n")
    return send_file(filePath, as_attachment=True, download_name=f'report_{datetime.date.today()}.txt', mimetype='text')

def whatDoInStart():
    base.Start()
    base.startAddAdminsAndCook()
    base.newWeek()

if __name__ == '__main__':
    whatDoInStart()

    app.run(host='0.0.0.0')
