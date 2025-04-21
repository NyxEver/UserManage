import mysql.connector
from People import People

mydb = mysql.connector.connect(
    host="127.0.0.1"
    ,user="root"
    ,password="****"
    ,database="****"
)
print(mydb,"数据库连接成功!")

people_cursor = mydb.cursor()
people_cursor.execute("CREATE TABLE if not exists people (id INT AUTO_INCREMENT PRIMARY KEY,"
                       "name varchar(255) not null, age char(3) not null"
                       ",gender varchar(1),number char(10) not null)")
people_cursor.close()
print("表 'people' 检查/创建 完成.")

def people_add(name, age, gender, number):
    try:
        person = People(name, age, gender, number)# 创建People对象进行验证
        peopleAdd_cursor = mydb.cursor()
        #peopleAdd_cursor.execute("INSERT INTO people(name,age,gender,number) values(%s,%s,%s,%s)",(name, age, gender, number))# 执行sql语句
        peopleAdd_cursor.execute("INSERT INTO people (name, age, gender, number) values(%s,%s,%s,%s)",
                                 (person.name, person.age, person.gender, person.number))
        mydb.commit()# 提交到数据库执行
        #print(f"{peopleAdd_cursor.rowcount} 条记录插入成功: Name={name}")
        print(f"{peopleAdd_cursor.rowcount} 条记录插入成功: {person}")#print(person) 调用 __str__()
        peopleAdd_cursor.close()
        return True
    except mysql.connector.Error as error:
        print("出错内容：",error)
        return False

def people_delete(field_type , value):
    people_delete_cursor = mydb.cursor()
    people_delete_cursor.execute(f"SELECT * FROM people where {field_type} = %s",(value,))
    for row in people_delete_cursor.fetchall():
        print(f"ID={row[0]},Name={row[1]},age={row[2]},gender={row[3]},number={row[4]}")
    del_input =input("请再次确认是否删除 y/n：")
    if del_input=="y":
        people_delete_cursor.execute(f"DELETE FROM people where {field_type} = %s",(value,))
    elif del_input=="n":
        print("取消删除成功")
    people_delete_cursor.close()

def people_change(field_type , value_1 ,value_2):
    people_change_cursor = mydb.cursor()
    people_change_cursor.execute(f"UPDATE people SET {field_type} = %s where {field_type} = %s",(value_2,value_1,))
    mydb.commit()
    for row in people_change_cursor.fetchall():
        print(f"ID={row[0]},Name={row[1]},age={row[2]},gender={row[3]},number={row[4]}")
    print("修改成功")
    people_change_cursor.close()

def peopleName_find(name):
    people_name_cursor = mydb.cursor()
    people_name_cursor.execute("SELECT * FROM people where name=%s",(name,))
    for row in people_name_cursor.fetchall():
        print(f"ID={row[0]},Name={row[1]},age={row[2]},gender={row[3]},number={row[4]}")
    people_name_cursor.close()

def peopleAge_find(age):
    people_age_cursor = mydb.cursor()
    people_age_cursor.execute("SELECT * FROM people where age=%s",(age,))
    for row in people_age_cursor.fetchall():
        print(f"ID={row[0]},Name={row[1]},age={row[2]},gender={row[3]},number={row[4]}")
    people_age_cursor.close()

def peopleGender_find(gender):
    people_gender_cursor = mydb.cursor()
    people_gender_cursor.execute("SELECT * FROM people where gender=%s",(gender,))
    for row in people_gender_cursor.fetchall():
        print(f"ID={row[0]},Name={row[1]},age={row[2]},gender={row[3]},number={row[4]}")
    people_gender_cursor.close()

def peopleNumber_find(number):
    people_number_cursor = mydb.cursor()
    people_number_cursor.execute("SELECT * FROM people where number=%s",(number,))
    for row in people_number_cursor.fetchall():
        print(f"ID={row[0]},Name={row[1]},age={row[2]},gender={row[3]},number={row[4]}")
    people_number_cursor.close()

def all_people():
    allpeople_cursor = mydb.cursor()
    allpeople_cursor.execute("SELECT * FROM people")
    try:
        for row in allpeople_cursor.fetchall():
            array=row[0]
            name=row[1]
            age=row[2]
            gender=row[3]
            number=row[4]
            print(f"名单列表：ID={array}Name={name}, age={age}, gender={gender}, number={number}")
            allpeople_cursor.close()
    except mysql.connector.Error as error:
        print(f"ERROR:{error}")