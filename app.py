from flask import Flask, render_template, request, redirect, url_for, jsonify
from db import init_db, add_dish, get_dishes, edit_dish, delete_dish, search_dishes, get_calories_by_date, get_calories_by_minute
import pytz
from datetime import datetime

app = Flask(__name__)

local_tz = pytz.timezone('Europe/Moscow')

def utc_to_local(utc_dt):
    utc_dt = utc_dt.replace(tzinfo=pytz.utc)
    return utc_dt.astimezone(local_tz)

#@app.route('/')
#def index():
#    dishes = get_dishes()
#    dishes = [(dish[0], dish[1], dish[2], dish[3], dish[4], dish[5], utc_to_local(dish[6])) for dish #in dishes]
#    return render_template('index.html', dishes=dishes)

@app.route('/')
def index():
    dishes = get_dishes()
    return render_template('index.html', dishes=dishes)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    protein = request.form['protein']
    fat = request.form['fat']
    carbs = request.form['carbs']
    calories = request.form['calories']
    add_dish(name, protein, fat, carbs, calories)
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        name = request.form['name']
        protein = request.form['protein']
        fat = request.form['fat']
        carbs = request.form['carbs']
        calories = request.form['calories']
        edit_dish(id, name, protein, fat, carbs, calories)
        return redirect(url_for('index'))
    dish = [dish for dish in get_dishes() if dish[0] == id][0]
    return render_template('edit.html', dish=dish)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    delete_dish(id)
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('query')
    results = search_dishes(query)
    return jsonify(results)

@app.route('/chart')
def chart():
    labels, data =  get_calories_by_minute()
    return jsonify({
        'labels': labels,
        'data': data
    })

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0')

