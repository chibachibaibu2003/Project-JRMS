from flask import Flask, render_template,redirect,url_for,request,session
from admin import admin_bp
from student import student_bp
import random,string,db

app = Flask(__name__)
app.secret_key=''.join(random.choices(string.ascii_letters,k=256))

app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)

@app.route('/', methods=['GET'])
def sample_top():
    msg=request.args.get('msg')
    if 'user' in session:
        session.pop('user',None)
    if msg==None:
        return render_template('index.html')
    else:
        return render_template('index.html',msg=msg)

@app.route('/',methods=['POST'])
def login():
    email=request.form.get('email')
    pw=request.form.get('pw')
    
    if email=="" and pw=="" :
        error='メールアドレスとパスワードを入力して下さい。'
        return render_template('index.html',error=error)
    elif email=="":
        error='メールアドレスを入力して下さい。'
        return render_template('index.html',error=error)
    elif pw=="":
        error='パスワードを入力して下さい。'
        input_data={'email':email,'password':pw}
        return render_template('index.html',error=error,data=input_data)
    
    if db.login(email,pw)[0]:
        session['user']=True
        lank=db.login(email,pw)[1]
        id=db.login(email,pw)[2]
        if lank==0:
            session['user_id']=id
            return redirect(url_for('mypage'))
        else:
            return redirect(url_for('admin_top'))
    else:
        error='ユーザー名またはパスワードが違います。'
        
        input_data={'email':email,'password':pw}
        return render_template('index.html',error=error,data=input_data)

@app.route('/mypage')
def mypage():
    if 'user' in session:
        return render_template('student/top.html')
    else :
        return redirect(url_for('sample_top'))
    
@app.route('/admin_top')
def admin_top():
    if 'user' in session:
        return render_template('admin/top.html')
    else:
        return redirect(url_for('sample_top'))

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register2',methods=['POST'])
def register_page2():
    email=request.form.get('email')
    pw=request.form.get('pw')
    
    if email=="" and pw=="" :
        error='メールアドレスとパスワードを入力して下さい。'
        return render_template('register.html',error=error)
    elif email=="":
        error='メールアドレスを入力して下さい。'
        return render_template('register.html',error=error)
    elif pw=="":
        error='パスワードを入力して下さい。'
        return render_template('register.html',error=error)
    
    count=db.insert_user(pw,email)
    
    if count==1:
        msg='登録が完了しました。'
        return redirect(url_for('sample_top',msg=msg))
    else:
        error='登録に失敗しました。'
        return render_template('register.html',error=error)
    
    
if __name__ == "__main__":
    app.run(debug=True)