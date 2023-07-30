import psycopg2

def create_db(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients_db(
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(15) NOT NULL,
            lastname VARCHAR(15) NOT NULL,
            email VARCHAR(30) NOT NULL
            );
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
            id_phones SERIAL PRIMARY KEY,
            client_id INT NOT NULL REFERENCES clients_db(id),
            phone VARCHAR(20) NOT NULL
            );
        """)
    return


def add_client(cur, first_name, last_name, email, phones=None):
    cur.execute("""
        INSERT INTO clients_db(firstname, lastname, email) 
        VALUES(%s, %s, %s);
        """, (first_name, last_name, email))
    cur.execute("""
        SELECT id from clients_db
        ORDER BY id DESC
        LIMIT 1
        """)
    id = cur.fetchone()[0]
    if phones is None:
        return id
    else:
        cur.execute("""
            INSERT INTO phones(client_id, phone) VALUES(%s, %s);
            """, (id, phones))
    return


def add_phone(cur, client_id, phone):
    cur.execute("""
        INSERT INTO phones(client_id, phone) VALUES(%s, %s);
        """, (client_id, phone))
    return

def change_client(cur, id, first_name=None, last_name=None, email=None, phones=None):
    if first_name is not None:
        cur.execute("""
            UPDATE clients_db SET firstname=%s WHERE id=%s;
            """, (first_name, id))
    if last_name != None:
        cur.execute("""
            UPDATE clients_db SET lastname=%s WHERE id=%s;
            """, (last_name, id))
    if email != None:
        cur.execute("""
            UPDATE clients_db SET email=%s WHERE id=%s;
            """, (email, id))
    if phones != None:
        add_phone(cur, id, phones)
    return

def delete_phone(cur, client_id, phone):
    cur.execute("""
        DELETE FROM phones WHERE client_id=%s and phone=%s;
        """, (client_id, phone))
    return

def delete_client(cur, client_id):
    cur.execute("""
        DELETE FROM phones WHERE client_id=%s;
        """, (client_id,))
    cur.execute("""
        DELETE FROM clients_db WHERE id=%s;
        """, (client_id,))
    cur.execute("""
        SELECT * FROM clients_db;
        """)
    return


def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    if phone is not None:
        cur.execute("""
            SELECT clients_db.id FROM clients_db
            JOIN phones ON phones.client_id = clients_db.id
            WHERE phones.phone=%s;
            """, (phone,))
    else:
        cur.execute("""
            SELECT id FROM clients_db
            WHERE firstname=%s OR lastname=%s OR email=%s;
            """, (first_name, last_name, email))
    print(cur.fetchall())


if __name__ == '__main__':
    with psycopg2.connect(database="clients_db", user="postgres", password="Snp54321") as conn:
        with conn.cursor() as cur:
            # Обнуляние БД
            cur.execute("""
            DROP TABLE phones;
            DROP TABLE clients_db;
            """) 
            
            # 1. Создание БД:
            create_db(cur)
            print("БД создана")

            # 2. Добавляем новых клиентов:
            add_client(cur, 'Александр', 'Иванов', 'aivanov@gmail.com', '79129122212')
            add_client(cur, 'Иван', 'Петров', 'ivapet@gmail.com')
            add_client(cur, 'Светлана', 'Светикова', 'ss125@gmail.com', '79059242735')
            add_client(cur, 'Анатолий', 'Леснов', 'alesnov10@gmail.com')
            add_client(cur, 'Елена', 'Коровина', 'ekorovina15@gmail.com')
            add_client(cur, 'Мария', 'Свердлова', 'ms8888@gmail.com')
            print("Новые клиенты добавлены")
                        
            # 3. Добавляем телефон для существующего клиента:
            add_phone(cur, '1', '79128884455')
            add_phone(cur, '2', '79085252471')
            add_phone(cur, '4', '79587511523')
            print("Телефон добавлен")

            # 4. Изменяем данные о клиенте:
            change_client(cur, '1', 'Алексей')
            change_client(cur, '2', None, None, 'ivanpetrov@gmail.com')
            change_client(cur, '3', None, None, 'ss126@gmail.com')
            change_client(cur, '2', None, None, None, '79992455656')
            
            # 5. Удаляем телефон для существующего клиента:
            delete_phone(cur, '1', '79128884455')
            delete_phone(cur, '4', '79587511523')  
 
            # 6. Удаляем существующего клиента:
            delete_client(cur, 5)
            
            # 7. Находим клиента по его данным: имени, фамилии, email или телефону:
            find_client(cur, 'Елена')
            find_client(cur, None, 'Иванов')
            find_client(cur, None, None, 'ms8888@gmail.com')
            find_client(cur, None, None, None, '79129122212')

        cur.close()