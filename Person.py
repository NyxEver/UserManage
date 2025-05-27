from abc import ABC, abstractmethod
class Person(ABC):
    @abstractmethod
    def __init__(self,name,age,gender,number):
        if not name:#验证名字是否合法
            raise ValueError("你啥都没输入我咋记住你呢？")
        if age < 0 or age>=150:#验证年龄是否合法
            raise ValueError ("你输的那是人类的年龄吗？",age)
        if gender not in ['M','F']:#验证性别是否合法
            raise ValueError("你输的那是人类的性别吗？")

        self.name = name
        self.age = age
        self.gender = gender
        self.number = number

    def save_SQL(self):
        pass
    def delete_SQL(self):
        pass
    def update_SQL(self):
        pass
    def find_SQL(self):
        pass