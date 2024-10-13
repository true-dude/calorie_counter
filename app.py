from flask import Flask, render_template, request, redirect, url_for
from db import init_db, add_dish, get_dishes, edit_dish, delete_dish, get_dish_by_id, add_consumed, get_consumed, get_calories_by_minute

app = Flask(__name__)



@app.route('/')
def index():
    dishes = get_dishes()
    consumed = get_consumed()
    consumed = [(item[0], item[1], item[2], item[3]) for item in consumed]
    return render_template('index.html', dishes=dishes, consumed=consumed)

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
    
    dish = get_dish_by_id(id)
    return render_template('edit.html', dish=dish)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    delete_dish(id)
    return redirect(url_for('index'))

@app.route('/consume', methods=['POST'])
def consume():
    dish_id = request.form['dish_id']
    quantity = request.form['quantity']
    add_consumed(dish_id, quantity)
    return redirect(url_for('index'))

@app.route('/chart')
def chart():
    labels, data = get_calories_by_minute()
    return {
        'labels': labels,
        'data': data
    }

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0')
