from abandon.People import *
from SQL_People import (people_add, people_delete, people_change,
                        peopleName_find, peopleAge_find, peopleGender_find, peopleNumber_find, all_people)

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