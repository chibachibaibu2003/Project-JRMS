import os,psycopg2,string,random,hashlib,datetime
from flask import session

def get_connection():
    url=os.environ['DATABASE_URL']
    connection=psycopg2.connect(url)
    return connection

def insert_user(pw,mail):
    sql='insert into user_account values(default,%s,%s,%s,0)'
    
    salt=get_salt()
    hashed_pw=get_hash(pw,salt)
    
    try:
        connection=get_connection()
        cursor=connection.cursor()
        
        cursor.execute(sql,(mail,salt,hashed_pw))
        count=cursor.rowcount
        connection.commit()
        
    except psycopg2.DatabaseError:
        count=0
    
    finally:
        cursor.close()
        connection.close()
        
    return count

def login(mail,pw):
    sql="select pass,salt,user_lank,id from user_account where mail=%s"
    flg=False
    id=0
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql,(mail,))
        user=cursor.fetchone()
        lank=0
        if user != None:
            salt=user[1]
            hashed_pw=get_hash(pw,salt)
            if hashed_pw== user[0]:
                flg=True
                lank=user[2]
                id=user[3]
    except psycopg2.DatabaseError :
        flg=False
        lank=0
    finally:
        cursor.close()
        connection.close()
    return flg,lank,id
            
def get_salt():
    charset=string.ascii_letters+string.digits
    salt=''.join(random.choices(charset,k=30))
    return salt

def get_hash(pw,salt):
    b_pw=bytes(pw,"utf-8")
    b_salt=bytes(salt,"utf-8")
    hashed_pw=hashlib.pbkdf2_hmac("sha256",b_pw,b_salt,1000).hex()
    return hashed_pw

def insert_report(date):
    sql="insert into report values(default,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'')"
    try:
        connection=get_connection()
        cursor=connection.cursor()
        today=datetime.date.today()
        id=session['user_id']
        test_report=f'{date["report_test_1"]}\n{date["report_test_2"]}\n{date["report_test_3"]}\n{date["report_test_4"]}\n{date["report_test_5"]}\n{date["report_test_6"]}\n{date["report_test_7"]}\n{date["report_test_8"]}\n{date["report_test_9"]}\n{date["report_test_10"]}\n{date["report_test_11"]}'
        cursor.execute(sql,(date['name'],date['student_num'],date['course'],date['company_name'],date['company_furigana'],date['company_tel'],date['location'],date['occupation'],date['industory'],date['application'],test_report,today,0,'{0,0,0,0,0,0,0,0,0,0,0,0,0}',id))
        count=cursor.rowcount
        
        connection.commit()
    except psycopg2.DatabaseError:
        count=0
    
    finally:
        cursor.close()
        connection.close()
        
    return count

def get_report_id():
    sql='select report_id from report order by report_id desc limit 1'
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql)
        id=cursor.fetchone()
        
    except psycopg2.DatabaseError :
        count=0
    finally:
        cursor.close()
        connection.close()
        # idはタプルです
    return id

def insert_report_2(id,num,date,interview,test):
    sql='insert into report_test values(default,%s,%s,%s,%s,%s)'
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql,(id,num,date,interview,test))
        count=cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError :
        count=0
    finally:
        cursor.close()
        connection.close()
    return count

def report_correction_list():
    sql='select company_name,submission_date,report_id from report where approval_rank < 2'
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql)
        list=cursor.fetchall()
        
    except psycopg2.DatabaseError :
        list=((0,0,0),(0,0,0))
    finally:
        cursor.close()
        connection.close()
        # listはlist型です
    return list

def user_report_correction_list(id):
    sql='select company_name,submission_date,report_id from report where approval_rank = 1 and user_id=%s'
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql,(id,))
        list=cursor.fetchall()
        
    except psycopg2.DatabaseError :
        list=((0,0,0),(0,0,0))
    finally:
        cursor.close()
        connection.close()
        # listはlist型です
    return list
    

def report_search(id):
    sql="select * from report where report_id=%s"
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql,(id,))
        list=cursor.fetchone()
    except psycopg2.DatabaseError :
        list=((0,0,0),)
    finally:
        cursor.close()
        connection.close()
        # listはタプル型です
    return list

def report_test_search(id):
    sql="select*from report_test where report_id=%s"
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql,(id,))
        list=cursor.fetchall()
    except psycopg2.DatabaseError :
        list=((0,0,0),)
    finally:
        cursor.close()
        connection.close()
        # listはタプル型です
    return list

