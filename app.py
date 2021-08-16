from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'prod':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:a.yuvAc*@localhost/loginAppSecond'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://qoxgvaniitknjb:2b0618f540cdb4986f43f138545490b469ca379f9cf35f961ad1826fea7cd487@ec2-44-196-250-191.compute-1.amazonaws.com:5432/ddk764gsjtnc6c' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class loginInfo(db.Model):
    __tablename__ = 'loginInfo'
    email = db.Column(db.String(200), primary_key=True)
    password = db.Column(db.String(200))
    dateOfBirth = db.Column(db.DateTime(200))
    hobby = db.Column(db.String(200))
    color = db.Column(db.String(200))

    def __init__(self, email, password, dateOfBirth, hobby, color):
        self.email = email
        self.password = password
        self.dateOfBirth = dateOfBirth
        self.hobby = hobby
        self.color = color


@app.route('/loggedin', methods=['POST'])
def loggedIn():
    email = request.form['email']
    password = request.form['password']
    user = loginInfo.query.filter_by(email=email, password=password).first()
    if user == None:
        return render_template('login.html', message='You have entered the worng username or password')
    return render_template('loggedIn.html', user=user)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signUp.html')

@app.route('/createaccount', methods=['POST'])
def createaccount():
    email = request.form['email']
    password = request.form['password']
    dateOfBirth = request.form['dateOfBirth']
    hobby = request.form['hobby']
    color = request.form['color']
    if db.session.query(loginInfo).filter(loginInfo.email == email).count() == 0:
        data = loginInfo(email, password, dateOfBirth, hobby, color)
        db.session.add(data)
        db.session.commit()
        return render_template('login.html', message='Your account has been created sucsessfuly')
    return render_template('signUp.html', message='That email is already taken')

if __name__ == '__main__':
    app.run()