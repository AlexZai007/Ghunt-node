import os
import shutil
import re
import os
import csv


def split_file(filename, num_arrays):
    '''
    Метод для распределния информации из файла по масивам
    '''
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    num_lines = len(lines)
    lines_per_array = num_lines // num_arrays
    remainder = num_lines % num_arrays
    result = []
    start = 0
    for i in range(num_arrays):
        end = start + lines_per_array
        if i < remainder:
            end += 1
        result.append(lines[start:end])
        start = end
    return result


def read_file(filename):
    """
    Читайем файл построчно и возращаем масивом
    """
    with open(filename, 'r') as f:
        lines = [line.rstrip() for line in f]
    return lines



def create_token_table():
    '''
    Создаем сводную таблицу
    '''
    folder = 'temp'
    csv_file = 'token_table.csv'
    headers = ['Server', 'Email', 'Token']
    
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        
        for server in os.listdir(folder):
            server_folder = os.path.join(folder, server)
            for file_name in os.listdir(server_folder):
                if file_name.endswith('.txt'):
                    email = file_name[:-4]  # убираем расширение .txt
                    file_path = os.path.join(server_folder, file_name)
                    with open(file_path, mode='r') as token_file:
                        token = token_file.read().strip()        
                    writer.writerow([server, email, token])
                    

def clear_temp_folder():

    '''
    Подчищаем файлы из папки temp
    '''

    folder = 'temp'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): 
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    