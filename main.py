import psycopg2
from config import db_name, user, password, host


conn = psycopg2.connect(
    database=db_name, 
    user=user, 
    password=password
)
conn.autocommit = True
cur = conn.cursor()

def Create_table(cursor): #Функция, создающая структуру БД (таблицы).
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS client (
    ID serial PRIMARY key,
    First_Name Varchar(60),
    Last_Name Varchar(60),
    email Char(20)
    );
    CREATE TABLE IF NOT EXISTS telephone (
    ID serial PRIMARY key,
    id_client integer REFERENCES client (ID),
    number char(15)
    );
    """)
    
def add_client(cursor, first_name, last_name, mail, *number): #Функция, позволяющая добавить нового клиента.
    cursor.execute("""
    INSERT INTO public.client (first_name, last_name, email)
    """, (first_name, last_name, mail))
    id_cl = cursor.fetchone()[0]
    #print(id_cl)
    if number:
        cursor.execute("""
        INSERT INTO public.telephone (id_client, number)
        VALUES (%s,%s);
        """, (id_cl, number))
    print('Данные добавлены')
    
def add_telephone(cursor, first_name, last_name, number): #Функция, позволяющая добавить телефон для существующего клиента.
    cursor.execute("""
    SELECT id
    FROM client
    WHERE first_name = %s and last_name = %s                  
    """, (first_name, last_name))
    id_cl = cursor.fetchone()
    if id_cl != None:
        cursor.execute("""
        INSERT INTO public.telephone (id_client, number)
        VALUES (%s,%s);
        """, (id_cl[0], number))
    print('Данные добавлены')
    
def edit_client(cursor, first_name, last_name, email): #Функция, позволяющая изменить данные о клиенте (email).
    cursor.execute("""
    SELECT id
    FROM client
    WHERE first_name = %s and last_name = %s                  
    """, (first_name, last_name))
    id_cl = cursor.fetchone()
    if id_cl != None:
        cursor.execute("""
        UPDATE client
        SET email = %s
        WHERE id = %s                
        """, (email, id_cl[0]))
    else:
        print('Клиент не найден')
    
def del_tel(cursor, first_name, last_name, *number): #Функция, позволяющая удалить телефон для существующего клиента (если передан номер, удаляет его, иначе все).
    cursor.execute("""
    SELECT id
    FROM client
    WHERE first_name = %s and last_name = %s                  
    """, (first_name, last_name))
    id_cl = cursor.fetchone()
    i = 7
    if id_cl != None:
        if number:
            cursor.execute("""
            DELETE FROM telephone
            WHERE id_client = %s and number = %s                
            """, (id_cl[0], number))
        else:
            cursor.execute("""
            DELETE FROM telephone WHERE id_client = %s;
            """, (id_cl[0],))
    print('Номер удален')
        
def del_client(cursor, first_name, last_name): #Функция, позволяющая удалить существующего клиента.
    del_tel(cursor, first_name, last_name)
    cursor.execute("""
        DELETE FROM client
        WHERE first_name = %s and last_name = %s                
        """, (first_name, last_name))
    print('Клиент удален')
    
def find_client(cursor, first_name, last_name): #Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
    cursor.execute("""
    SELECT c.first_name, c.last_name, c.email, t.number
    FROM client c
    LEFT JOIN telephone t ON t.id_client = c.id
    WHERE first_name = %s and last_name = %s                  
    """, (first_name, last_name))
    #print(cursor.fetchall())
    for i in cursor.fetchall():
        print(' '.join(i))
       

#Create_table(cur)
add_client(cur, '12300', '45600', '898@', '89523506410')
add_telephone(cur, '12300', '45600', '891100000')
#edit_client(cur, '123000', '45600', '1@1')
#del_tel(cur, '12300', '45600')
#del_client(cur, '12300', '45600')
find_client(cur, '12300', '45600')

if conn:
    cur.close()
    conn.close()
    print('Работа с базой данных завершена')
    


