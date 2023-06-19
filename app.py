from flask import Flask, render_template,redirect,url_for,request
import random

app = Flask(__name__)

@app.route('/')
def sample_top():
    return render_template('index.html')

@app.route('/login',methods=['POST'])
def login():
    email=request.form.get('email')
    pw=request.form.get('pw')
    return render_template('top.html',email=email,pw=pw)

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register2',methods=['POST'])
def register_mail_page():
    emali=request.form.get('email')
    return render_template('register_mail.html',email=emali)

if __name__ == "__main__":
    app.run(debug=True)