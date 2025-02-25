from flask import Flask, request, redirect
from flask import render_template
from data.user import current_user
from data.task_processing import plot_tasks, get_tasks, add_task
from config.mogodb_connect import init_mongodb

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html', user=current_user, tasks=get_tasks(), plot=plot_tasks())


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add_task', methods=['POST'])
def add_new_task():
    if request.method == 'POST':
        task = {
            'title': request.form.get('title'),
            'description': 'This is a new task',
            'status': request.form.get('status'),
            'progress': float(request.form.get('progress')),
            'due_date': request.form.get('due_date')
        }
        add_task(task)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)