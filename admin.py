from flask import Flask,Blueprint, render_template,redirect,url_for,request,session
import random,string,db

admin_bp=Blueprint('admin',__name__,url_prefix='/admin')

admin_bp.secret_key=''.join(random.choices(string.ascii_letters,k=256))

@admin_bp.route('/', methods=['GET'])
def sample_top():
    msg=request.args.get('msg')
    
    if msg==None:
        return render_template('index.html')
    else:
        return render_template('index.html',msg=msg)

@admin_bp.route('/menu')
def menu():
    if 'user' in session:
        return render_template('top.html')
    else:
        return redirect(url_for('sample_top'))    