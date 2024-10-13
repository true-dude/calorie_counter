import psycopg2
from datetime import datetime, timedelta

def init_db():
    conn = psycopg2.connect("dbname=calories user=postgres password=postgres host=db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS dishes (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            protein FLOAT,
            fat FLOAT,
            carbs FLOAT,
            calories FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def add_dish(name, protein, fat, carbs, calories):
    conn = psycopg2.connect("dbname=calories user=postgres password=postgres host=db")
    cur = conn.cursor()
    cur.execute('INSERT INTO dishes (name, protein, fat, carbs, calories) VALUES (%s, %s, %s, %s, %s)',
                (name, protein, fat, carbs, calories))
    conn.commit()
    cur.close()
    conn.close()

def get_dishes():
    conn = psycopg2.connect("dbname=calories user=postgres password=postgres host=db")
    cur = conn.cursor()
    cur.execute('SELECT * FROM dishes ORDER BY created_at DESC')
    dishes = cur.fetchall()
    cur.close()
    conn.close()
    return dishes

def edit_dish(id, name, protein, fat, carbs, calories):
    conn = psycopg2.connect("dbname=calories user=postgres password=postgres host=db")
    cur = conn.cursor()
    cur.execute('UPDATE dishes SET name=%s, protein=%s, fat=%s, carbs=%s, calories=%s WHERE id=%s',
                (name, protein, fat, carbs, calories, id))
    conn.commit()
    cur.close()
    conn.close()

def delete_dish(id):
    conn = psycopg2.connect("dbname=calories user=postgres password=postgres host=db")
    cur = conn.cursor()
    cur.execute('DELETE FROM dishes WHERE id=%s', (id,))
    conn.commit()
    cur.close()
    conn.close()

def search_dishes(query):
    conn = psycopg2.connect("dbname=calories user=postgres password=postgres host=db")
    cur = conn.cursor()
    cur.execute('SELECT * FROM dishes WHERE name ILIKE %s', (f'%{query}%',))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def get_calories_by_date():
    conn = psycopg2.connect("dbname=calories user=postgres password=postgres host=db")
    cur = conn.cursor()
    
    cur.execute('''
        SELECT DATE(created_at), SUM(calories)
        FROM dishes
        WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at)
    ''')
    
    results = cur.fetchall()
    cur.close()
    conn.close()

    labels = [str(row[0]) for row in results]
    data = [row[1] for row in results]
    return labels, data
    
def get_calories_by_minute():
    conn = psycopg2.connect("dbname=calories user=postgres password=postgres host=db")
    cur = conn.cursor()

    # Получение данных за последние 10 минут с группировкой по минутам
    cur.execute('''
        SELECT DATE_TRUNC('minute', created_at), SUM(calories)
        FROM dishes
        WHERE created_at >= NOW() - INTERVAL '10 minutes'
        GROUP BY DATE_TRUNC('minute', created_at)
        ORDER BY DATE_TRUNC('minute', created_at)
    ''')
    
    results = cur.fetchall()
    cur.close()
    conn.close()

    # Подготовка данных для Chart.js
    labels = []
    data = []

    # Формирование данных по каждой минуте за последние 10 минут
    current_time = datetime.now()
    for i in range(10):
        minute_label = (current_time - timedelta(minutes=i)).strftime('%H:%M')
        labels.insert(0, minute_label)  # Вставляем в начало списка, чтобы шло от старых данных к новым
        # Проверяем, есть ли записи за это время
        found = False
        for row in results:
            if row[0].strftime('%H:%M') == minute_label:
                data.insert(0, row[1])
                found = True
                break
        if not found:
            data.insert(0, 0)  # Если данных нет, ставим 0 калорий
    
    return labels, data
