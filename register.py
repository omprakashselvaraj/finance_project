from flask import Flask, render_template, request, flash
from flask_mysql_connector import MySQL
#from flask_mysqldb import MySQL
from datetime import datetime
#import re


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2410'
app.config['MYSQL_DATABASE'] = 'project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""
    print('1')
    if request.method == "POST":
        details = request.form
        username=details['username']
        password=details['password']
        print('2')
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT username,password FROM signup')
        account = cursor.fetchall()
        print(account)
        print('3')
        c=0
        d=0
        e=0
        for i in account:
            if username not in i:
                c=c+1
                print('4')
            if username in i and password in i:
                d=d+1
                print('5')
            if username in i and password not in i:
                e=e+1
                print('6')
        if c==len(account):
            msg="Don't have an account? create using the link below"
            print(msg)
            return render_template('index.html',msg=msg)
        if d==1:
            cursor.close()
            print('7')
            return 'success'
        if e!=0:
            msg="Invalid password"
            print('8')
            return render_template('login.html',msg=msg)

    


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    if request.method == "POST":
        details = request.form
        #fname = details['firstname']
        #lname = details['lastname']
        uname = details['username']
        print("1")
        mobile = details['mobile']
        DOB = (details['DOB'])
        date = datetime.strptime(DOB, '%Y-%m-%d')
        #date=DOB[6:]+"-"+DOB[3:5]+"-"+DOB[:2]
       
        email = details['email']
        password = details['password']
        print("2")
        cur = mysql.connection.cursor()
        print("3")
        cur.execute('SELECT username FROM signup')
        account = cur.fetchall()
        
        c=0
        print("4")
        for i in account:
            if uname in i:
                c=c+1
        print("5")
        if c!=0:
            msg="Account already exists !"
            print('6')
            return render_template('index.html', msg=msg)
        
        #if c>0:
         #   flash("account exists")
        else:
            print("7")
            cur.execute("INSERT INTO signup(username,mobile,dob,email,password) VALUES (%s, %s, %s, %s, %s)", (uname, mobile, date, email, password))
        
            print("8")
            mysql.connection.commit()
    
            cur.execute("SELECT * FROM signup")
            result = cur.fetchall()
            print(result)
            msg="succesfully registered"
            return render_template('login.html',msg=msg)
            cur.close()
      #  return 'success'
    #return render_template('index.html')


if __name__ == '__main__':
    app.run()