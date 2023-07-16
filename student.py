from flask import Flask,Blueprint, render_template,redirect,url_for,request,session
import random,string,shutil,pythoncom,os,db
import win32com.client
import openpyxl

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
    if 'input' in session:
        session.pop('user', None) 
    if 'user' in session:
        name=request.form.get('name')
        course=request.form.get('course')
        student_num=request.form.get('student_num')
        comapany_name=request.form.get('company_name')
        comapany_furigana=request.form.get('company_furigana')
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
            input_date={'name':name,'course':course,'student_num':student_num,'company_name':comapany_name,'company_furigana':comapany_furigana,'company_tel':comapany_tel,'location':location,'occupation':occupation,'industory':industory,'application':application,'date_1':date_1,'date_2':date_2,'date_3':date_3,'date_4':date_4,'test_1':test_1,'test_2':test_2,'test_3':test_3,'test_4':test_4,'interview_1':interview_1,'interview_2':interview_2,'interview_3':interview_3,'interview_4':interview_4,'report_test_1':report_test_1,'report_test_2':report_test_2,'report_test_3':report_test_3,'report_test_4':report_test_4,'report_test_5':report_test_5,'report_test_6':report_test_6,'report_test_7':report_test_7,'report_test_8':report_test_8,'report_test_9':report_test_9,'report_test_10':report_test_10,'report_test_11':report_test_11}
            return render_template('student/register.html',error=error,data=input_date)
        else:
            input_date={'name':name,'course':course,'student_num':student_num,'company_name':comapany_name,'company_furigana':comapany_furigana,'company_tel':comapany_tel,'location':location,'occupation':occupation,'industory':industory,'application':application,'date_1':date_1,'date_2':date_2,'date_3':date_3,'date_4':date_4,'test_1':test_1,'test_2':test_2,'test_3':test_3,'test_4':test_4,'interview_1':interview_1,'interview_2':interview_2,'interview_3':interview_3,'interview_4':interview_4,'report_test_1':report_test_1,'report_test_2':report_test_2,'report_test_3':report_test_3,'report_test_4':report_test_4,'report_test_5':report_test_5,'report_test_6':report_test_6,'report_test_7':report_test_7,'report_test_8':report_test_8,'report_test_9':report_test_9,'report_test_10':report_test_10,'report_test_11':report_test_11}
            session['input']=input_date
            return redirect(url_for('student.register_confirm_2'))
    else:
        return redirect(url_for('sample_top'))

@student_bp.route('/confirm_2')
def register_confirm_2():
    input=session['input']
    shutil.copy('./Project-JRMS/static/excel/Excelサンプル.xlsx','./Project-JRMS/static/excel/report_excel.xlsx')
    wb = openpyxl.load_workbook('./Project-JRMS/static/excel/report_excel.xlsx')
    sheet = wb['サンプル']
    sheet['f12'].value=input['name']
    wb.save('./Project-JRMS/static/excel/report_excel.xlsx')
    wb.close()
    pythoncom.CoInitialize()
    excel = win32com.client.Dispatch("Excel.Application")
    file = excel.Workbooks.Open('C:/Users/ibuch/Desktop/python/Project-JRMS/static/excel/report_excel.xlsx')
    file.WorkSheets("サンプル").Activate()
    file.ActiveSheet.ExportAsFixedFormat(0, f'C:/Users/ibuch/Desktop/python/Project-JRMS/static/pdf/view.pdf')
    file.Close()
    excel.Quit()
    os.remove('C:/Users/ibuch/Desktop/python/Project-JRMS/static/excel/report_excel.xlsx')
    
    count=db.insert_report(input)
    if count==1:
        report_tuple=db.get_report_id()
        report_id=report_tuple[0]
        num=1
        db.insert_report_2(report_id,num,input['date_1'],input['interview_1'],input['test_1'])
        if input['test_2'] !='' or input['interview_2'] !='':
            num =2
            db.insert_report_2(report_id,num,input['date_2'],input['interview_2'],input['test_2'])
        if input['test_3'] !='' or input['interview_3'] !='':
            num =3
            db.insert_report_2(report_id,num,input['date_3'],input['interview_3'],input['test_3'])
        if input['test_4'] !='' or input['interview_4'] !='':
            num =4
            db.insert_report_2(report_id,num,input['date_4'],input['interview_4'],input['test_4'])
    return render_template('student/register_confirm.html')

@student_bp.route('/menu_by_confirm')
def menu_by_confirm():
    if 'user' in session:
        os.remove('C:/Users/ibuch/Desktop/python/Project-JRMS/static/pdf/view.pdf')
        return redirect(url_for('student.menu'))
    else:
        return redirect(url_for('sample_top'))

@student_bp.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('sample_top'))
