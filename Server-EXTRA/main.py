import argparse
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/run_command', methods=['POST'])
def run_command():

    #получаем информацию из тела
    email = request.json.get('email')
    command = request.json.get('command')

    #проверка почты
    if not email:
        return jsonify({'error': 'Email is missing'}), 400
    
    #проверка команды
    if not command:
        return jsonify({'error': 'Command is missing'}), 400

    #сформируем команду
    command_insert = f'{command} {email}'

    #пробуем запустить команду
    try:
        result = subprocess.run(command_insert.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10)
        return jsonify({'output': result.stdout.decode('utf-8').strip()})
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command execution timed out'}), 500
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.output.decode('utf-8').strip()}), 500

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080, help="Port number")
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port)
