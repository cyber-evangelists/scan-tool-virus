from beanie import Document

class User(Document):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str

    class Settings:
        name = "Users"