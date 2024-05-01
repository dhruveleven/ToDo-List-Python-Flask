from flask import Flask,render_template,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type =  db.Column(db.Integer,nullable=False)
    content = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.now())

    def __repr__(self):
        return '<Task %r>' % self.id
    
@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_urgency = request.form['type']
        task_content = request.form['content']
        new_task = Todo(type=task_urgency,content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding your new task!"
        
    elif request.method == 'GET' and request.args.get('sort') == 'priority':
        tasks = Todo.query.order_by(Todo.type).all()
        return render_template('index.html', tasks=tasks)

    elif request.method == 'GET' and request.args.get('sort') == 'date':
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
            
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    del_task = Todo.query.get_or_404(id)
    try:
        db.session.delete(del_task)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting task"

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.type = request.form['type']
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Issue while updating task!"
    else:
        return render_template('update.html',task=task)


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
    