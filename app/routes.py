from flask import render_template, request, jsonify
from . import db
from .models import Todo

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/todos', methods=['GET', 'POST'])
    def handle_todos():
        if request.method == 'POST':
            data = request.get_json()
            new_todo = Todo(text=data['text'])
            db.session.add(new_todo)
            db.session.commit()
            return jsonify(new_todo.to_dict()), 201
        
        todos = Todo.query.all()
        return jsonify([todo.to_dict() for todo in todos])

    @app.route('/api/todos/<int:id>', methods=['DELETE', 'PATCH'])
    def todo_actions(id):
        todo = Todo.query.get_or_404(id)
        
        if request.method == 'DELETE':
            db.session.delete(todo)
            db.session.commit()
            return jsonify({'message': 'Todo deleted'})
        
        if request.method == 'PATCH':
            data = request.get_json()
            todo.completed = data.get('completed', todo.completed)
            db.session.commit()
            return jsonify(todo.to_dict())