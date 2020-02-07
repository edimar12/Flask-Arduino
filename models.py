from flask_sqlalchemy import SQLAlchemy
from flask import Flask , session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BD_test.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column('id',db.Integer, primary_key=True, autoincrement = True)
    username = db.Column(db.String,unique= True)
    password = db.Column(db.String)
    def __init__(self, username,password):
        self.username = username
        self.password = password
 
class Leitura(db.Model):
    id = db.Column('id',db.Integer, primary_key=True, autoincrement = True)
    dia = db.Column(db.String)
    horas = db.Column(db.String)
    status= db.Column(db.String)
    tensao = db.Column(db.Float)
    falta_t = db.Column(db.Boolean)
    sobre_t = db.Column(db.Boolean)
    def __init__(self, dia,horas,status, tensao,falta_t,sobre_t):
        self.dia = dia
        self.horas = horas
        self.status = status
        self.tensao = tensao
        self.falta_t = falta_t
        self.sobre_t = sobre_t



if __name__ == "__main__":
    
    db.create_all()
    db.session.add(Leitura('dia','horas','status',123,False,False))
    db.session.commit()