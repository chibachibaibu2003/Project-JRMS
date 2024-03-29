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
            if 'input' in session:
                session.pop('input',None)
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
    sheet['f10'].value=input['company_name']
    sheet['AL10'].value=input['company_tel']
    sheet['f11'].value=input['location']
    sheet['AB12'].value=input['course']
    sheet['f13'].value=input['occupation']
    sheet['s13'].value=input['industory']
    sheet['ah13'].value=input['application']
    sheet['i15'].value=input['date_1']
    sheet['i16'].value=input['test_1']
    sheet['i17'].value=input['interview_1']
    if input['date_2'] !='2023-01-01':
        sheet['i18'].value=input['date_2']
    sheet['i19'].value=input['test_2']
    sheet['i20'].value=input['interview_2']
    if input['date_3'] !='2023-01-01':
        sheet['i21'].value=input['date_3']
    sheet['i22'].value=input['test_3']
    sheet['i23'].value=input['interview_3']
    if input['date_4'] !='2023-01-01':
        sheet['i24'].value=input['date_4']
    sheet['i25'].value=input['test_4']
    sheet['i26'].value=input['interview_4']
    sheet['d28'].value=input['report_test_1']
    sheet['d29'].value=input['report_test_2']
    sheet['d30'].value=input['report_test_3']
    sheet['d31'].value=input['report_test_4']
    sheet['d32'].value=input['report_test_5']
    sheet['d33'].value=input['report_test_6']
    sheet['d34'].value=input['report_test_7']
    sheet['d35'].value=input['report_test_8']
    sheet['d36'].value=input['report_test_9']
    sheet['d37'].value=input['report_test_10']
    sheet['d38'].value=input['report_test_11']
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
        if input['date_2'] !='2023-01-01':
            num =2
            db.insert_report_2(report_id,num,input['date_2'],input['interview_2'],input['test_2'])
        if input['date_3'] !='2023-01-01':
            num =3
            db.insert_report_2(report_id,num,input['date_3'],input['interview_3'],input['test_3'])
        if input['date_4'] !='2023-01-01':
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
    
@student_bp.route('/correction')
def correction_select():
    if 'user' in session:
        id=session['user_id']
        data_list=db.user_report_correction_list(id)
        return render_template('student/correction_select.html',datas=data_list)
    else:
        return redirect(url_for('sample_top'))

@student_bp.route('/correction_2/<int:id>')
def correction(id):
    if 'user' in session:
        revision=db.report_revision_search(id)[0]
        session['revision']=revision
        session['report_id']=id
        text=db.get_correct_text(id)[0]
        li=[]
        for str in text.split('\n'):
            li.append(str)
        return render_template('student/correction.html',datas=revision,texts=li)
    else:
        return redirect(url_for('sample_top'))
    
@student_bp.route('/correction3',methods=['POST'])
def correction_confirm():
    if 'user' in session:
        id=session['report_id']
        company_name=request.form.get('company_name')
        tel_num=request.form.get('company_tel')
        location=request.form.get('company_location')
        name=request.form.get('name')
        study_course=request.form.get('course')
        occupation=request.form.get('occupation')
        industory=request.form.get('industory')
        application=request.form.get('application')
        report1=request.form.get('report_test_1')
        report2=request.form.get('report_test_2')
        report3=request.form.get('report_test_3')
        report4=request.form.get('report_test_4')
        report5=request.form.get('report_test_5')
        report6=request.form.get('report_test_6')
        report7=request.form.get('report_test_7')
        report8=request.form.get('report_test_8')
        report9=request.form.get('report_test_9')
        report10=request.form.get('report_test_10')
        report11=request.form.get('report_test_11')
        text=f'{report1}\n{report2}\n{report3}\n{report4}\n{report5}\n{report6}\n{report7}\n{report8}\n{report9}\n{report10}\n{report11}'
        li=[company_name,tel_num,location,name,study_course,occupation,industory,application,text]
        db.update_report(li,id)
        return render_template('student/top.html')
    else:
        return redirect(url_for('sample_top'))

@student_bp.route('/search_report')
def search_report():
    if 'user' in session:
        return render_template('student/search_report.html')
    else:
        return redirect(url_for('sample_top'))

@student_bp.route('/search_report_list',methods=['POST'])
def search_report_list():
    if 'user' in session:
        word=request.form.get('search_box')
        industory=request.form.get('industory')
        application=request.form.get('application')
        data=[industory,application]
        report_list=db.report_public_list(data,word)
        return render_template('student/search_report_list.html',datas=report_list)
    else:
        return redirect(url_for('sample_top'))

@student_bp.route('/correction_result/<int:id>')
def correction_result(id):
    if 'user' in session:
        data=db.report_search(id)
        test=db.report_test_search(id)
        shutil.copy('./Project-JRMS/static/excel/Excelサンプル.xlsx','./Project-JRMS/static/excel/report_excel.xlsx')
        wb = openpyxl.load_workbook('./Project-JRMS/static/excel/report_excel.xlsx')
        sheet = wb['サンプル']
        sheet['f12'].value=data[1]
        sheet['f10'].value=data[4]
        sheet['AL10'].value=data[6]
        sheet['f11'].value=data[7]
        sheet['AB12'].value=data[3]
        sheet['f13'].value=data[8]
        sheet['s13'].value=data[9]
        sheet['ah13'].value=data[10]
        sheet['i15'].value=test[0][3]
        sheet['i16'].value=test[0][5]
        sheet['i17'].value=test[0][4]
        if len(test)>=2:
            sheet['i18'].value=test[1][3]
            sheet['i19'].value=test[1][5]
            sheet['i20'].value=test[1][4]
        if len(test)>=3:
            sheet['i21'].value=test[2][3]
            sheet['i22'].value=test[2][5]
            sheet['i23'].value=test[2][4]
        if len(test)==4:
            sheet['i24'].value=test[3][3]
            sheet['i25'].value=test[3][5]
            sheet['i26'].value=test[3][4]
        num=27
        for wd in data[11].split('\n'):
            num+=1
            num_str='D'+str(num)
            sheet[num_str].value=wd
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
        return render_template('student/search_report_result.html')
    else:
        return redirect(url_for('sample_top'))

@student_bp.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('sample_top'))
