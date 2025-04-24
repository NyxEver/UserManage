
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
