#memory list version v0.1

"""
main.py:
from People import *

print("2025.03.22")
print("管理系统")
people_list = []

#print("输入数字 1.增加   2.删除   3.改变   4.查找   5.退出")# 开始主循环，让程序持续运行直到用户选择退出
while True:
    print("输入数字 1.增加   2.删除   3.改变   4.查找   5.全部   6.退出")
    user_input = int(input("输入数字选择功能："))
    if user_input == 1:
        h_input = int(input("是否开始添加？（1/2）："))
        while h_input == 1:
            user_name = input("Enter your name:")
            user_age = int(input("Enter your age:"))
            user_gender = input("Enter your gender:")
            user_number = int(input("Enter your number:"))
            people = People(user_name, user_age, user_gender, user_number)# 使用输入的信息创建一个 People 类的实例 (对象)
            people_list.append(people)
            user_input2 = int(input("是否继续添加？（1/2）"))
            if user_input2 != 1:
                for people in people_list:
                    print("当前清单：", people)
                break
        else:
            pass
    elif user_input == 2:
        del_name = input("请输入想删除的：")
        People.Delete_method(del_name,people_list)
    elif user_input == 3:
        cha_name = input("请输入想修改的：")
        People.Change_method(cha_name, people_list)
    elif user_input == 4:
        find_name = input("请输入想查找的：")
        People.Find_method(find_name,people_list)
    elif user_input == 5:
        for people in people_list:
            print("当前清单：", people)
    elif user_input == 6:
        print("程序结束")
        break

People.py:


class People:
    #people_number=0
    def __init__(self,name,age,gender,number):
        self.name=name
        self.age = age
        self.gender = gender
        self.number =number
        #People.people_number += 1  # 在创建对象时自动增加计数

    #def display_peopleN(self):
    #    print("现在有几个人：%d" % People.people_number)
    def display_people(self): # 实例方法，用于打印该对象（人）的详细信息
        print("Name:", self.name, ", age:", self.age, ", gender:", self.gender, ", number:", self.number)
    def __str__(self):# 特殊方法定义了当 print() 函数作用于 People 对象时应如何显示
        return "Name:"+str(self.name)+", age:"+str(self.age)+", gender:"+str(self.gender)+", number:"+str(self.number)

        def Delete_method(del_name,list_param):
        for person in list_param:
            if person.name == del_name:
                list_param.remove(person)
                print("Deleted")
        #return list

    def Find_method(find_name,list_param):
        for person in list_param:
            if person.name == find_name:
                print(person.name)
                print(person.age)
                print(person.gender)
                print(person.number)
                break
            else:
                pass
    def Change_method(cha_name,list_param):
        for person in list_param:
            if person.name == cha_name:
                person.age = int(input("Enter your age: "))
                person.gender = input("Enter your gender: ")
                person.number = int(input("Enter your number: "))
                print(person.name)
                print(person.age)
                print(person.gender)
                print(person.number)
            else:
                pass
"""