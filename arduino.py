from flask import Flask, request, redirect, url_for, render_template,session
from pyfirmata import Arduino, util
import time
from functiontest import valor_pin, dayBr, hour, getDados
from flask_sqlalchemy import SQLAlchemy
from models import db,Leitura, User
from flask_migrate import Migrate
global last


global last
app = Flask(__name__, template_folder= "templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BD_test.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "123456"
db = SQLAlchemy(app)
migrate= Migrate(app,db)

@app.route('/login',methods=["POST","GET"])
def login():
    user_id = None
    if 'username' and 'password' in request.form:
        user = User(request.form['username'],request.form['password'])
        for u in User.query.all():
            if user.username == u.username and user.password == u.password:
                session['user'] = u.id
                
    if session.get('user'):
        
        
        return redirect(url_for("index")) 

    return render_template("login.html", User = User, user_id = session.get('user'))

@app.route('/logout', methods=['POST','GET'])
def logout():
    session.pop('user')
    return redirect(url_for("login"))
@app.route('/',methods=["POST","GET"])

def index():

    return render_template("index.html",constantes=constantes)

@app.route('/log',methods = ["POST", "GET"])
def log():
    daylog = request.form["data"][-2:]+request.form["data"][4:8]+request.form["data"][:4]

    leituralog = Leitura.query.filter(Leitura.dia==daylog)
    faltaslog =  Leitura.query.filter(Leitura.dia==daylog,Leitura.falta_t==True)
    sobrelog = Leitura.query.filter(Leitura.dia==daylog,Leitura.sobre_t==True)
    context={
                'leituralog': leituralog,
                'faltaslog' : faltaslog,
                'sobrelog' :  sobrelog,
                'first' : leituralog[0].id,
                'dia' : daylog
            }

    return render_template("logdb.html", context=context)
@app.route('/start', methods = ["POST","GET"])
def start():
    if not session.get('user'):
        return redirect(url_for("login"))
    else :
        time.sleep(2) 
        dic = dict(request.form)
        global last   

        for const in dic :
            if dic[const] != '' :
                constantes[const] = float(dic[const])

        dia = dayBr()
        horas = hour()
        print(constantes)
        if request.method == 'POST':
        
            
            last = Leitura.query.all()[-1].id
            
            
        vl_pin0 = pin0.read()*1000

        if (vl_pin0 < constantes['limiar_sup']) and (vl_pin0 > constantes['limiar_inf']):
    
            print("Energia esta em 110v.")
            status ='110v'
            tensao = vl_pin0*constantes['parametro_110v']
            sob_tensao = constantes['sob_tensao_110v']
            
        else:        
            status= '220v'
            print("Energia esta em 220v.")
            tensao = vl_pin0* constantes['parametro_220v']
            sob_tensao = constantes['sob_tensao_220v']
        
        tensao = round(tensao,2)     
        print(f'Monitorando Energia... {tensao}v')

        if (tensao >= constantes['sbr_tensao']):

            print("Sobre Tensao...")

            db.session.add(Leitura(dia,horas,status,tensao,False,True))
            db.session.commit()
            return "Sobre Tensão!"
            
        if tensao == 0.00:

            print("Faltou Energia...")

            db.session.add(Leitura(dia,horas,status,tensao,True,False))
            db.session.commit()
        
        else:

            db.session.add(Leitura(dia,horas,status,tensao,False,False))
            db.session.commit()
            if (tensao <= sob_tensao):

                print("Queda de Energia...")

        #log.close()
        #placa.exit()
        leituras = Leitura.query.all()[last:]
        
        return render_template("reading.html", leituras=leituras,constantes=constantes )


if __name__ == "__main__":
    print("Iniciando..")
    constantes = getDados()

    placa = Arduino('/dev/ttyUSB0')
    it = util.Iterator(placa)
    it.start()

    sob_tensao = 178.00
    
    pin0 = placa.get_pin('a:0:i') 
    time.sleep(2)
    
    db.init_app(app=app)
    app.run(debug = True)
    
