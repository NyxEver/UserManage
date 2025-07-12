from abc import ABC, abstractmethod
from DatabaseManagePooling import user_add, user_delete, user_update, user_find, get_user_id, verify_account, register_account

class User_Template(ABC):
    def __init__(self,number,password,name,age,gender,role, grade, position, ID=None):
        if not name and role != 'root':#验证名字是否合法
            raise ValueError("你啥都没输入我咋记住你呢？")
        if age < 0 or age>=150:#验证年龄是否合法
            raise ValueError ("你输的那是人类的年龄吗？",age)
        if gender not in ['M','F']:#验证性别是否合法
            raise ValueError("你输的那是人类的性别吗？")

        self.ID = ID
        self.number = number
        self.password = password
        self.name = name
        self.age = age
        self.gender = gender
        self.role = role
        self.grade = grade
        self.position = position

    def save_SQL(self):
        result_save = user_add(self)
        return result_save
    def delete_SQL(self):
        result_delete = user_delete(self)
        return result_delete

    def update_SQL(self,get_id):
        result_update = user_update(self,get_id)
        return result_update

    @staticmethod
    def find_SQL(field_type, find_value):
        result_find = user_find(field_type, find_value)
        return result_find
    def get_user_ID(self):
        result_ID = get_user_id(self)
        return result_ID
    def get_field_type(self):
        pass
    def get_table_type(self):
        pass

    def register_account(self):
        result_register = register_account(self)
        return result_register

    @staticmethod
    def verify_user_account(number, password):
        result_verify = verify_account(number, password)
        return result_verify
