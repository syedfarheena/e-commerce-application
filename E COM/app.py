from flask import Flask,render_template,request
import random
from pymysql import connect
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import razorpay


razorpay_key_id = "rzp_test_Yd8n5O3NVPZ3Cs"
razorpay_key_secret = "tse0IBIiiJjyf3ZWahrGIpac"
client = razorpay.Client(auth=(razorpay_key_id,razorpay_key_secret))

verifyotp ="0"


db_config = {
    'host' : 'localhost',
    'database' : 'royalshop',
    'user' : 'root',
    'password' : '984984'
}

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("home.html")

@app.route("/contactus")
def contactus():
    return render_template("contactus.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/registerdata",methods=["POST","GET"])
def registerdata():
    if request.method == "POST":
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        cpassword = request.form['confirm-password']
        if password == cpassword:
            otp = random.randint(111111,999999)
            global verifyotp
            verifyotp = str(otp)
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "syedfarheena16062003@gmail.com"  
            sender_password = "ykqn ijrh bjfk ddwn"
            from_email = "syedfarheena16062003@gmail.com" 
            to_email = email
            subject = "otp for verification"
            body = f"The otp for login is {verifyotp}"


            message = MIMEMultipart()
            message["From"] = from_email
            message["To"] = to_email
            message["Subject"] = subject
            message.attach(MIMEText(body,'plain'))

            server= smtplib.SMTP(smtp_server, smtp_port)
            server.starttls() 
            server.login(sender_email, sender_password)
            server.send_message(message)
            server.quit()
            return render_template("verifyemail.html",name=name,username=username,email=email,mobile=mobile,password=password)
        else:
            return "Make sure password and confirm password to be same"
    else:
        return "<h3 style='color:red'>Data got in wrong manner</h3>"
    

@app.route("/verifyemail",methods=["POST","GET"])
def verifyemail():
    if request.method =="POST":
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        otp = request.form['otp']
        if otp==verifyotp:
            try:
                conn = connect(**db_config)
                cursor = conn.cursor()
                q = "INSERT INTO USERS VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(q,(name,username,email,mobile,password))
                conn.commit()
            except:
                return "Error Occured while storing data in database or Username alreary exists"
            else:
                return render_template("login.html")
        else:
            return "Wrong otp"
    else:
        return "<h3 style='color:red'>Data got in wrong manner</h3>"

@app.route("/userlogin",methods = ["POST","GET"])
def userlogin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        try:
            conn = connect(**db_config)
            cursor = conn.cursor()
            q = "SELECT * FROM USERS WHERE USERNAME = (%s)"
            cursor.execute(q,(username))
            row = cursor.fetchone()
            if row == None:
                return "User Does not Exists, Create account first !"
            else:
                if row[4] != password:
                    return "Incorrect Password !"
                else:
                    return render_template("userhome.html",name=username)
        except:
            return "Error Occured while retriving the data"

    else:
        return "Data Occured in incorrect way"

@app.route("/add_to_cart",methods = ["POST","GET"])
def add_to_cart():
    if request.method == "POST":
        username = request.form['username']
        productname = request.form['productname']
        quantity = request.form['quantity']
        price = request.form['price']
        totalprice = int(quantity) * int(price)
        totalprice = str(totalprice)
        try:
            conn = connect(**db_config)
            cursor = conn.cursor()
            q = "INSERT INTO CART VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(q,(username,productname,quantity,price,totalprice))
            conn.commit()
        except:
            return " Error Occured while storing data into data base"
        else:
           return render_template("userhome.html",name=username)

    else:
        return "Data occured in incorrect way"
    
@app.route("/cartpage",methods = ["GET"])
def cartpage():
    username = request.args.get('username')
    try:
        conn = connect(**db_config)
        cursor = conn.cursor()
        q = "SELECT * FROM CART WHERE USERNAME = (%s)"
        cursor.execute(q,(username))
        row = cursor.fetchall()
        subtotal = 0
        for i in row:
            subtotal = subtotal +int(i[4])
        result = subtotal * 100
        order = client.order.create({
            'amount' : result,
            'currency' : 'INR',
            'payment_capture' : '1'
        })   
    except:
        return "Error occured while Retreving the data"
    else:
        return render_template("cart.html",data=row,grandtotal=subtotal,order=order)


@app.route("/sucess",methods = ["POST","GET"])
def sucess():
    payment_id = request.form.get("razorpay_payment_id")
    order_id = request.form.get("razorpay_order_id")
    signature = request.form.get("razorpay_signature")
    dict1 = {
        'razorpay_order_id' : order_id,
        'razorpay_payment_id' : payment_id,
        'razorpay_signature' : signature
    }
    try:
        client.utility.verify_payment_signature(dict1)
        return render_template("success.html")
    except:
        return render_template("failed.html")


if __name__ == "__main__":
    app.run(port=5003)