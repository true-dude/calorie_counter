import psycopg2
from datetime import datetime, timedelta

def init_db():
    conn = psycopg2.connect("dbname=calories user=postgres password=postgres host=db")
    cur = conn.cursor()
    
    # Таблица для блюд
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
    
    # Таблица для съеденных блюд
    cur.execute('''
        CREATE TABLE IF NOT EXISTS consumed (
            id SERIAL PRIMARY KEY,
            dish_id INT REFERENCES dishes(id),
            quantity FLOAT,  -- Количество съеденного блюда (в граммах)
            consumed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

def get_dishes():
    conn = psycopg2.connect("dbname=calories user=postgres password=postgres host=db")
    cur = conn.cursor()
    cur.execute('SELECT id, name, calories FROM dishes ORDER BY created_at DESC')
    dishes = cur.fetchall()
    cur.close()
    conn.close()
    return dishes

def get_dish_by_id(id):
    conn = psycopg2.connect("dbname=calories user=postgres password=postgres host=db")
    cur = conn.cursor()
    cur.execute('SELECT id, name, protein, fat, carbs, calories FROM dishes WHERE id = %s', (id,))
    dish = cur.fetchone()
    cur.close()
    conn.close()
    return dish

def add_consumed(dish_id, quantity):
    conn = psycopg2.connect("dbname=calories user=postgres password=postgres host=db")
    cur = conn.cursor()
    cur.execute('INSERT INTO consumed (dish_id, quantity) VALUES (%s, %s)', (dish_id, quantity))
    conn.commit()
    cur.close()
    conn.close()

def get_consumed():
    conn = psycopg2.connect("dbname=calories user=postgres password=postgres host=db")
    cur = conn.cursor()
    cur.execute('''
        SELECT dishes.name, consumed.quantity, dishes.calories, consumed.consumed_at
        FROM consumed
        JOIN dishes ON consumed.dish_id = dishes.id
        ORDER BY consumed.consumed_at DESC
    ''')
    consumed = cur.fetchall()
    cur.close()
    conn.close()
    return consumed

def get_calories_by_minute():
    conn = psycopg2.connect("dbname=calories user=postgres password=postgres host=db")
    cur = conn.cursor()

    # Получение данных по съеденным калориям за последние 10 минут
    cur.execute('''
        SELECT DATE_TRUNC('minute', consumed_at), SUM(dishes.calories * (consumed.quantity / 100))
        FROM consumed
        JOIN dishes ON consumed.dish_id = dishes.id
        WHERE consumed_at >= NOW() - INTERVAL '10 minutes'
        GROUP BY DATE_TRUNC('minute', consumed_at)
        ORDER BY DATE_TRUNC('minute', consumed_at)
    ''')
    
    results = cur.fetchall()
    cur.close()
    conn.close()

    # Подготовка данных для Chart.js
    labels = []
    data = []

    current_time = datetime.now()
    for i in range(10):
        minute_label = (current_time - timedelta(minutes=i)).strftime('%H:%M')
        labels.insert(0, minute_label)
        found = False
        for row in results:
            if row[0].strftime('%H:%M') == minute_label:
                data.insert(0, row[1])
                found = True
                break
        if not found:
            data.insert(0, 0)
    
    return labels, data
