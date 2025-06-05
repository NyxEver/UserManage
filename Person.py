from abc import ABC, abstractmethod
from DatabaseManager import person_add, person_delete, person_update_dict, update_value, person_update, person_find


class Person(ABC):
    @abstractmethod
    def __init__(self,name,age,gender,number,role):
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
        self.role = role
    def save_SQL(self):
        result = person_add(self)
        return result
    def delete_SQL(self):
        result = person_delete(self)
        return result

    @staticmethod
    def update_dict(field_type, change_value, list_number):
        result_dict = person_update_dict(field_type, change_value, list_number)
        return result_dict

    @staticmethod
    def update_SQL(result_dict, new_values):
        updated_dict = update_value(result_dict, new_values)
        result_update = person_update(result_dict, updated_dict)
        return result_update

    @staticmethod
    def find_SQL(field_type, find_value):
        result = person_find(field_type, find_value)
        return result
    def get_field_type(self):
        pass
    def get_table_type(self):
        pass