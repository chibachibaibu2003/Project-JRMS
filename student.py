from flask import Flask,Blueprint, render_template,redirect,url_for,request,session
import random,string,db

student_bp=Blueprint('student',__name__,url_prefix='/student')

student_bp.secret_key=''.join(random.choices(string.ascii_letters,k=256))

@student_bp.route('/', methods=['GET'])
def sample_top():
    msg=request.args.get('msg')
    
    if msg==None:
        return render_template('index.html')
    else:
        return render_template('index.html',msg=msg)

@student_bp.route('/menu')
def menu():
    if 'user' in session:
        return render_template('student/top.html')
    else:
        return redirect(url_for('sample_top'))
    
@student_bp.route('/register')
def register():
    if 'user' in session:
        return render_template('student/register.html')
    else:
        return redirect(url_for('sample_top'))
    
@student_bp.route('/confirm',methods=['POST'])
def register_confirm():
    if 'user' in session:
        name=request.form.get('name')
        course=request.form.get('course')
        comapany_name=request.form.get('company_name')
        comapany_tel=request.form.get('company_tel')
        location=request.form.get('company_location')
        occupation=request.form.get('occupation')
        industory=request.form.get('industory')
        application=request.form.get('application')
        date_1=request.form.get('date_1')
        test_1=request.form.get('test_1')
        interview_1=request.form.get('interview_1')
        date_2=request.form.get('date_2')
        test_2=request.form.get('test_2')
        interview_2=request.form.get('interview_2')
        date_3=request.form.get('date_3')
        test_3=request.form.get('test_3')
        interview_3=request.form.get('interview_3')
        date_4=request.form.get('date_4')
        test_4=request.form.get('test_4')
        interview_4=request.form.get('interview_4')
        report_test_1=request.form.get('report_test_1')
        report_test_2=request.form.get('report_test_2')
        report_test_3=request.form.get('report_test_3')
        report_test_4=request.form.get('report_test_4')
        report_test_5=request.form.get('report_test_5')
        report_test_6=request.form.get('report_test_6')
        report_test_7=request.form.get('report_test_7')
        report_test_8=request.form.get('report_test_8')
        report_test_9=request.form.get('report_test_9')
        report_test_10=request.form.get('report_test_10')
        report_test_11=request.form.get('report_test_11')
        if name ==''or course==''or comapany_name==''or comapany_tel==''or location==''or occupation==''or industory==''or application==''or date_1=='' or report_test_1=='':
            error='全ての必須項目にデータを入力して下さい'
            input_date={'name':name,'course':course,'company_name':comapany_name,'company_tel':comapany_tel,'location':location,'occupation':occupation,'industory':industory,'application':application,'date_1':date_1,'date_2':date_2,'date_3':date_3,'date_4':date_4,'test_1':test_1,'test_2':test_2,'test_3':test_3,'test_4':test_4,'interview_1':interview_1,'interview_2':interview_2,'interview_3':interview_3,'interview_4':interview_4,'report_test_1':report_test_1,'report_test_2':report_test_2,'report_test_3':report_test_3,'report_test_4':report_test_4,'report_test_5':report_test_5,'report_test_6':report_test_6,'report_test_7':report_test_7,'report_test_8':report_test_8,'report_test_9':report_test_9,'report_test_10':report_test_10,'report_test_11':report_test_11}
            return render_template('student/register.html',error=error,data=input_date)
        else:
            input_date={'name':name,'course':course,'company_name':comapany_name,'company_tel':comapany_tel,'location':location,'occupation':occupation,'industory':industory,'application':application,'date_1':date_1,'date_2':date_2,'date_3':date_3,'date_4':date_4,'test_1':test_1,'test_2':test_2,'test_3':test_3,'test_4':test_4,'interview_1':interview_1,'interview_2':interview_2,'interview_3':interview_3,'interview_4':interview_4,'report_test_1':report_test_1,'report_test_2':report_test_2,'report_test_3':report_test_3,'report_test_4':report_test_4,'report_test_5':report_test_5,'report_test_6':report_test_6,'report_test_7':report_test_7,'report_test_8':report_test_8,'report_test_9':report_test_9,'report_test_10':report_test_10,'report_test_11':report_test_11}
            return render_template('student/register.html')
    else:
        return redirect(url_for('sample_top'))
    
@student_bp.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('sample_top'))
