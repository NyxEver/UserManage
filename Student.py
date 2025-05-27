from DatabaseManager import person_add, person_find
from Person import Person

class Student(Person):
    def __init__(self, name, age, gender, number, grade):
        super().__init__(name, age, gender, number)
        self.grade = grade

    def save_SQL(self):
        result = person_add(self)
        return result
    def delete_SQL(self):
        result = person_delete(self)
        return result
    def update_SQL(self):
        result = person_update(self)
        return result
    def find_SQL(self,field_type,find_value):
        result = person_find(field_type,find_value)
        return result