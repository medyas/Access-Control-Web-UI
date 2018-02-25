import os, requests, json, classes, datetime
from flask import Flask, request, session, redirect, render_template, url_for, send_from_directory


db = classes.dataBase()

app = Flask(__name__)

@app.route('/')
def index():
    if not session:
        return render_template('index.html')
    else:
        return redirect(url_for('dashboard'))

@app.route('/login/', methods=['POST',  'GET'])
def login():
    if request.method == 'POST':
        status, data = db.checkUser(request.form['username'])
        if(status):
            if(request.form['password'] == data[5]):
                session['username'] = request.form['username']
                session['id'] = data[0]
                return url_for('dashboard')
            else:
                return "error"
        else:
            return "error"
    else:
        return redirect(url_for('index'))

@app.route('/dashboard/', methods=['POST',  'GET'])
def dashboard():
    if not session:
        return redirect(url_for('index'))
    else:
        return render_template('header.html') + render_template('dashboard.html') + render_template('footer.html')

@app.route('/about/')
def about():
    if not session:
        return redirect(url_for('index'))
    else:
        return render_template('header.html') + render_template('about.html') + render_template('footer.html')

@app.route('/conctact/')
def contact():
    if not session:
        return redirect(url_for('index'))
    else:
        return render_template('header.html') + render_template('contact.html') + render_template('footer.html')

@app.route('/settings/')
def settings():
    if not session:
        return redirect(url_for('index'))
    else:
        return render_template('header.html') + render_template('settings.html') + render_template('footer.html')

@app.route('/logout/')
def logout():
    if not session:
        return redirect(url_for('index'))
    else:
        session.pop('username', None)
        return redirect(url_for('index'))

@app.route('/adduser/')
def adduser():
    if not session:
        return redirect(url_for('index'))
    else:
        return render_template('header.html') + render_template('adduser.html') + render_template('footer.html')

@app.route('/addemployee/')
def addemployee():
    if not session:
        return redirect(url_for('index'))
    else:
        return render_template('header.html') + render_template('addemployee.html') + render_template('footer.html')

@app.route('/block/')
def block():
    if not session:
        return redirect(url_for('index'))
    else:
        return render_template('header.html') + render_template('block.html') + render_template('footer.html')

@app.route('/deleteuser/')
def deleteuser():
    if not session:
        return redirect(url_for('index'))
    else:
        return render_template('header.html') + render_template('deleteuser.html') + render_template('footer.html')

@app.route('/deleteemployee/')
def deleteemployee():
    if not session:
        return redirect(url_for('index'))
    else:
        return render_template('header.html') + render_template('deleteemployee.html') + render_template('footer.html')


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))


app.secret_key = os.urandom(1024)

if __name__ == '__main__':
    app.run(debug=True)
