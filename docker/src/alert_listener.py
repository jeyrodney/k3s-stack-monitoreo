from flask import Flask, request, jsonify
from datetime import datetime
from python_webex.v1.Bot import Bot
import logging
import os
import sys

try:

    carpeta = os.getcwd()
    ruta= carpeta + '\\venv\\Temp\\Logs_alert_listener.log'
    logging.basicConfig(filename=ruta , encoding='utf-8', level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("Inicio del módulo alert_listener.py")

    #cargar token del bot de webex
    bot = Bot("M2JmYzZiMWItNjg5OS00NjRiLThhODItMTNlMmY2NzIyMzcwYTA2OWIyMTQtZTEw_PF84_34814e66-86b2-45a2-8e58-84e3ad385fe8")
    bot.send_message(room_id='d9516040-b5e2-11ef-ac38-274f3cc594ff', text = f"*****Se reinicia el Escuchador de Alertas*****")
    app = Flask(__name__)

    @app.route('/alert', methods=['POST'])
    def alert():
        data = request.get_json()
        alerts = data.get('alerts', [])
        for alert in alerts:
            #bot.send_message(room_id='d9516040-b5e2-11ef-ac38-274f3cc594ff', text = f"Validacion Alerta:\n {alert}")
            if (alert['status'] == 'resolved') and (alert['labels']['alertname'] == 'BranchDown'):
                descripcion = f"Alerta resuelta!: {alert['annotations']['description']}"
                emoji = "✅✅✅"
            elif (alert['status'] == 'firing') and (alert['labels']['alertname'] == 'BranchDown'):
                descripcion = alert['annotations']['description']
                emoji = "❗️❗️❗️❗️❗️"
            elif alert['labels']['alertname'] == 'HighLatency':
                descripcion = alert['annotations']['description']
                emoji = "🤔🤔🤔"
            elif (alert['labels']['alertname'] == 'HighPacketLoss'):
                descripcion = alert['annotations']['description']
                emoji = "📉📉📉📉"
            elif (alert['status'] == 'resolved') and (alert['labels']['alertname'] == 'AnomaliaRedSucursales'):
                descripcion = f"Sucursales Alertadas OK: se estabiliza la conectividad y no hay mas perdidas generales"
                emoji = "🔋🔋🔋🔋"
            elif (alert['labels']['alertname'] == 'AnomaliaRedSucursales'):
                descripcion = alert['annotations']['description']
                emoji = "📢😱😱😱🔥"
            else: 
                descripcion = f"Cayó el en ELSE: {alert['status']} {alert['labels']['severity']}"
                emoji = "indefinido"
                
            alertas = []
            alertas.append(f"\n{emoji}")
            if descripcion == "Sucursales Alertadas OK: se estabiliza la conectividad y no hay mas perdidas generales":
                alertas.append(f"ALERTA RESUELTA: Perdida de paquetes en varias sucursales")
            else:
                alertas.append(f"ALERTA: {alert['annotations']['summary']}")
            alertas.append(f"Descripción: {descripcion}")
            alertas.append(f"Severidad: {alert['labels']['severity']}")
            alertas.append(f"Hora Alerta: {datetime.now()}")
            alertas.append(f"{emoji}\n")
            mensaje = '\n'.join(alertas)
            #print(mensaje)
            #envio de la notificacion al espacio de Webex
            bot.send_message(room_id='d9516040-b5e2-11ef-ac38-274f3cc594ff', text = mensaje)
        return jsonify({"status": "received"}), 200

    if __name__ == '__main__':
        app.run(port=5000)
except Exception as e: 
        
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    error = ("ERROR en modulo "+str(fname)+", en la linea "+ str(exc_tb.tb_lineno)+": "+str(exc_type)+str(e))
    print (error)
    logging.error(error)
    bot.send_message(room_id='d9516040-b5e2-11ef-ac38-274f3cc594ff', text = "Error en módulo alert_listener, ver logs.")