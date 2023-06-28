from flask import Flask, render_template,redirect,url_for,request
import random,db

app = Flask(__name__)

@app.route('/', methods=['GET'])
def sample_top():
    msg=request.args.get('msg')
    
    if msg==None:
        return render_template('index.html')
    else:
        return render_template('index.html',msg=msg)

@app.route('/login',methods=['POST'])
def login():
    email=request.form.get('email')
    pw=request.form.get('pw')
    return render_template('top.html',email=email,pw=pw)

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register2',methods=['POST'])
def register_page2():
    email=request.form.get('email')
    pw=request.form.get('pw')
    
    count=db.insert_user(pw,email)
    
    if email=="" and pw=="" :
        error='メールアドレスとパスワードを入力して下さい。'
        return render_template('register.html',error=error)
    elif email=="":
        error='メールアドレスを入力して下さい。'
        return render_template('register.html',error=error)
    elif pw=="":
        error='パスワードを入力して下さい。'
        return render_template('register.html',error=error)
    
    if count==1:
        msg='登録が完了しました。'
        return redirect(url_for('sample_top',msg=msg))
    else:
        error='登録に失敗しました。'
        return render_template('register.html',error=error)
    
if __name__ == "__main__":
    app.run(debug=True)