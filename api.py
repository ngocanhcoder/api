
#uvicorn api:app --reload

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from flask import Flask
import json
import random
import string
app = FastAPI()

def load_data(filename='data.json'):
    with open(filename, 'r') as file:
        return json.load(file)
def add_data_to_file(new_data, filename='data.json'):
    # lấy dữ liệu file json
    existing_data = load_data(filename)
    # lọc trùng tài khoản
    def is_duplicate(entry):
        return entry.get('api_key') == new_data['api_key'] or entry.get('user') == new_data['user']
    if any(is_duplicate(entry) for entry in existing_data):
        return 0  
    # lưu tài khoản
    existing_data.append(new_data)
    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=2)
    return True  
def generate_random_api():
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for _ in range(30))  # Độ dài là 30
    return random_string







class TaskManager:
    def __init__(self):
        ...
    def main(self):
        return {'message':'welcome','admin':'Na Software','Zalo':'0363333490'}
    
    def login(self, api_key:str):
        data = load_data()
        for entry in data:
            if entry.get('api_key') == api_key:
                return {'status': True, 'user': entry.get('user')}
        return {'status': False, 'user': None}
    
    def add_key(self,user:str):
        key = generate_random_api()
        new_entry = {"api_key": key, "user": user}
        add = add_data_to_file(new_entry, 'data.json')
        if add  != False:
            return {'status':True,'message':'Thêm tài khoản thành công','data': {'api_key':key,'User':user}}
        if add == 0:
            return {'status':False,'message':'Đã tồn tại tài khoản trong hệ thống!'}
        return {'status':False,'message':'Thêm tài thất bại'}
    



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

task_manager = TaskManager()


app = Flask(__name__)
@app.get('/')
def main():
    return task_manager.main()
@app.get("/login/api_key={api_key}")
def login(api_key:str):
    return task_manager.login(api_key)

@app.get("/signin/user={user}")
def add_key(user:str):
    return task_manager.add_key(user)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)