
from Person import Person

class Teacher(Person):
    def __init__(self, number, name, age, gender, role, position, ID=None):
        super().__init__(number, name, age, gender, role, ID)
        self.position =position#职位
    def get_field_type(self):
        return 'Teacher'
    def get_table_type(self):
        return 'number'