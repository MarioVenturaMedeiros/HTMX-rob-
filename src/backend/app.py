from flask import Flask, request, jsonify, render_template, render_template_string
from flask_cors import CORS
from robo import InteliArm
from serial.tools import list_ports
from tinydb import TinyDB, Query
import os

app = Flask(__name__, template_folder='../templates')
CORS(app)

Robo = InteliArm()

# Get the directory path of the current Python script
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'logs.json')

# Create the database
db = TinyDB(db_path)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/log', methods=['GET'])
def log():
    return render_template('log.html')


@app.route('/get_logs', methods=['GET'])
def get_logs():
    logs = db.all()
    return logs
    #return render_template("log.html",logs=logs)


@app.route('/ports', methods=['GET'])
def get_ports():
    ports = list_ports.comports()
    if ports:
        buttons = ''.join([
            f'<button hx-post="/connect" hx-vals=\'{{"port": "{port.device}"}}\' hx-target="#controls" hx-swap="outerHTML">{port.device}</button>'
            for port in ports
        ])
        return buttons
    else:
        return "<div id='error'>Não está conectado ao robô</div>"


@app.route('/connect', methods=['POST'])
def connect():
    try:
        # Assuming the port is sent as form data
        port = request.form.get('port')
        if not port:
            return "<div id='error'>Porta não especificada.</div>", 400

        # Attempt to connect to the specified port
        if Robo.conectar_porta(port):
            # If the connection is successful, you can return success message or the next steps
            return render_template_string("""
                <div>Conectado ao robô com sucesso!</div>
                <!-- Your success logic here -->
            """)
        else:
            # If conectar_porta returns False, it means the connection attempt failed
            # Changed status code to 200 for client-side handling
            return "<div id='error'>Não está conectado ao robô</div>", 200
    except Exception as e:
        # If an exception is caught, return an error message
        # Optional: log the error for debugging purposes
        print(f"Failed to connect to port {port}: {str(e)}")
        return "<div id='error'>Não está conectado ao robô</div>", 200


@app.route('/movej', methods=['POST'])
def movej():
    data = request.json
    x = float(data.get('x', 0))
    y = float(data.get('y', 0))
    z = float(data.get('z', 0))
    r = float(data.get('r', 0))
    Robo.movej_to(x, y, z, r)
    return jsonify({"message": "Moved using movej"})


if __name__ == '__main__':
    app.run(port=8000, debug=True)
