import os
import mysql.connector

mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST', '127.0.0.1'), #os.getenv()：获取指定环境变量的值
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', '2397947891'),
    database=os.getenv('DB_NAME', 'student_db')
)


account_cursor = mydb.cursor()#创建游标
account_cursor.execute("CREATE TABLE if not exists account (username VARCHAR(20) PRIMARY KEY,"#执行创建表的SQL语句
                       "password VARCHAR(50) not null,identify char(1) not null)")
account_cursor.close()#关闭游标
print("表 'account' 检查/创建 完成.")

account_cursor = mydb.cursor()#创建游标
account_cursor.execute("SELECT * FROM account where username = 'admin'")
if not account_cursor.fetchone():
    try:
        test_account="insert into student_db.account(username,password,identify) values('admin', 'admin123','0')"#0为root身份代表，1为游客身份
        account_cursor.execute(test_account)
        mydb.commit()
        print("账号创建成功")
    except mysql.connector.Error as error:
        print(error)
else:
    print("跳过创建")
account_cursor.close()

def verify_account(username,password):
    verify_account_cursor = mydb.cursor()
    verify_account_cursor.execute("SELECT * FROM account where username = %s and password = %s",(username,password,))
    if verify_account_cursor.fetchone():
        return True
    else:
        return False

def register_account(username,password,identify=1):#只能注册游客身份
    try:
        register_account_cursor = mydb.cursor()
        register_account_cursor.execute("insert into account(username,password,identify) values(%s,%s,%s)",(username,password,identify))
        mydb.commit()
        register_account_cursor.close()
        return True
    except mysql.connector.Error as error:
        return False