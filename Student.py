
from Person import Person

class Student(Person):
    def __init__(self, number, name, age, gender, role, grade, ID=None):
        super().__init__(number, name, age, gender,  role, ID)
        self.grade = grade
    def get_field_type(self):
        return 'Student'
    def get_table_type(self):
        return 'number'