import json
from flask import (Flask, flash, redirect, render_template, request, session)
from app.models import GetNextUserID, User, Contact
from werkzeug.security import generate_password_hash, check_password_hash

#-------------------------------------------------------------------------------------------------------------------------------------------#

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uzumymw'

#-------------------------------------------------------------------------------------------------------------------------------------------#

@app.route('/', methods=['GET'])
def index():
    session['username'] = None
    return render_template('index.html')

#-------------------------------------------------------------------------------------------------------------------------------------------#

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('login-user')
    password = request.form.get('login-password')
    with open('users.json') as json_file:
        data = json.load(json_file)
    cont = 0
    for i in data:
        cont += 1
        if username == i['username'] and check_password_hash(i['password'], password):
            session['username'] = username
            return redirect('/dashboard')
        if cont >= len(data):
            flash('Usuário ou senha inválidos')
            return redirect('/')

#-------------------------------------------------------------------------------------------------------------------------------------------#

@app.route('/register', methods=['POST'])
def register():
    userId = GetNextUserID()
    username = request.form.get('register-user')
    email = request.form.get('register-email')
    password = request.form.get('register-password')
    password_hash = generate_password_hash(password)
    user = [User(userId, username, email, password_hash)]
    with open('users.json') as json_file:
        data = json.load(json_file)
    for i in data:
        if i['username'] == username:
            flash('Usuário já existe, utilize outro')
            return redirect('/')
        elif i['username'] != username:
            new_user = data + user
    with open('users.json', 'w') as f:
        json.dump(new_user, f, indent=6)
    return redirect('/')

#-------------------------------------------------------------------------------------------------------------------------------------------#

@app.route('/dashboard')
def dashboard():
    if session['username']:
        contacts : dict
        with open('users.json') as json_file:
            data = json.load(json_file)
        for i in data:
            if i['username'] == session['username']:
                contacts = i['contacts']
        return render_template('dashboard.html', username = session['username'], contacts = contacts)
    else:
        return redirect('/')

#-------------------------------------------------------------------------------------------------------------------------------------------#

@app.route('/logout')
def logout():
    session['username'] = None
    return redirect('/')

#-------------------------------------------------------------------------------------------------------------------------------------------#

@app.route('/createContact', methods=['GET', 'POST'])
def createContact():
    name = request.form.get('contact-name')
    email = request.form.get('contact-email')
    phone = request.form.get('contact-phone')
    contact = Contact(name, email, phone)
    with open ('users.json') as json_file:
        data = json.load(json_file)
    for i in data:
        if i['username'] == session['username']:
            temp = i['contacts']
            temp.append(contact)
    with open('users.json', 'w') as f:
        json.dump(data, f, indent=5)
    
    return redirect('/dashboard')        

#-------------------------------------------------------------------------------------------------------------------------------------------#

@app.route('/deleteContact', methods=['GET', 'POST', 'DELETE'])
def deleteContact():
    selected_contact = request.form.get('contact-name')
    with open('users.json') as json_file:
        data = json.load(json_file)
    for i in data:
        if i['username'] == session['username']:
            temp = i['contacts']
    cont = 0
    for k in temp:
        cont += 1
        if k['name'] == selected_contact:
            cont -= 1
            del temp[cont]

    with open('users.json', 'w') as f:
        json.dump(data, f, indent=5)
    return redirect('/dashboard')

#-------------------------------------------------------------------------------------------------------------------------------------------#

@app.route('/updateContact', methods=['GET', 'POST', 'PUT'])
def updateContact():
    selected_contact = request.form.get('contact-name-selected')
    name = request.form.get('contact-name')
    email = request.form.get('contact-email')
    phone = request.form.get('contact-phone')
    with open('users.json') as json_file:
        data = json.load(json_file)
    for i in data:
        if i['username'] == session['username']:
            temp = i.get('contacts')
    for k in temp:
        if k['name'] == selected_contact:
            k['name'] = name
            k['email'] = email
            k['phone'] = phone
    with open('users.json', 'w') as f:
        json.dump(data, f, indent=5)
        return redirect('/dashboard')

#-------------------------------------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run()