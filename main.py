from People import *
from SQL import (people_add,people_delete,people_change,
                 peopleName_find,peopleAge_find,peopleGender_find,peopleNumber_find,all_people)

print("2025.04.16")
print("管理系统")

while True:
    print("输入数字 1.增加   2.删除   3.改变   4.查找   5.全部   6.退出")
    user_input = int(input("输入数字选择功能："))
    if user_input == 1:
        user_name = input("Enter your name:")
        user_age = int(input("Enter your age:"))
        user_gender = input("Enter your gender:")
        user_number = int(input("Enter your number:"))
        people_add(user_name, user_age, user_gender, user_number)
    elif user_input == 2:
        print("请输入删除的选择：1.name 2.age 3.gender 4.number")
        del_input = int(input("输入数字选择功能："))
        if del_input == 1:
            del_name = input("请输入想删除的：")
            people_delete("name", del_name)
    elif user_input == 3:
        print("请输入修改的选择：1.name 2.age 3.gender 4.number")
        change_input = int(input("输入数字选择功能："))
        if change_input == 1:
            change_name1 = input("请输入想修改的：")
            change_name2 = input("请输入修改后的名称：")
            people_change("name", change_name1, change_name2)
    elif user_input == 4:
        print("请输入查找的选择：1.name 2.age 3.gender 4.number")
        find_input = int(input("输入数字选择功能："))
        if find_input==1:
            find_name = input("请输入想查找的名字：")
            peopleName_find(find_name)
        if find_input==2:
            find_age = input("请输入想查找的年龄：")
            peopleAge_find(find_age)
        if find_input==3:
            find_gender = input("请输入想查找的性别：")
            peopleGender_find(find_gender)
        if find_input==4:
            find_number = input("请输入想查找的号码：")
            peopleNumber_find(find_number)
    elif user_input == 5:
        all_people()
    elif user_input == 6:
        print("程序结束")
        break