from flask import Flask
import pymysql
app = Flask(__name__)

db_config = {
    'host' : 'localhost',
    'database' : 'flask',
    'user' : 'root',
    'password' : '984984'
}

@app.route("/senddata")
def senddata():
if __name__=="__main__":
    app.run(port=5002)
'''
app = Flask(__name__)

@app.route("/")
def landing():
    return "This is my second flask application"
@app.route("/aboutus")
def aboutus():
    return "About us Page"
@app.route("/contactus")
def contactus():
    return "<h1 style='color:red'> +91 9856774378 </h1>"
@app.route("/response/<name>")
def response(name):
    print("Hello" + name)
    return f"Hello (name)"
if __name__ == "__main__":
    app.run()
    '''