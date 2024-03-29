from flask import Flask,Blueprint, render_template,redirect,url_for,request,session
import random,string,db,shutil,pythoncom,os
import win32com.client
import openpyxl

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
        return render_template('admin/top.html')
    else:
        return redirect(url_for('sample_top'))

@admin_bp.route('/correction')
def correction_select():
    if 'user' in session:
        data_list=db.report_correction_list()
        return render_template('admin/correction_select.html',datas=data_list)
    else:
        return redirect(url_for('sample_top'))


@admin_bp.route('/correction_2/<int:id>')
def correction(id):
    if 'user' in session:
        report_id=id
        session['report_id']=report_id
        data=db.report_search(report_id)
        test=db.report_test_search(report_id)
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
        return render_template('admin/correction.html')
    else:
        return redirect(url_for('sample_top'))

@admin_bp.route('/menu_by_confirm')
def menu_by_confirm():
    if 'user' in session:
        os.remove('C:/Users/ibuch/Desktop/python/Project-JRMS/static/pdf/view.pdf')
        return redirect(url_for('admin.menu'))
    else:
        return redirect(url_for('sample_top'))

@admin_bp.route('/correction_confirm',methods=['POST'])
def correct_confirm():
    if 'user' in session:
        id=session['report_id']
        rank=1
        data1=request.form.get('check_1')
        data2=request.form.get('check_2')
        data3=request.form.get('check_3')
        data4=request.form.get('check_4')
        data5=request.form.get('check_5')
        data6=request.form.get('check_6')
        data7=request.form.get('check_7')
        data8=request.form.get('check_8')
        data9=request.form.get('check_9')
        data10=request.form.get('check_10')
        data11=request.form.get('check_11')
        data12=request.form.get('check_12')
        data13=request.form.get('check_13')
        text1=request.form.get('text_1')
        text2=request.form.get('text_2')
        text3=request.form.get('text_3')
        text4=request.form.get('text_4')
        text5=request.form.get('text_5')
        text6=request.form.get('text_6')
        text7=request.form.get('text_7')
        text=f'{text1}\n{text2}\n{text3}\n{text4}\n{text5}\n{text6}\n{text7}'
        updata_list=[data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,data11,data12,data13]
        db.insert_report_revision(updata_list,text,id)
        db.report_approval(id,rank)
        os.remove('C:/Users/ibuch/Desktop/python/Project-JRMS/static/pdf/view.pdf')
        return redirect(url_for('admin.menu'))
    else:
        return redirect(url_for('sample_top'))

@admin_bp.route('/approval')
def approval():
    if 'user' in session:
        id=session['report_id']
        rank=2
        db.report_approval(id,rank)
        os.remove('C:/Users/ibuch/Desktop/python/Project-JRMS/static/pdf/view.pdf')
        return redirect(url_for('admin.menu'))
    else:
        return redirect(url_for('sample_top'))

@admin_bp.route('/search_report')
def search_report():
    if 'user' in session:
        return render_template('admin/search_report.html')
    else:
        return redirect(url_for('sample_top'))

@admin_bp.route('/search_report_list',methods=['POST'])
def search_report_list():
    if 'user' in session:
        word=request.form.get('search_box')
        industory=request.form.get('industory')
        application=request.form.get('application')
        data=[industory,application]
        report_list=db.report_public_list(data,word)
        return render_template('admin/search_report_list.html',datas=report_list)
    else:
        return redirect(url_for('sample_top'))

@admin_bp.route('/correction_result/<int:id>')
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
        return render_template('admin/search_report_result.html')
    else:
        return redirect(url_for('sample_top'))

@admin_bp.route('/delete_report_select')
def delete_report_select():
    if 'user' in session:
        list=db.delete_report_list()
        return render_template('admin/delete_report_select.html',datas=list)
    else:
        return redirect(url_for('sample_top'))

@admin_bp.route('/delete_report/<int:id>')
def delete_report(id):
    if 'user' in session:
        db.delete_report_test(id)
        db.delete_report(id)
        return render_template('admin/top.html')
    else:
        return redirect(url_for('sample_top'))
    
@admin_bp.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('sample_top'))