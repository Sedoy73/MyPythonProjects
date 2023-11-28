from datetime import date
import psycopg2
from psycopg2 import sql
from fastapi import FastAPI
from pydantic import BaseModel, validator, root_validator
from fastapi.responses import HTMLResponse
from fastapi import Depends

app = FastAPI()

# данные для подключения к базе данных

db_params = {
    "database": "study",
    "user": "postgres",
    "password": "Ssde1100",
    "host": "127.0.0.1",
}


class PersonInput(BaseModel):
    wfirst_name: str
    wlast_name: str
    waddress: str
    wbirthdate: date


# Функция для создания подключения к базе данных
def create_connection():
    connection = psycopg2.connect(**db_params)
    return connection


@app.get("/")
async def root():
    people = get_people()
    result = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title><Program></title>
</head>
<body>
    <h2>Таблица данных сотрудников</h2>
         </style>
         </head> 
         <body>
          <table border="1" bordercolor="grey">
           <tr>
                <th>Имя</th>
                <th>Фамилия</th>
                <th>Адрес</th>
                <th>Дата рождения</th>
                <th>Действие</th>
            </tr>
"""
    for p in people:
        formatted_date = p[4].strftime("%d-%m-%Y")
        result = (
            result
            + "<tr><td>"
            + p[1]
            + "</td><td>"
            + p[2]
            + "</td><td>"
            + p[3]
            + "</td><td>"
            + formatted_date
            + "<td><button type='submit'>Редактировать</button><button type='submit'>Удалить</button></td></tr>"
        )
    result = (
        result
        + """
          </table>
          <p></p>
    <form action="/add_person" method="post">
          <table border="1" bordercolor="grey">
           <tr>
                 <th>Имя</th>
                 <th>Фамилия</th>
                 <th>Адрес</th>
                 <th>Дата рождения</th>
                 <th>Действие</th>
           </tr>
           <tr>
                <td> <input type="text" id="wfirst_name" name="wfirst_name" required></td>
                <td> <input type="text" id="wlast_name" name="wlast_name" required></td>
                <td> <input type="text" id="waddress" name="waddress" required></td>
                <td> <input type="text" id="wbirthdate" name="wbirthdate" required></td>
                <td><button name="badd" type='submit'>Добавить</button></td>
            </tr>
          </table>       
    </form>
</body>
</html>"""
    )
    return HTMLResponse(content=result, status_code=200)


# @app.get("/get_people")
def get_people():
    connection = create_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT * FROM staff ORDER BY staff_id;
    """

    cursor.execute(select_query)
    people = cursor.fetchall()

    cursor.close()
    connection.close()

    return people


@app.post("/add_person")
def add_person(person_data: PersonInput = Depends()):
    connection = create_connection()
    cursor = connection.cursor()
    print (person_data.wfirst_name)
    print (person_data.wlast_name)
    print (person_data.waddress)
    print (person_data.wbirthdate)

    insert_query = sql.SQL(
        """
        INSERT INTO staff (first_name, last_name, address, birthdate)
        VALUES ({wfirst_name}, {wlast_name}, {waddress}, {wbirthdate});
        """
    ).format(
        first_name=sql.Literal(person_data.wfirst_name),
        last_name=sql.Literal(person_data.wlast_name),
        address=sql.Literal(person_data.waddress),
        birthdate=sql.Literal(person_data.wbirthdate),
    )

    cursor.execute(insert_query)

    connection.commit()
    cursor.close()
    connection.close()


@app.post("/del_person")
def del_person(staff_id):
    connection = create_connection()
    cursor = connection.cursor()

    delete_query = """
        DELETE FROM staff WHERE staff_id = %s;
    """
    cursor.execute(delete_query, (staff_id,))
    connection.commit()
    cursor.close()
    connection.close()


def edit_people(staff_id, wfirst_name, wlast_name, waddress, wbirthdate):
    connection = create_connection()
    cursor = connection.cursor()

    update_query = sql.SQL(
        """
        UPDATE staff 
        SET first_name = {wfirst_name}, last_name = {wlast_name}, address = {waddress}, birthdate = {wbirthdate}
        WHERE staff_id = {staff_id};
    """
    ).format(
        wfirst_name=sql.Literal(wfirst_name),
        wlast_name=sql.Literal(wlast_name),
        waddress=sql.Literal(waddress),
        wbirthdate=sql.Literal(wbirthdate),
        staff_id=sql.Literal(staff_id),
    )

    cursor.execute(update_query)

    connection.commit()
    cursor.close()
    connection.close()


'''
class People (BaseModel):
    __tablename__ = "stuff"
    id = int
    first_name: str
    last_name: str
    address: str
    birthdate: date

    
# Пример использования
if __name__ == "__main__":
    connection = create_connection()
    cursor = connection.cursor()

    # Получение списка людей
    people_list = get_people()
    print("Список людей:")
    for person in people_list:
        print(person)

# Функция для получения списка людей
def get_people():
    connection = create_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT * FROM staff ORDER BY staff_id;
    """

    cursor.execute(select_query)
    people = cursor.fetchall()

    cursor.close()
    connection.close()

    return people

def create_table():
    connection = create_connection()
    cursor = connection.cursor()

    create_table_query = """
        CREATE TABLE IF NOT EXISTS people (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            birth_date DATE NOT NULL
        );
    """
    cursor.execute(create_table_query)

    connection.commit()
    cursor.close()
    connection.close()


# Функция для добавления человека в базу данных
def add_person(full_name, birth_date):
    connection = create_connection()
    cursor = connection.cursor()

    insert_query = sql.SQL(
        """
        INSERT INTO people (full_name, birth_date) 
        VALUES ({full_name}, {birth_date});
    """
    ).format(full_name=sql.Literal(full_name), birth_date=sql.Literal(birth_date))

    cursor.execute(insert_query)

    connection.commit()
    cursor.close()
    connection.close()
'''
