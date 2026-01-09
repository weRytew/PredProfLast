from flask import Flask, send_file, render_template, request, jsonify, url_for, session, redirect, abort, flash, send_from_directory
import os
import sqlite3
import base
import datetime

from base import chengEters

app = Flask(__name__)
app.config["SECRET_KEY"] = "defrtyres4j43ms"
app.permanent_session_lifetime = datetime.timedelta(minutes=3)

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
                print(name)
                return jsonify({'message': 'Success!', 'nextPage': f'/profile/{session["userLogged"]}'}), 200
            else:
                session.permanent = True
                session["userLogged"] = name
                session["password"] = password
                return jsonify({'message': 'Success!', 'nextPage': f'/profile/{name}'}), 200
        elif base.findUser(name, password, "cooks"):
            if "userLogged" in session:
                return jsonify({'message': 'Success!', 'nextPage': f'/cook/{session["userLogged"]}'}), 200
            else:
                session.permanent = True
                session["userLogged"] = name
                session["password"] = password
                return jsonify({'message': 'Success!', 'nextPage': f'/cook/{name}'}), 200
        elif base.findUser(name, password, "admins"):
            if "userLogged" in session:
                return jsonify({'message': 'Success!', 'nextPage': f'/admin/{session["userLogged"]}'}), 200
            else:
                session.permanent = True
                session["userLogged"] = name
                session["password"] = password
                return jsonify({'message': 'Success!', 'nextPage': f'/admin/{name}'}), 200
        return jsonify({'message': 'error'}), 400

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == "GET":
        return render_template('Registration.html')
    elif request.method == "POST":
        name = request.form["name"]
        if not base.ChekUserCreat(name, "eaters"):
            password = request.form["password"]
            tel = request.form["tel"]
            base.AddEaters(name, password, tel)
            session.permanent = True
            session["userLogged"] = name
            session["password"] = password
            return jsonify({'message': 'Success!', 'nextPage': f'/profile/{name}'}), 200
        return jsonify({'message': 'error'}), 400

@app.route('/profile/<name>', methods=['GET', 'POST'])
def profile(name):
    if "userLogged" not in session:
        return redirect(url_for("enter"))
    elif session["userLogged"] != name:
        return redirect(url_for("enter"))
        abort(401)
    elif request.method == "GET":
        print(session["userLogged"], session["password"])
        dataUser = base.getDataEters(session["userLogged"], session["password"])
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
        payment = payment[:-1]
        data = (base.getDataEters(session["userLogged"], session["password"]))
        history = data[6]
        if history == "":
            history = ["тут пока ничего нет"]
        else:
            history = data[6][:-1].split(",")
        return render_template('UserProfile.html', payment=payment, balans=int(balans),
                               allergens=allergens,
                               comments="/comments", history=history)
    if request.method == "POST":
        print("d")

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
        data = (base.getDataEters(session["userLogged"], session["password"]))
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
                    print(i[:-1])
                    base.attendanceEters(session["userLogged"], session["password"], i[:-1])
                    base.vidat(f)
                    payment[j][2] = "получено"
                    history += f"{payment[j][0]} {payment[j][2]} {datetime.date.today()},"


    for i in range(len(paymentN)):
        paymentN[i] = (("-".join(paymentN[i])) + ",").strip()
    paymentN = " ".join(paymentN)
    base.chengEters(session["userLogged"], session["password"], "payment", paymentN)
    base.chengEters(session["userLogged"], session["password"], "history", history)
    base.chengEters(session["userLogged"], session["password"], "attendance", attendance)
    return redirect(url_for("profile", name=session["userLogged"]))

@app.route('/pay', methods=['POST'])
def pay():
    if "userLogged" not in session:
        return redirect(url_for("enter"))
    if request.method == "POST":
        dataUser = base.getDataEters(session["userLogged"], session["password"])
        a = request.form.items()
        k = []
        for i in a:
            k.append(i[0])
        payment = countThePrice(k, dataUser)
        manu = base.getData("manuOnweek")
        if type(payment) is not str and len(payment) == 1:
            flash("выбран уже купленный товар")
        elif type(payment) is not str and len(payment) == 2:
            flash("выбран товар которого нет в наличии")
        elif type(payment) is not str and len(payment) == 3:
            flash("недостаточно средств для покупки")
        return redirect(url_for("profile", name=session["userLogged"]))

def countThePrice(tochtokupili, dataUser):
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
            print(manu, "dssd")
            if ruday in j and meal in j:
                if (ruday + " " + meal) in dataUser[5]:
                    return [False]
                if int(j[4]) == 0:
                    return (False, False)
                k.append([ruday, meal])
                chena += int(j[3])
    print(manu, 1212)
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
    base.chengEters(session["userLogged"], session["password"], "balans", int(dataUser[-1]) - chena)
    base.chengEters(session["userLogged"], session["password"], "payment", dataUser[5] + payment)
    for i in k:
        base.payFood(i[0], i[1])
    return payment

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    print(base.getData("comments"), 1)
    print("sdsdsd")
    if request.method == "GET":
        comments = base.getAllComments()
        print(comments)
        return render_template('comments.html', comments=comments)
    if request.method == "POST":
        print("dfdfdfdfdfdfdf")
        if "userLogged" not in session:
            return redirect(url_for("enter"))
        print(request.form["text"])
        base.addComments(session["userLogged"], request.form["text"])
        comments = base.getAllComments()
        if comments == None:
            comments = ["тут пок нечего нет"]
        return render_template('comments.html', comments=comments)

