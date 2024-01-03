from beanie import Document

class User(Document):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
<<<<<<< HEAD
    role: str

    class Settings:
        name = "users"
=======

    class Settings:
        name = "Users"
>>>>>>> c18931cd379c94ab8ef653a2d07b3d6f15040e9e
