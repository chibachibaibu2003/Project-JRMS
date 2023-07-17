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
    sql='insert into report values(default,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
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
