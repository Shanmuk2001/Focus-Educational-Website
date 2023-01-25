from flask import Flask, render_template, redirect, request, session, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = "12341234"

@app.route('/',methods=['GET', 'POST'])
def start():
    global username
    username = ""
    if request.method == "POST":
        if "username" in request.form and "email" in request.form and "pass" in request.form:
            mydb = mysql.connector.connect(host="localhost", user='user1', password='MySQLdba', database='db')
            mycursor = mydb.cursor()
            username = request.form['username']
            email = request.form['email']
            password = request.form['pass']
            print(username, email, password)
            mycursor.execute("SELECT * FROM login_details WHERE username=%s ", (username,))
            info = mycursor.fetchone()
            if info == None:
                mycursor.execute("SELECT * FROM login_details WHERE email=%s ", (email,))
                info = mycursor.fetchone()
            print(info, username, email, password)
            if not info:
                mycursor.execute("INSERT INTO login_details(username,pass,email) VALUES(%s,%s,%s)",(username, password, email))
                mydb.commit()
                mydb.close()
                return render_template("csshtml.html",info=["", "", "", "Registered Successfully"])
            else:
                mydb.close()
                if info[0] == username:
                    return render_template("csshtml.html",info=[username, password, email, "Username Already Exists"])
                else:
                    return render_template("csshtml.html",info=[username, password, email, "G-mail Already Exists "])
    return render_template("csshtml.html", info=["", "", "", ""])

if __name__=='__main__':
    app.run(debug=True)