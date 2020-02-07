from datetime import date , datetime
from pyfirmata import Arduino, util
import time

def valor_pin(pin ,numAmostras):
    pin_total = 0
    for i in range(0,numAmostras):        
        time.sleep(0.1)
        pin_total = pin_total + pin.read()    
    return pin_total/numAmostras

def dayBr():
    now = datetime.now()
    return now.strftime("%d-%m-%Y")
def hour():
    return datetime.now().strftime('%H:%M')

def getDados():
    
    const = {
            'sbr_tensao' :240.00,
            'sob_tensao_110v': 86.00,
            'sob_tensao_220v': 178.00,
            'limiar_sup': 130.9,    #298.00
            'limiar_inf': 21.08,     #48.00
            'parametro_110v': 0.95,  #0.42
            'parametro_220v': 0.67  #0.30
    }

    return const
