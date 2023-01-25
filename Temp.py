from flask import Flask, render_template, redirect, request, session, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = "12341234"
username=""

@app.route('/')
def start():
    return render_template("start.html")

@app.route('/index')
def index():
    return render_template("index.html",username=username)

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    global username
    username=""
    #print(request.method)
    if request.method == 'POST':
        if 'username' in request.form and 'pass' in request.form:
            username = request.form['username']
            password = request.form['pass']
            mydb = mysql.connector.connect(host="localhost", user='user1', password='MySQLdba', database='db')
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM login_details WHERE username=%s AND pass=%s", (username, password))
            info = mycursor.fetchone()
            #print(info)
            mydb.close()
            if info is not None:
                if info[0] == username and info[1] == password:
                    #print("YEah")
                    session['loginsuccess'] = True
                    return redirect(url_for('index'))
            else:
                #print("yeah",username,password)
                return render_template("Login.html",info=[username,password,"No Username or Wrong Password"])

    return render_template("Login.html",info=['','',''])
@app.route('/Register', methods=['GET', 'POST'])
def Register():
    global username
    username=""
    if request.method == "POST":
        #print(request.form)
        if "username" in request.form and "email" in request.form and "pass" in request.form:
            print("hello")
            mydb = mysql.connector.connect(host="localhost", user='user1', password='MySQLdba', database='db')
            mycursor = mydb.cursor()
            username = request.form['username']
            email = request.form['email']
            password = request.form['pass']
            mycursor.execute("SELECT * FROM login_details WHERE username=%s ", (username,))
            info = mycursor.fetchone()
            if info == None:
                mycursor.execute("SELECT * FROM login_details WHERE email=%s ", (email,))
                info = mycursor.fetchone()
                #print(info, username, email, password)
            if not info:
                mycursor.execute("INSERT INTO login_details(username,pass,email) VALUES(%s,%s,%s)",(username, password, email))
                mydb.commit()
                mydb.close()
                return redirect(url_for('Login'))
            else:
                mydb.close()
                if info[0] == username:
                    return render_template("Register.html",info=[username, password, email, "Username Already Exists"])
                else:
                    return render_template("Register.html",info=[username, password, email, "G-mail Already Exists "])
    return render_template("Register.html", info=["", "", "", ""])

@app.route('/python')
def python():
    return render_template("python.html",username=username)

@app.route('/ML')
def ML():
    return render_template("ML.html",username=username)

@app.route('/DS')
def DS():
    return render_template("DS.html",username=username)

@app.route('/DL')
def DL():
    return render_template("DL.html",username=username)



if __name__=='__main__':
    app.run(debug=True)