@app.route("/addAlergens", methods=["POST"])
def addAlergens():
    if request.method == "POST":
        if "userLogged" not in session:
            return redirect(url_for("enter"))
        beforCheng = base.getDataEters(session["userLogged"], session["password"])
        allergens = beforCheng[4] + " " + request.form["alergens"]
        base.chengEters(session["userLogged"], session["password"], "allergens", allergens)
        return redirect(url_for("profile", name=session["userLogged"]))

@app.route('/getMany/', methods=['POST'])
def getMany():
    if request.method == "POST":
        print("dfdfdfdfdfdfdf")
        if "userLogged" not in session:
            return redirect(url_for("enter"))
        print(request.form["colMoney"])
        beforCheng = base.getDataEters(session["userLogged"], session["password"])
        print(beforCheng)
        allergens = beforCheng[4]
        newValue = beforCheng[-1] + int(request.form["colMoney"])
        base.chengEters(session["userLogged"], session["password"], "balans", newValue)
        return redirect(url_for("profile", name=session["userLogged"]))


@app.route('/manu/value', methods=['GET'])
def manuValue():
    if request.method == "GET":
        # print(base.getManu())
        return jsonify({'manu': base.getData("manuOnweek")}), 200

@app.route('/cook/<name>', methods=['GET'])
def cookPage(name):
    if "userLogged" not in session or session["userLogged"] != name:
        abort(401)
    if request.method == "GET":
        ZO = (base.getData("chtoWidano"))[0]
        print(ZO)
        NV = [0, 0]

        food = base.getData("manuOnweek")
        for i in food:
            NV[1] += i[5]
        NV[0] = NV[1] - ZO[0] - ZO[1]
        data = base.getData("purchaseRequests")
        return render_template('Cook.html', ZO=ZO, NV=NV, application=data)

@app.route("/purchaseRequests", methods=["POST"])
def sendPurchaseRequests():
    if "userLogged" not in session or not base.findUser(session["userLogged"], session["password"], "cooks"):
        print(base.findUser(session["userLogged"], session["password"], "cooks"))
        return redirect(url_for("enter"))
    if request.method == "POST":
        base.addPurchaseRequests(session["userLogged"], request.form["applications"])
        return redirect(url_for("cookPage", name=session["userLogged"]))

@app.route('/admin/<name>', methods=['GET'])
def adminPage(name):
    if "userLogged" not in session or session["userLogged"] != name:
        abort(401)
    if request.method == "GET":
        a = getStatistikAboutAttendense()
        p = getStatistikAboutPayment()
        AttendAndPaymant = obedAP(a, p)
        application = base.getData("purchaseRequests")
        print(base.getData("pribForWeek"), 5)
        return render_template('Admin.html', AttendAndPaymant=AttendAndPaymant, application=application)

@app.route('/gerte', methods=['POST'])
def adminWorkWithApplication():
    if "userLogged" not in session:
        abort(401)
    elif request.method == "POST":
        chekP = []
        for i in request.form.items():
            chekP.append(i[0])
        print(chekP)
        allApplication = base.getData("purchaseRequests")
        for i in range(len(allApplication)):
            if allApplication[i][-1] in chekP:
                base.cengePurchaseRequests(allApplication[i][-1])
        return redirect(url_for("adminPage", name=session["userLogged"]))

def obedAP(a, p):
    arrayWithTrans = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    # объединить два листа
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
    print(attend)
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
    print(attend)
    return attend

@app.route("/createOtchet", methods=['GET'])
def otchot():
    if "userLogged" not in session:
        abort(401)
    ZO = (base.getData("chtoWidano"))[0]
    print(ZO)
    NV = [0, 0]
    food = base.getData("manuOnweek")
    for i in food:
        NV[1] += i[5]
    NV[0] = NV[1] - ZO[0] - ZO[1]

    file_path = os.path.join('data', 'otchet.txt')

    with open(file_path, 'w', encoding='utf-8') as file:
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
    print(file)
    return send_file(
        file_path,
        as_attachment=True,
        download_name=f'report_{datetime.date.today()}.txt',
        mimetype='text'
    )

if __name__ == '__main__':
    base.Start()
    print(base.getData("comments"), 1)
    print(base.getData("eaters"), 2)
    print(base.getData("admins"), 3)
    print(base.getData("cooks"), 4)
    print(base.getData("manuOnweek"), 5)
    base.AddCookAndAdmin("fedr", "12345", "admins")
    base.AddCookAndAdmin("ivan", "2345", "cooks")
    base.AddFood("пятница", "завтрак", "1) суп\n 2) макароны\n 3) чай", "800", 10, 400)
    base.AddFood("понедельник", "завтрак", "1) каша\n 2) макароны\n 3) чай", "500", 5, 250)
    base.AddFood("вторник", "обед", "1) суп\n 2) макароны\n 3) чай", "600", 6, 300)
    base.AddFood("понедельник", "обед", "1) мясо\n 2) макароны\n 3) чай", "20000", 2, 1000)
    print(base.getData("pribForWeek"), 5)
    app.run(debug=True)

# 89321632184