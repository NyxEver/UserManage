
from Person import Person

class Teacher(Person):
    def __init__(self, name, age, gender, number, role, position):
        super().__init__(name, age, gender, number, role)
        self.position =position#职位
    def get_field_type(self):
        return 'Teacher'
    def get_table_type(self):
        return 'number'