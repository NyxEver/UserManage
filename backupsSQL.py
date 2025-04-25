#SQL storage version v0.2

"""
main.py:
from People import *
from SQL import (people_add,people_delete,people_change,
                 peopleName_find,peopleAge_find,peopleGender_find,peopleNumber_find,all_people)

print("2025.04.16")
print("管理系统")

while True:
    print("输入数字 1.增加   2.删除   3.改变   4.查找   5.全部   6.退出")
    user_input = int(input("输入数字选择功能："))
    if user_input == 1:#添加部分
        try:
            user_name = input("Enter your name:")
            user_age = int(input("Enter your age:"))
            user_gender = input("Enter your gender:")
            user_number = int(input("Enter your number:"))
            people = People(user_name, user_age, user_gender, user_number)# 创建People对象进行验证
            people_add(user_name, user_age, user_gender, user_number)#将数据传入SQL.py的添加方法中
        except ValueError as value_error:
            print(f"输入错误：{value_error}")
    elif user_input == 2:#删除部分
        key_del_input = int(input("请输入删除的选择——1.name 2.age 3.number："))
        key_del = {1:('name',"想要删除的名字："),2:('age',"想要删除的年龄："),3:('number',"想要删除的号码：")}#字典、元组嵌套
        if key_del_input in key_del:
            del_type, del_value = key_del[key_del_input]#元组元素对应
            value=input(del_value)
            people_delete(del_type, value)#将数据传入SQL.py的方法中
        else:
            print("请重新输入")
    elif user_input == 3:#修改方法
        try:
            key_change_input = int(input("请输入修改的选择——1.name 2.age 3.number："))
            key_change = {1: ('name', "想要修改的名字：","修改后的名字："), 2: ('age', "想要修改的年龄：","修改后的年龄："),
                3: ('number', "想要修改的号码：","修改后的号码：")}  # 字典、元组嵌套
            if key_change_input in key_change:
                change_type, change_value1,change_value2 = key_change[key_change_input]
                value1 = input(change_value1)
                value2 = input(change_value2)
                people_change(change_type, value1,value2)#将数据传入SQL.py的方法中
            else:
                print("请重新输入")
        except ValueError as error:
            print(f"修改后的数据验证失败: {error}")
    elif user_input == 4:#查找方法，最初使用单一功能的方法
        print("请输入查找的选择：1.name 2.age 3.gender 4.number")
        find_input = int(input("输入数字选择功能："))
        if find_input==1:
            find_name = input("请输入想查找的名字：")
            peopleName_find(find_name)#将数据传入SQL.py的方法中
        if find_input==2:
            find_age = input("请输入想查找的年龄：")
            peopleAge_find(find_age)#将数据传入SQL.py的方法中
        if find_input==3:
            find_gender = input("请输入想查找的性别：")
            peopleGender_find(find_gender)#将数据传入SQL.py的方法中
        if find_input==4:
            find_number = input("请输入想查找的号码：")
            peopleNumber_find(find_number)#将数据传入SQL.py的方法中
    elif user_input == 5:#无需传参，直接调用方法
        all_people()
    elif user_input == 6:#退出程序
        print("程序结束")
        break

People.py:
class People:
    def __init__(self,name,age,gender,number):#构造方法
        if not name:#验证名字是否合法
            raise ValueError("你啥都没输入我咋记住你呢？")
        if age < 0 or age>=150:#验证年龄是否合法
            raise ValueError ("你输的那是人类的年龄吗？",age)
        if gender not in ['M','F']:#验证性别是否合法
            raise ValueError("你输的那是人类的性别吗？")

        self.name=name
        self.age = age
        self.gender = gender
        self.number =number

    def __str__(self):#提供了对象的字符串表示形式
        return "Name:"+str(self.name)+", age:"+str(self.age)+", gender:"+str(self.gender)+", number:"+str(self.number)

SQL.py:
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
    return True
    people_change_cursor.close()

def peopleName_find(name):#寻找方法：名字
    people_name_cursor = mydb.cursor()
    people_name_cursor.execute("SELECT * FROM people where name=%s",(name,))
    for row in people_name_cursor.fetchall():
        print(f"ID={row[0]},Name={row[1]},age={row[2]},gender={row[3]},number={row[4]}")
    people_name_cursor.close()
    return True

def peopleAge_find(age):#寻找方法：年龄
    people_age_cursor = mydb.cursor()
    people_age_cursor.execute("SELECT * FROM people where age=%s",(age,))
    for row in people_age_cursor.fetchall():
        print(f"ID={row[0]},Name={row[1]},age={row[2]},gender={row[3]},number={row[4]}")
    people_age_cursor.close()
    return True

def peopleGender_find(gender):#寻找方法：性别
    people_gender_cursor = mydb.cursor()
    people_gender_cursor.execute("SELECT * FROM people where gender=%s",(gender,))
    for row in people_gender_cursor.fetchall():
        print(f"ID={row[0]},Name={row[1]},age={row[2]},gender={row[3]},number={row[4]}")
    people_gender_cursor.close()
    return True

def peopleNumber_find(number):#寻找方法：号码
    people_number_cursor = mydb.cursor()
    people_number_cursor.execute("SELECT * FROM people where number=%s",(number,))
    for row in people_number_cursor.fetchall():
        print(f"ID={row[0]},Name={row[1]},age={row[2]},gender={row[3]},number={row[4]}")
    people_number_cursor.close()
    return True

def all_people():#打印数据库内所有的
    all_people_cursor = mydb.cursor()
    all_people_cursor.execute("SELECT * FROM people")#搜索people表内所有的数据
    try:
        for row in all_people_cursor.fetchall():#遍历并接收全部的返回结果行
            array=row[0]
            name=row[1]
            age=row[2]
            gender=row[3]
            number=row[4]
            print(f"名单列表：ID={array}Name={name}, age={age}, gender={gender}, number={number}")#格式化打印
        all_people_cursor.close()
        return True
    except mysql.connector.Error as error:
        print(f"ERROR:{error}")
        return False
"""