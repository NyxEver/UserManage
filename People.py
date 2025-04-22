
class People:
    #people_number=0
    def __init__(self,name,age,gender,number):
        if not name:
            raise ValueError("你啥都没输入我咋记住你呢？")
        if age < 0 or age>=150:
            raise ValueError ("你输的那是人类的年龄吗？",age)
        if gender not in ['M','F']:
            raise ValueError("你输的那是人类的性别吗？")

        self.name=name
        self.age = age
        self.gender = gender
        self.number =number

    #def display_peopleN(self):
    #    print("现在有几个人：%d" % People.people_number)
    def display_people(self):
        print("Name:", self.name, ", age:", self.age, ", gender:", self.gender, ", number:", self.number)
    def __str__(self):
        return "Name:"+str(self.name)+", age:"+str(self.age)+", gender:"+str(self.gender)+", number:"+str(self.number)
