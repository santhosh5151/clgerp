from flask import *
import pymysql

app = Flask(__name__)

mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="santhosh"
)
cursor = mydb.cursor()

is_login=False
userId = ""
rollNumber = ""
userRoll = ""
@app.route("/",methods=['GET', 'POST'])
def login():
    error = " "
    if request.method == "POST":
        roll = request.form['username']
        cursor.execute("SELECT * FROM users WHERE Roll_Number = %s",(roll))
        data =  cursor.fetchone()
        
        if data == None:
            error =  "Invalid User"
        else:
            global is_login
            global userId
            global rollNumber
            global userRole

            is_login=True
            userId = data[0]
            rollNumber = data[2]
            userRole = data[6]

            return redirect("dashboard")

    return render_template("clgk.html",data=error)
#@app.route("/login")
#def login2():
    #return render_template("clgk.html")
@app.route("/dashboard")
def dashboardPage():
    if is_login:
        return render_template("erp2.html")
    else:
        redirect("/")

@app.route("/register", methods=["GET","POST"])
def reg():
    msg=""
    if request.method =="POST":
        username=request.form["username"]                                                           
        Roll=request.form["rollno"]
        email=request.form[ "Email"]
        password=request.form[ "Password"]

        try:
            cursor.execute("INSERT INTO users SET Username=%s,Roll_Number=%s,Email=%s,Password=%s",(username,Roll,email,password))
            mydb.commit()
            msg=1
        except:
            msg=0
    return render_template("index6.html" , msg=msg)

@app.route("/users")
def usersList():
    cursor.execute( "SELECT * FROM users ")

    data = cursor.fetchall()
    return render_template("users.html", users=data )

@app.route("/myInfo")
def details():
    if is_login:
        cursor.execute("SELECT * FROM users WHERE Roll_Number = %s" ,(rollNumber,))
        userData = cursor.fetchone()
        return render_template("information.html",users = userData)
    else:
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
