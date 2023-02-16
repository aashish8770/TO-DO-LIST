from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}>'

db.create_all()

@app.route('/todos', methods=['GET', 'POST'])
def todos():
    if request.method == 'GET':
        todos = Todo.query.all()
        return {'todos': [todo.task for todo in todos]}
    if request.method == 'POST':
        task = request.form['task']
        todo = Todo(task=task)
        db.session.add(todo)
        db.session.commit()
        return {'message': 'Todo created'}

@app.route('/todos/<int:todo_id>', methods=['PUT', 'DELETE'])
def todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return {'error': 'Todo not found'}, 404
    if request.method == 'PUT':
        task = request.form['task']
        complete = request.form['complete']
        todo.task = task
        todo.complete = complete
        db.session.commit()
        return {'message': 'Todo updated'}
    if request.method == 'DELETE':
        db.session.delete(todo)
        db.session.commit()
        return {'message': 'Todo deleted'}

if __name__ == '__main__':
    app.run(debug=True)