def report_revision_search(id):
    sql="select revision_point from report where report_id=%s"
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql,(id,))
        list=cursor.fetchone()
    except psycopg2.DatabaseError :
        list=((0,0,0),)
    finally:
        cursor.close()
        connection.close()
        # listはタプル型です
    return list

def insert_report_revision(list,text,id):
    sql='update report set revision_point = %s , correct_text=%s where report_id=%s'
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql,(list,text,id))
        count=cursor.rowcount
        
        connection.commit()
    except psycopg2.DatabaseError:
        count=0
    
    finally:
        cursor.close()
        connection.close()
        
    return count

def report_approval(id,flag):
    sql='update report set approval_rank=%s where report_id=%s'
    if flag==1:
        rank=1
    elif flag==2:
        rank=2
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql,(rank,id))
        count=cursor.rowcount
        
        connection.commit()
    except psycopg2.DatabaseError:
        count=0
    
    finally:
        cursor.close()
        connection.close()
        
    return count

def update_report(list,id):
    sql1="update report set\u0020"
    sql2="name="
    sql3="study_course="
    sql4="company_name="
    sql5="tell_num="
    sql6="location="
    sql7="occupation="
    sql8="industory="
    sql9="application="
    sql14="test_report="
    sql15="where report_id=%s"
    revi=report_revision_search(id)[0]
    if revi[0]=='1':
        sql1=sql1+sql4+"'"+list[0]+"'"+','+'\u0020'
    if revi[1]=='1':
        #list[1]はstr型
        sql1=sql1+sql5+"'"+list[1]+"'"+','+'\u0020'
    if revi[2]=='1':
        sql1=sql1+sql6+"'"+list[2]+"'"+','+'\u0020'
    if revi[3]=='1':
        sql1=sql1+sql2+"'"+list[3]+"'"+','+'\u0020'
    if revi[4]=='1':
        sql1=sql1+sql3+"'"+list[4]+"'"+','+'\u0020'
    if revi[5]=='1':
        sql1=sql1+sql7+"'"+list[1]+"'"+','+'\u0020'
    if revi[6]=='1':
        sql1=sql1+sql8+"'"+list[6]+"'"+','+'\u0020'
    if revi[7]=='1':
        sql1=sql1+sql9+"'"+list[7]+"'"+','+'\u0020'
    if revi[12]=='1':
        sql1=sql1+sql14+"'"+list[8]+"'"+','+'\u0020'
    sql1=sql1[:-2]+'\u0020'+sql15
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql1,(id,))
        count=cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError :
        count=0
    finally:
        cursor.close()
        connection.close()
    return count

def get_correct_text(id):
    sql="select correct_text from report where report_id=%s"
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql,(id,))
        data=cursor.fetchone()
    except psycopg2.DatabaseError:
        data=""
    finally:
        cursor.close()
        connection.close()
        
    return data

def report_public_list(list,word):
    sql='select company_name,submission_date,report_id from report where approval_rank=2'
    if list[0]!="なし":
        sql=sql+'\u0020and\u0020'+'industory='+"'"+list[0]+"'"
    if list[1]!='なし':
        sql=sql+'\u0020and\u0020'+'application='+"'"+list[1]+"'"
    if word!="":
        sql=sql+'\u0020and\u0020'+'company_name\u0020like\u0020'+"'%"+word+"%'"
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql)
        list=cursor.fetchall()
        
    except psycopg2.DatabaseError :
        list=((0,0,0),(0,0,0))
    finally:
        cursor.close()
        connection.close()
        # listはlist型です
    return list
 
def delete_report_list():
    sql='select company_name,submission_date,report_id from report where approval_rank = 2'
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql)
        list=cursor.fetchall()
        
    except psycopg2.DatabaseError :
        list=((0,0,0),(0,0,0))
    finally:
        cursor.close()
        connection.close()
        # listはlist型です
    return list   

def delete_report(id):
    sql="delete from report where report_id=%s"
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql,(id,))
        count=cursor.rowcount
        connection.commit()
        
    except psycopg2.DatabaseError :
        count=0
    finally:
        cursor.close()
        connection.close()
        
    return count

def delete_report_test(id):
    sql="delete from report_test where report_id=%s"
    try:
        connection=get_connection()
        cursor=connection.cursor()
        cursor.execute(sql,(id,))
        count=cursor.rowcount
        connection.commit()
        
    except psycopg2.DatabaseError :
        count=0
    finally:
        cursor.close()
        connection.close()
        
    return count 

li=["",""]
wd=''
list=report_public_list(li,wd)
print(list)
lis=delete_report_list()
print(lis)