import json

def GetNextUserID():
    with open('users.json') as userDb:
        db = json.load(userDb)
        cont = 0
        for i in db:
            cont += 1
            if cont >= len(db):
                return cont

def User(id, username, email, password):
    user = {
        "id":id,
        "username":username,
        "email":email,
        "password":password,
        "contacts":[{
            "name":"Bem Vindo",
            "email":"",
            "phone":"12345-5678",
        }]
    }
    return user

def Contact(name, email, phone):
    contact = {
        "name":name,
        "email":email,
        "phone":phone
    }
    return contact