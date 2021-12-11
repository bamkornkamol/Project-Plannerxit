"""System module."""
import pymysql
from flask import Flask, render_template, request, session, flash

app = Flask(__name__)
app.secret_key = 'any random string'
conn = pymysql.connect(host='localhost', user='root', password='', db='plannerxit')


# when click in server
@app.route("/")
def main():
    print(session)
    session.clear() 
    print(session)
    return render_template('index.html')

@app.route("/home")
def home():
    return render_template('home.html', username=session['username'])

# month route
@app.route("/calendar")
def jan():
    return render_template('1jan.html')

@app.route("/mar")
def mar():
    return render_template('3mar.html')

@app.route("/apr")
def apr():
    return render_template('4apr.html')

@app.route("/may")
def may():
    return render_template('5may.html')

@app.route("/jun")
def jun():
    return render_template('6jun.html')

@app.route("/jul")
def jul():
    return render_template('7jul.html')

@app.route("/aug")
def aug():
    return render_template('8aug.html')

@app.route("/sep")
def sep():
    return render_template('9sep.html')

@app.route("/oct")
def october():
    return render_template('10oct.html')

@app.route("/nov")
def nov():
    return render_template('11nov.html')

@app.route("/dec")
def dec():
    return render_template('12dec.html')

@app.route("/feb")
def feb():
    return render_template('2feb.html')

# go to page
@app.route("/diary")
def diary():
    cur = conn.cursor()
    cur.execute('SELECT * FROM meeting')
    rows = cur.fetchall()
    return render_template('diary.html', username=session['username'], rows=rows, num=[i for i in range(1, len(rows)+1)])

@app.route("/todolist")
def todolist():
    cur = conn.cursor()
    cur.execute('SELECT * FROM todolist')
    rows = cur.fetchall()
    return render_template('todolist.html', username=session['username'], rows=rows, num=[i for i in range(1, len(rows)+1)])

# add data
@app.route("/todolist_add", methods=['POST'])
def todolist_data():
    if request.method == "POST":
        with conn.cursor() as cursor:
            title = request.form["title"]
            name = request.form["name"]
            discribe = request.form["discribe"]
            time = request.form["time"]
            print(title, name, discribe, time)
            conn.ping(reconnect=True)
            sql = "INSERT INTO `todolist` (`title`, `date_time`, `discribe`, `name_writer`) values(%s, %s, %s, %s)"
            print(sql)
            cursor.execute(sql, (title, time, discribe, name))
            conn.commit()
    conn.ping(reconnect=True)
    cur = conn.cursor()
    cur.execute('SELECT * FROM todolist')
    rows = cur.fetchall()
    return render_template('todolist.html', username=session['username'], rows=rows, num=[i for i in range(1, len(rows)+1)])

@app.route("/meeting_add", methods=['POST'])
def meeting_data():
    if request.method == "POST":
        with conn.cursor() as cursor:
            title = request.form["title"]
            name = request.form["name"]
            discribe = request.form["discribe"]
            time = request.form["time"]
            print(title, name, discribe, time)
            conn.ping(reconnect=True)
            sql = "INSERT INTO `meeting` (`title`, `date_time`, `discribe`, `header`) values(%s, %s, %s, %s)"
            print(sql)
            cursor.execute(sql, (title, time, discribe, name))
            conn.commit()
    conn.ping(reconnect=True)
    cur = conn.cursor()
    cur.execute('SELECT * FROM meeting')
    rows = cur.fetchall()
    return render_template('diary.html', username=session['username'], rows=rows, num=[i for i in range(1, len(rows)+1)])

# @app.route("/meeting_add", methods=['POST'])
# def meeting_data():
#     if request.method == "POST":
#         with conn.cursor() as cursor:
#             title = request.form["title"]
#             name = request.form["name"]
#             discribe = request.form["discribe"]
#             time = request.form["time"]
#             print(title, name, discribe, time)
#             conn.ping(reconnect=True)
#             sql = "INSERT INTO `meeting` (`title`, `date_time`, `discribe`, `header`) values(%s, %s, %s, %s)"
#             print(sql)
#             cursor.execute(sql, (title, time, discribe, name))
#     conn.ping(reconnect=True)
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM meeting')
#     rows = cur.fetchall()
#     return render_template('diary.html', username=session['username'], rows=rows, num=[i for i in range(1, len(rows)+1)])

