from flask import Flask, render_template, request, flash,session
from flask_mysql_connector import MySQL
#from flask_mysqldb import MySQL
from datetime import datetime
import numpy as np
#global user

app = Flask(__name__)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2410'
app.config['MYSQL_DATABASE'] = 'project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('username', None)
   return render_template('login.html')
  



@app.route('/expense',methods=['GET','POST'])
def expense():
    if request.method=="POST":
        diff=[]
        detail=request.form
        income=int(detail['income'])
        cb=int(detail['cb'])
        ce=int(detail['ce'])
        mb=int(detail['mb'])
        me=int(detail['me'])
        hb=int(detail['hb'])
        he=int(detail['he'])
        fb=int(detail['fb'])
        fe=int(detail['fe'])
        tb=int(detail['tb'])
        te=int(detail['te'])
        eb=int(detail['eb'])
        ee=int(detail['ee'])
        tab=int(detail['tab'])
        tae=int(detail['tae'])
        emb=int(detail['emb'])
        eme=int(detail['eme'])
        ob=int(detail['ob'])
        oe=int(detail['oe'])
        ben=np.array([cb,mb,hb,fb,tb,eb,tab,emb,ob])
        exp=np.array([ce,me,he,fe,te,ee,tae,eme,oe])
        diff=ben-exp
        #print(ben,exp,diff)
        saving=income-sum(exp)
        sp=(saving/income)*100
        diff=list(diff)
        diff.append(saving)
        diff.append(sp)
        #print(saving)
        return render_template('expense.html',diff=diff)


@app.route('/calculate',methods=['GET','POST'])
def calculate():
    print('0')
    if request.method=="POST":
        detail=request.form
        print('1')
        salary=int(detail['salary'])
        print('2')
        saving=int(detail['savings'])
        print('3')
        years=int(detail['year'])
        print('4')
        print(salary,saving,years)
        return "success"

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        #query='select * from signup where username=%s'
        #data=session['username']
        cursor=mysql.connection.cursor()
        cursor.execute('select * from signup where username=%s',(session['username'],))
        account = cursor.fetchone()
        print(account)
        print(account[0],account[1])
        cursor.close()
        return render_template('profiledisp.html',account=account)   

@app.route('/forgot',methods=['GET','POST'])
def forget():
    c=0
    msg=""
    if request.method == "POST":
        details=request.form
        uname=details['username']
        mobile=details['mobile']
        password=details['password']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT username,mobile FROM signup')
        account = cursor.fetchall()
        print(account)
        query="update signup set password=%s where username=%s"
        data=(password,uname)
        for i in account :
            if uname in i and mobile in i:
                c=c+1
        if c==1:
            cursor.execute(query,data)
            mysql.connection.commit()
            msg="PASSWORD SUCCESSFULLY UPDATED!!!"
            return render_template('login.html',msg=msg)
        else:
            msg="NO ACCOUNT EXIST WITH THE GIVEN USERNAME AND DOB"
            return render_template('index.html',msg=msg)
        cursor.close()

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
            session['loggedin']=True
            session['username']=username
            return render_template('main.html')
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