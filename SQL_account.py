import mysql.connector

mydb = mysql.connector.connect(#数据库链接
    host="127.0.0.1"
    ,user="root"
    ,password="*"
    ,database="*"
)
print(mydb,"数据库连接成功!")

account_cursor = mydb.cursor()#创建游标
account_cursor.execute("CREATE TABLE if not exists account (id INT AUTO_INCREMENT PRIMARY KEY,"#执行创建表的SQL语句
                       "username VARCHAR(50) not null,password VARCHAR(255) not null)")
account_cursor.close()#关闭游标
print("表 'account' 检查/创建 完成.")

account_cursor = mydb.cursor()#创建游标
test_account="insert into student_db.account(username,password) values('admin', 'admin123')"
account_cursor.execute(test_account)
mydb.commit()
print("账号创建成功")
account_cursor.close()

def verify_account(username,password):
    verify_account_cursor = mydb.cursor()
    verify_account_cursor.execute(f"SELECT * FROM account where {username} = %s and {password} = %s",(username,password))
    if verify_account_cursor.fetchone():
        return True
    else:
        return False