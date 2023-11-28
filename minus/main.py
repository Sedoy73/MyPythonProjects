from fastapi import FastAPI
from datetime import date

app = FastAPI ()


@app.get("/")
async def hello():
    return "Staff list"

'''@app.post("/add-staff")
async def add_stuff (parameters: Stuff):
    print(f'Firstname:{first_name}')
    print(f'Lastname:{last_name}')
    print(f'Address:{address}')
    print(f'Birthdate:{birthdate}')
    return 'user is added'

staff_dict = {}
staff_dict ['Firstname'] = parameters.first_name
'''