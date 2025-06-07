from abc import ABC, abstractmethod
from DatabaseManager import person_add, person_delete, person_update, person_find, get_person_id


class Person(ABC):
    def __init__(self,number,name,age,gender,role,ID=None):
        if not name:#验证名字是否合法
            raise ValueError("你啥都没输入我咋记住你呢？")
        if age < 0 or age>=150:#验证年龄是否合法
            raise ValueError ("你输的那是人类的年龄吗？",age)
        if gender not in ['M','F']:#验证性别是否合法
            raise ValueError("你输的那是人类的性别吗？")

        self.ID = ID
        self.number = number
        self.name = name
        self.age = age
        self.gender = gender
        self.role = role
    def save_SQL(self):
        result_save = person_add(self)
        return result_save
    def delete_SQL(self):
        result_delete = person_delete(self)
        return result_delete

    def update_SQL(self,get_id):
        #updated_dict = update_value(result_dict, new_values)
        result_update = person_update(self,get_id)
        return result_update

    @staticmethod
    def find_SQL(field_type, find_value):
        result = person_find(field_type, find_value)
        return result
    def get_person_ID(self):
        result_ID = get_person_id(self)
        return result_ID
    def get_field_type(self):
        pass
    def get_table_type(self):
        pass