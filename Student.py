
from Person import Person

class Student(Person):
    def __init__(self, name, age, gender, number, role, grade):
        super().__init__(name, age, gender, number, role)
        self.grade = grade
    def get_field_type(self):
        return 'Student'
    def get_table_type(self):
        return 'number'