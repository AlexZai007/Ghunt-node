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

        output = subprocess.check_output(command_insert.split(), stderr=subprocess.STDOUT)
        return jsonify({'output': output.decode('utf-8').strip()})
    
    except subprocess.CalledProcessError as e:
        
        return jsonify({'error': e.output.decode('utf-8').strip()}), 500

if __name__ == '__main__':
    app.run()
