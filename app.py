from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tareas.db'
db = SQLAlchemy(app)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    hecho = db.Column(db.Boolean)


@app.route('/')
def index():
    listado = Tarea.query.all()
    return render_template('index.html', tareas = listado)

@app.route('/crear-tarea', methods=['POST'])
def crear():
    nueva_tarea = Tarea(content=request.form['contenido'], hecho=False)
    db.session.add(nueva_tarea)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/hecho/<id>')
def hecho(id):
    tarea = Tarea.query.filter_by(id=int(id)).first()
    tarea.hecho = not(tarea.hecho) #el not invierte el valor si es true lo pasa a false y viceversa
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<id>')
def eliminar(id):
    tarea = Tarea.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)