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
     
@admin_bp.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('sample_top'))    