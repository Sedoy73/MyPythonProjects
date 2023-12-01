from datetime import date
from typing import Optional
import psycopg2
from psycopg2 import Date, sql
from fastapi import FastAPI, Form
from pydantic import BaseModel  # , validator, root_validator
from fastapi.responses import HTMLResponse, RedirectResponse

# from fastapi import Depends

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


class PersonFind(BaseModel):
    ffirst_name: str
    flast_name: str
    faddress: str
    fbirthdate: date


class SortParams(BaseModel):
    sort_column: Optional[str] = None
    sort_order: Optional[str] = None


class SearchParams(BaseModel):
    ffirst_name: Optional[str] = None
    flast_name: Optional[str] = None
    faddress: Optional[str] = None
    # fbirthdate: Optional[Date] = None


def create_connection():
    connection = psycopg2.connect(**db_params)
    return connection


@app.get("/get_people")
def get_people(sort_params: SortParams, searchParams: SearchParams):
    connection = create_connection()
    cursor = connection.cursor()

    sort_column = sort_params.sort_column
    sort_order = sort_params.sort_order

    ffirst_name = searchParams.ffirst_name
    flast_name = searchParams.flast_name
    faddress = searchParams.faddress

    '''
    if ffirst_name!='None':
        select_query = f"SELECT * FROM staff WHERE first_name iLIKE '%{ffirst_name}%';"
    elif flast_name !='None':
        select_query = f"SELECT * FROM staff WHERE flast_name iLIKE '%{flast_name}%';"
    elif faddress !='None':
        select_query = f"SELECT * FROM staff WHERE faddress iLIKE '%{faddress}%';"       
    elif ffirst_name !='None' and flast_name !='None' and faddress !='None':
        select_query = f"""SELECT * FROM staff WHERE first_name iLIKE '%{ffirst_name}%'
        AND flast_name iLIKE '%{flast_name}%'
        AND faddress iLIKE '%{faddress}%';"""'''

    # elif sort_column!='None' and sort_order!='None':
    # select_query = f"SELECT * FROM staff ORDER BY {sort_column} {sort_order};"

    if (
        sort_column == "staff_id"
        and sort_order == "asc"
        and ffirst_name == None
        and flast_name == None
        and faddress == None
    ):
        select_query = "SELECT * FROM staff ORDER BY staff_id;"
    elif ffirst_name != None:
        select_query = f"SELECT * FROM staff WHERE first_name iLIKE '%{ffirst_name}%' AND last_name iLIKE '%{flast_name}%' AND address iLIKE '%{faddress}%';"

    cursor.execute(select_query)
    people = cursor.fetchall()

    cursor.close()
    connection.close()

    return people


@app.get("/", response_class=HTMLResponse)
async def main(
    ffirst_name: str | None = None,
    flast_name: str | None = None,
    faddress: str | None = None,
):
    return root("staff_id", "asc", ffirst_name, flast_name, faddress)


@app.get(
    "/{sort_column}/{sort_order}/{ffirst_name}/{flast_name}/{faddress}",
    response_class=HTMLResponse,
)
def root(
    sort_column,
    sort_order,
    ffirst_name: str | None = None,
    flast_name: str | None = None,
    faddress: str | None = None,
):
    sortParams = SortParams()
    sortParams.sort_column = sort_column
    sortParams.sort_order = sort_order

    searchParams = SearchParams()
    searchParams.ffirst_name = ffirst_name
    searchParams.flast_name = flast_name
    searchParams.faddress = faddress

    """print(ffirst_name)
    print(flast_name)
    print(faddress)"""

    people = get_people(sortParams, searchParams)

    print(sort_column)
    print(sort_order)
    print(ffirst_name)
    print(flast_name)
    print(faddress)

    fields = ["first_name", "last_name", "address", "birthdate"]
    sort = sort_order

    result = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title><Program></title>
</head>
<body>
    <h2>Поиск сотрудников</h2>
    <form action="/" method="get">
          <table border="1" bordercolor="grey">
           <tr>
                 <th>Имя</th>
                 <th>Фамилия</th>
                 <th>Адрес</th>
                 <th>Действие</th>
           </tr>
           <tr>
                <td> <input type="text" id="ffirst_name" name="ffirst_name"></td>
                <td> <input type="text" id="flast_name" name="flast_name"></td>
                <td> <input type="text" id="faddress" name="faddress"></td>
                <td><button name="fbtn" type='submit'>Поиск</button><button type='reset'>Сброс</button></td>
            </tr>
          </table>       
    </form>

    <h2>Таблица данных сотрудников</h2>
         </style>
         </head> 
         <body>
          <table border="1" bordercolor="grey">
    """

    result = (
        result
        + f"""<tr><th><a href='http://127.0.0.1:8000/{fields[0]}/{"desc" if sort_column== fields[0] and sort == "asc" else "asc"}'>Имя</a></th>
                 <th><a href='http://127.0.0.1:8000/{fields[1]}/{"desc" if sort_column== fields[1] and sort == "asc" else "asc"}/{ffirst_name}/{flast_name}/{faddress}'>Фамилия</a></th>
                 <th><a href='http://127.0.0.1:8000/{fields[2]}/{"desc" if sort_column== fields[2] and sort == "asc" else "asc"}/{ffirst_name}/{flast_name}/{faddress}'>Адрес</a></th>
                 <th><a href='http://127.0.0.1:8000/{fields[3]}/{"desc" if sort_column== fields[3] and sort == "asc" else "asc"}/{ffirst_name}/{flast_name}/{faddress}'>Дата рождения</a></th>
                <th>Действие</th>
            </tr>"""
    )

    for p in people:
        if p[4]:
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
            + "<td><form action='/change_person/"
            + str(p[0])
            + "' method='post'><button type='submit'>Редактировать</button></form><form action='/del_person/"
            + str(p[0])
            + "' method='post'><button type='submit'>Удалить</button></form></td></tr>"
        )
    result = (
        result
        + """
          </table>
          <p></p>

    <h2>Добавление сотрудников</h2>
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
                <td> <input type="date" id="wbirthdate" name="wbirthdate" required></td>
                <td><button name="badd" type='submit'>Добавить</button></td>
            </tr>
          </table>       
    </form>
