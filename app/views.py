import datetime

from flask import render_template, request
from app import app, redisCache
from app.forms import CreateTaskForm, UpdateTaskForm


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/createTask', methods=['GET', 'POST'])
def create_task():
    if request.method == 'GET':
        return render_template("create_task.html", form=CreateTaskForm())
    text = request.form['text']
    created = str(datetime.datetime.now())
    print(created)
    redisCache.set(created, text)
    method = 'CREATE'
    return render_template("success.html", method=method, text=text, created=created)


@app.route('/showTasks', methods=['GET'])
def show_tasks():
    dict_of_tasks = {}
    for key in redisCache.keys():
        dict_of_tasks[key.decode()] = redisCache.get(key).decode()

    return render_template("show_tasks.html", dict_of_tasks=dict_of_tasks)


@app.route('/updateTask', methods=['GET', 'POST'])
def update_task():
    if request.method == 'GET':
        form = UpdateTaskForm()
        form.created.choices = [(str(i.decode()) +"~~" + str(redisCache.get(i).decode()), i.decode()) for i in redisCache.keys()]
        form.process()
        return render_template('update_task.html', form=form)
    text = request.form['text']
    created = request.form['created'].split('~~')[0]
    print(request.form['created'], request.form['text'])
    redisCache.set(created, text)
    method = 'UPDATE'
    return render_template('success.html', method=method, text=text, created=created)


@app.route('/deleteTask', methods=['GET', 'POST'])
def delete_task():
    if request.method == 'GET':
        form = UpdateTaskForm()
        form.created.choices = [(created.decode() +"~~" + redisCache.get(created).decode(), created.decode()) for created in redisCache.keys()]
        return render_template('delete_task.html', form=form)
    created = request.form['created'].split("~~")[0]
    text = redisCache.get(created).decode()
    redisCache.delete(created)
    method = 'DELETE'
    return render_template('success.html', method=method, text=text, created=created)


@app.route('/deleteAllTasks', methods=['GET', 'POST'])
def delete_all_tasks():
    for key in redisCache.scan_iter():
        redisCache.delete(key)
    return render_template('index.html')
