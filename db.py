import os,psycopg2,string,random,hashlib

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

def get_salt():
    charset=string.ascii_letters+string.digits
    salt=''.join(random.choices(charset,k=30))
    return salt

def get_hash(pw,salt):
    b_pw=bytes(pw,"utf-8")
    b_salt=bytes(salt,"utf-8")
    hashed_pw=hashlib.pbkdf2_hmac("sha256",b_pw,b_salt,1000).hex()
    return hashed_pw

