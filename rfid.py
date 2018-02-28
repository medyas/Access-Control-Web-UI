import os, requests, json, classes, datetime
from flask import Flask, request, session, redirect, render_template, url_for, send_from_directory, make_response
import flask_login

# database connection
db = classes.dataBase()

# app init
app = Flask(__name__)

# app config
app.config.update(
    DEBUG=True,
    SECRET_KEY=os.urandom(1024),
    SESSION_REFRESH_EACH_REQUEST=False,
    PERMANENT_SESSION_LIFETIME=datetime.timedelta(hours=1)
)


#login_manager = flask_login.LoginManager()
#login_manager.init_app(app)

# find cookie
def checkCookie():
    if(request.cookies.get('username')):
        session['username'] = request.cookies.get('username')
        session['id'] = request.cookies.get('id')
        return True
    else:
        return False

# index-login page
@app.route('/')
def index():
    if not session and not checkCookie():
        return render_template('index.html')
    else:
        return redirect(url_for('dashboard'))

# login url
@app.route('/login/', methods=['POST',  'GET'])
def login():
    if request.method == 'POST':
        status, data = db.checkUser(request.form['username'].lower())
        if(status):
            if(request.form['password'] == data[5]):
                session['username'] = request.form['username'].lower()
                session['id'] = data[0]
                resp = make_response(url_for('dashboard'))
                resp.set_cookie('username', session['username'])
                resp.set_cookie('id', str(session['id']))
                return resp
            else:
                return "error"
        else:
            return "error"
    else:
        return redirect(url_for('index'))

# dashboard page
@app.route('/dashboard/', methods=['POST',  'GET'])
def dashboard():
    if not session and not checkCookie():
        return redirect(url_for('index'))
    else:
        if(request.method == 'GET'):
            return render_template('header.html') + render_template('dashboard.html') + render_template('footer.html')
        else:
            status, data = db.employeesLogs()
            if(status):
                return json.dumps(data)
            else:
                return ""

# about page
@app.route('/about/')
def about():
    if not session and not checkCookie():
        return redirect(url_for('index'))
    else:
        return render_template('header.html') + render_template('about.html') + render_template('footer.html')

# contact page
@app.route('/conctact/')
def contact():
    if not session and not checkCookie():
        return redirect(url_for('index'))
    else:
        return render_template('header.html') + render_template('contact.html') + render_template('footer.html')

@app.route('/settings/', methods=['POST',  'GET'])
def settings():
    if not session and not checkCookie():
        return redirect(url_for('index'))
    else:
        return render_template('header.html') + render_template('settings.html') + render_template('footer.html')


# add user page
@app.route('/adduser/', methods=['POST',  'GET'])
def adduser():
    if not session and not checkCookie():
        return redirect(url_for('index'))
    else:
        if(request.method == 'GET'):
            return render_template('header.html') + render_template('adduser.html') + render_template('footer.html')
        else:
            status, msg = db.addUser(request.form['firstname'], request.form['lastname'], request.form['username'], request.form['password'], request.form['email']request.form['edit']request.form['add']request.form['block'], request.form['delete'])
            if(status):
                data = {
                        'status': status,
                        'msg': msg,
                        'class': 'alert-success'
                    }
                return json.dumps(data)
            else:
                data = {
                        'status': status,
                        'msg': msg,
                        'class': 'alert-danger'
                    }
                return json.dumps(data)

# add employee page
@app.route('/addemployee/', methods=['POST',  'GET'])
def addemployee():
    if not session and not checkCookie():
        return redirect(url_for('index'))
    else:
        if(request.method == 'GET'):
            return render_template('header.html') + render_template('addemployee.html') + render_template('footer.html')
        else:
            status, data = db.employeesLogs()
            if(status):
                return json.dumps(data)
            else:
                return ""

# bloock employee page
@app.route('/block/', methods=['POST',  'GET'])
def block():
    if not session and not checkCookie():
        return redirect(url_for('index'))
    else:
        if(request.method == 'GET'):
            return render_template('header.html') + render_template('block.html') + render_template('footer.html')
        else:
            status, data = db.employeesLogs()
            if(status):
                return json.dumps(data)
            else:
                return ""

# delete user page
@app.route('/deleteuser/', methods=['POST',  'GET'])
def deleteuser():
    if not session and not checkCookie():
        return redirect(url_for('index'))
    else:
        if(request.method == 'GET'):
            return render_template('header.html') + render_template('deleteuser.html') + render_template('footer.html')
        else:
            status, data = db.employeesLogs()
            if(status):
                return json.dumps(data)
            else:
                return ""

# delete employee page
@app.route('/deleteemployee/', methods=['POST',  'GET'])
def deleteemployee():
    if not session and not checkCookie():
        return redirect(url_for('index'))
    else:
        return render_template('header.html') + render_template('deleteemployee.html') + render_template('footer.html')


# logout page
@app.route('/logout/')
def logout():
    if not session and not checkCookie():
        return redirect(url_for('index'))
    else:
        session.pop('username', None)
        session.pop('id', None)
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('username', '', expires=0)
        resp.set_cookie('id',  '', expires=0)
        return resp

# 404 not found page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html') 



# match the string to employee name
@app.route('/findemployee/<string>')
def findemployee(string=""):
    if not session and not checkCookie():
        return redirect(url_for('index'))
    else:
        if(string == ""):
            return ""
        status, data = db.findEmployee(string)
        if(status):
            return json.dumps(data)
        else:
            return ""

# find employee by uid
@app.route('/employee=<uid>')
def employee(uid=""):
    if not session and not checkCookie():
        return redirect(url_for('index'))
    else:
        status, emData = db.employee(uid)
        if(status and emData!=None):
            status, logsData = db.employeeLogs(uid)
            temp = {
                    'employee':emData,
                    'logs': logsData
                }
            return json.dumps(temp)
        else:
            return ''


if __name__ == '__main__':
    app.run()
