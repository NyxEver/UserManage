import mysql.connector
from People import People

mydb = mysql.connector.connect(#数据库链接
    host="127.0.0.1"
    ,user="root"
    ,password="*"
    ,database="*"
)
print(mydb,"数据库连接成功!")

people_cursor = mydb.cursor()#创建游标
people_cursor.execute("CREATE TABLE if not exists people (id INT AUTO_INCREMENT PRIMARY KEY,"#执行创建表的SQL语句
                       "name varchar(255) not null, age char(3) not null"
                       ",gender varchar(1),number char(10) not null)")
people_cursor.close()#关闭游标
print("表 'people' 检查/创建 完成.")

def people_add(name, age, gender, number):#添加方法
    try:
        #person = People(name, age, gender, number)
        peopleAdd_cursor = mydb.cursor()
        peopleAdd_cursor.execute("INSERT INTO people(name,age,gender,number) values(%s,%s,%s,%s)",(name, age, gender, number))# 执行sql语句
        #peopleAdd_cursor.execute("INSERT INTO people (name, age, gender, number) values(%s,%s,%s,%s)",(person.name, person.age, person.gender, person.number))
        mydb.commit()# 提交到数据库执行
        print(f"{peopleAdd_cursor.rowcount} 条记录插入成功: Name:{name}")
        #print(f"{peopleAdd_cursor.rowcount} 条记录插入成功: {person}")#print(person) 调用 __str__()
        peopleAdd_cursor.close()
        return True# 返回操作成功状态
    except mysql.connector.Error as error:
        print("出错内容：",error)
        return False# 返回操作失败状态

def people_delete(field_type , value):#删除方法，传入两个参数，1：类别，2：传入的参数
    people_delete_cursor = mydb.cursor()
    people_delete_cursor.execute(f"SELECT * FROM people where {field_type} = %s",(value,))#先寻找符合条件的记录
    for row in people_delete_cursor.fetchall():#接收全部的返回结果行
        print(f"找到了：ID={row[0]},Name={row[1]},age={row[2]},gender={row[3]},number={row[4]}")#打印确认
    del_input =input("请确认是否删除 y/n：")
    if del_input=="y":
        people_delete_cursor.execute(f"DELETE FROM people where {field_type} = %s",(value,))#确认删除符合条件的记录
        print(f"已删除{people_delete_cursor.rowcount}条记录：Name为{row[1]}的条例")
        mydb.commit()
        return True
    elif del_input=="n":
        print("取消删除成功")
        return False
    people_delete_cursor.close()

def people_change(field_type , value_1 ,value_2):#修改方法，传入三个参数，1：类别，2：传入的老参数，3：传入的新参数
    if field_type == 'name':#验证传入的名字参数
        test_person=People(value_2,20,'M','202020')
    elif field_type == 'age':#验证传入的年龄参数
        test_person=People('a',int(value_2),'M','202020')
    people_change_cursor = mydb.cursor()
    people_change_cursor.execute(f"UPDATE people SET {field_type} = %s where {field_type} = %s", (value_2, value_1,))#修改符合条件的记录
    mydb.commit()#提交
    print("修改成功")
    people_change_cursor.close()
    return True

def people_find(field_type , value_1):
    #name, age, gender, number
    people_find_cursor = mydb.cursor()
    people_find_cursor.execute(f"SELECT * FROM people where {field_type} = %s",(value_1,))
    for row in people_find_cursor.fetchall():
        print(f"ID={row[0]},Name={row[1]},age={row[2]},gender={row[3]},number={row[4]}")
    people_find_cursor.close()
    return True

def all_people():#打印数据库内所有的
    all_people_cursor = mydb.cursor()
    all_people_cursor.execute("SELECT * FROM people")#搜索people表内所有的数据
    try:
        results_all=all_people_cursor.fetchall()
        all_people_cursor.close()
        return results_all
    except mysql.connector.Error as error:
        print(f"ERROR:{error}")
        return False