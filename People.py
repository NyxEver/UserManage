
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
    def display_people(self):
        print("Name:", self.name, ", age:", self.age, ", gender:", self.gender, ", number:", self.number)
    def __str__(self):
        return "Name:"+str(self.name)+", age:"+str(self.age)+", gender:"+str(self.gender)+", number:"+str(self.number)
