from User_Template import User_Template

class User(User_Template):
    def __init__(self,number,password,name,age,gender,role, grade, position, ID=None):
        super().__init__(number,password,name,age,gender,role, grade, position, ID)