# delete data
@app.route("/delete_meeting", methods=['POST'])
def delete_meeting():
    """delete block"""
    if request.method == "POST":
        id_data = request.form['data']
        print(id_data)
        cur = conn.cursor()
        conn.ping(reconnect=True)
        cur.execute("DELETE from meeting where id=%s", (id_data))
        conn.commit()
        cur = conn.cursor()
        cur.execute('SELECT * FROM meeting')
        rows = cur.fetchall()
    return render_template('diary.html', username=session['username'], rows=rows, num=[i for i in range(1, len(rows)+1)])

@app.route("/delete_toDoList", methods=['POST'])
def delete_todolist():
    """delete block"""
    if request.method == "POST":
        id_data = request.form['data']
        print(id_data)
        cur = conn.cursor()
        conn.ping(reconnect=True)
        cur.execute("DELETE from todolist where id=%s", (id_data))
        conn.commit()
        cur = conn.cursor()
        cur.execute('SELECT * FROM todolist')
        rows = cur.fetchall()
    return render_template('todolist.html', username=session['username'], rows=rows, num=[i for i in range(1, len(rows)+1)])

# เขียนเผื่อไว้
@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/login_data", methods=['POST'])
def userlogin():
    if (
        request.method == "POST"
        and "email" in request.form
        and "password" in request.form
    ):
        with conn.cursor() as cursor:
            email = request.form["email"]
            password = request.form["password"]
            conn.ping(reconnect=True)
            sql = "SELECT * FROM users WHERE email = %s"
            cursor.execute(sql, (email))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['email'] = account[2]
                session['password'] = account[3]
                print("login success")
                print(session)
                if(password != session['password']):
                    flash("* password is wrong")
                    return render_template('login.html')
                else:
                    return render_template("home.html", username=session['username'])
            else:
                flash("* not have a email in system")
                return render_template("login.html")
    return render_template("login.html")

@app.route("/signup_data", methods=["POST"])
def register_data():
    """register"""
    if request.method == "POST":
        with conn.cursor() as cursor:
            email = request.form["email"]
            username = request.form["username"]
            password = request.form["password"]
            cpassword = request.form["cpassword"]
            if not username:
                flash("* please enter username")
                return render_template("signup.html")
            elif not email:
                flash("* please enter e-mail")
                return render_template("signup.html")
            elif not password:
                flash("* please enter your password")
                return render_template("signup.html")
            elif not cpassword:
                flash("* please confirm your password")
                return render_template("signup.html")
            elif (password != cpassword) :
                flash("* password is not match")
                return render_template("signup.html")
            else:
                conn.ping(reconnect=True)
                sql = "SELECT email FROM users WHERE email = %s"
                cursor.execute(sql, email)
                account = cursor.fetchone()
                if(account):
                    flash('* this email is have in system')
                    return render_template("signup.html")
                else :
                    sql = "INSERT INTO `users` (`username`, `email`, `password`) values(%s, %s, %s)"
                    cursor.execute(sql, (username, email, password))
                    conn.commit()
                    return render_template("login.html")

# logout
@app.route("/logout")
def logout():
    print(session)
    session.clear() 
    print(session)
    return render_template("index.html")

# profile
@app.route("/profile")
def profile():
    """go to profile"""
    if session['loggedin']:
        return render_template('profile.html', email=session['email'], username=session['username'])
    return render_template('index.html')

@app.route("/profile_edit", methods=["POST"])
def edit_profile():
    """edit profile"""
    new_username = request.form["username"]
    if request.method == "POST":
        print(new_username)
        with conn.cursor() as cursor:
            conn.ping(reconnect=True)
            sql = "UPDATE users SET username = %s WHERE id = %s"
            cursor.execute(sql, (new_username, session['id']))
            conn.commit()
    session['username'] = new_username
    print(session['username'])
    return render_template("profile.html", email=session['email'], username=session['username'])

if __name__ == "__main__":
    app.debug = True
    app.run()
