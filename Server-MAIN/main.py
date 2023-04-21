from services import *
import threading
import requests
import os
import csv
import paramiko

#получаем все входные даные
servers = read_file("servers.txt")
mails = split_file("mails.txt", len(servers))


#генерируем меню запуска
menu_start(servers, mails)
client_input = input("$ ")

if client_input == "1":
    send_commands(servers, mails)

if client_input == "2":
    clear_temp_folder()

if client_input == "3":
    create_token_table()

if client_input == "4":
    ip = input("$ssh (ip) -> ")
    user = input("$ssh (login) -> ")
    passw = input("$ssh (password) -> ")
    cooki = input("$ssh (куки) -> ")

    # Подключение к удаленному серверу по SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=user, password=passw)

    # Выполнение команды на удаленном сервере
    stdin, stdout, stderr = ssh.exec_command('pipx run ghunt login')

    # Ожидание ввода "2"
    stdin.write('2\n')
    stdin.flush()

    # Ввод значения cooki
    
    stdin.write(cooki + '\n')
    stdin.flush()

    # Закрытие подключения
    ssh.close()

    print(f"⛓Изменения успешно внесены на сервер {ip}:5000")



