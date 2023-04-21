import threading
import requests
import time
import os
import json




def send_command(server, email_list):
    '''
    обработчик для каждого сервера
    
    '''
    if not os.path.exists("temp/" + server):

        os.makedirs("temp/" + server)
        print("🌐 Сервер зарегестрирован!")
    else:
        print("🌐 Сервер уже был зарегестрирова!")

    

    for i in range(len(email_list)):
        start_time = time.time()


        command = {
            'command': 'pipx run ghunt email',
            'email': email_list[i]
        }
        url = f'http://{server}/run_command'

        response = requests.post(url, json=command)

        filename = f"temp/{server}/{email_list[i]}.txt"

        with open(filename, 'w') as f:
            f.write(response.text)


        end_time = time.time()
        speed = len(email_list) / (end_time - start_time)


        data = response.json()
        #print(data)
        if "error" in data:    
            print(f"💠Сервер: {server} обработал {email_list[i]} за: {speed:.2f} сек | 🔥 СЕРВЕР РАБОТАЕТ НЕ КОРЕКТНО")
        else:
            print(f"💠Сервер: {server} обработал {email_list[i]} за: {speed:.2f} сек ")
    
    
def send_commands(servers, emails):
    '''
    Запускатор потоков для серверов
    '''
    threads = []
    for i, server in enumerate(servers):
        t = threading.Thread(target=send_command, args=(server, emails[i]))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()