</body>
</html>"""
    )

    return HTMLResponse(content=result, status_code=200)


"""def get_person(staff_id):
    connection = create_connection()
    cursor = connection.cursor()

    select_query = "SELECT * FROM staff where staff_id = " + str(staff_id) + ";"

    cursor.execute(select_query)
    person = cursor.fetchall()

    cursor.close()
    connection.close()

    return person
"""


@app.post("/add_person")
def add_person(
    wfirst_name: str = Form(...),
    wlast_name: str = Form(...),
    waddress: str = Form(...),
    wbirthdate: date = Form(...),
):
    connection = create_connection()
    cursor = connection.cursor()

    insert_query = sql.SQL(
        """
        INSERT INTO staff (first_name, last_name, address, birthdate)
        VALUES (%s, %s, %s, %s);
        """
    )

    cursor.execute(
        insert_query,
        (wfirst_name, wlast_name, waddress, wbirthdate),
    )

    connection.commit()
    cursor.close()
    connection.close()
    response = RedirectResponse("/", status_code=303)
    return response


@app.post("/del_person/{staff_id}")
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
    response = RedirectResponse("/", status_code=303)
    return response


@app.post("/edit_person/{staff_id}")
def edit_people(
    staff_id,
    ufirst_name: str = Form(...),
    ulast_name: str = Form(...),
    uaddress: str = Form(...),
    ubirthdate: date = Form(...),
):
    connection = create_connection()
    cursor = connection.cursor()

    update_query = sql.SQL(
        f"UPDATE staff "
        f"SET first_name = '{ufirst_name}', last_name = '{ulast_name}', address = '{uaddress}', birthdate = '{ubirthdate}' "
        f"WHERE staff_id = {staff_id};"
    )
    cursor.execute(
        update_query,
        (ufirst_name, ulast_name, uaddress, ubirthdate),
    )

    connection.commit()
    cursor.close()
    connection.close()
    response = RedirectResponse("/", status_code=303)
    return response


@app.post("/change_person/{staff_id}", response_class=HTMLResponse)
def change_person(staff_id):
    person = get_person(staff_id)
    print(person)
    print(person[0][3])
    result = (
        f"<!DOCTYPE html>"
        f"<html lang='en'>"
        f"<head>"
        f"<meta charset='UTF-8'>"
        f"<title><Program></title>"
        f"</head>"
        f"<body>"
        f"<h2>Редактирование данных сотрудника</h2>"
        f" </style>"
        f" </head> "
        f" <body>"
        f"  <table border='1' bordercolor='grey'>"
        f" <form action='/edit_person/{staff_id}' method='post'>"
        f" <table border='1' bordercolor='grey'>"
        f"   <tr>"
        f"   <th>Имя</th>"
        f"   <th>Фамилия</th>"
        f"   <th>Адрес</th>"
        f"   <th>Дата рождения</th>"
        f"   <th>Действие</th>"
        f" </tr>"
        f" <tr>"
        f" <td> <input type='text' value='{person[0][1]}' id='ufirst_name' name='ufirst_name' required></td>"
        f" <td> <input type='text' value='{person[0][2]}' id='ulast_name' name='ulast_name' required></td>"
        f"<td> <input type='text' value='{person[0][3]}' id='uaddress' name='uaddress' required></td>"
        f"<td> <input type='date' value='{person[0][4]}' id='ubirthdate' name='ubirthdate' required></td>"
        f" <td><button name='uadd' type='submit'>Подтвердить изменения</button></td></tr></table></form>"
    )
    return HTMLResponse(content=result, status_code=200)


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


@app.get("/find_person")
def find_person(searchParams: SearchParams):
    connection = create_connection()
    cursor = connection.cursor()

    ffirst_name = searchParams.ffirst_name
    flast_name = searchParams.flast_name
    faddress = searchParams.faddress

    print ('Find person' + ffirst_name)
    print (flast_name)
    print (faddress)
    

    if ffirst_name!='None':
        select_query = f"SELECT * FROM staff WHERE first_name iLIKE '%{ffirst_name}%';"
    elif flast_name !='None':
        select_query = f"SELECT * FROM staff WHERE flast_name iLIKE '%{flast_name}%';"
    elif faddress !='None':
        select_query = f"SELECT * FROM staff WHERE faddress iLIKE '%{faddress}%';"       
    elif ffirst_name !='None' and flast_name !='None' and faddress !='None':
        select_query = f"""SELECT * FROM staff WHERE first_name iLIKE '%{ffirst_name}%'
        AND flast_name iLIKE '%{flast_name}%'
        AND faddress iLIKE '%{faddress}%';"""
    
    cursor.execute(select_query)

    cursor.close()
    connection.close()

    return person

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
