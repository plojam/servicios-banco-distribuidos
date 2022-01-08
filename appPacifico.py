from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import cross_origin, CORS 

app = Flask(__name__)
cors = CORS(app, resources={"*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root3:patito123@192.168.40.139/banco_del_pacifico'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(10), unique=True)
    nombre = db.Column(db.String(70))
    saldo = db.Column(db.Integer)
    descripcion = db.Column(db.String(100))
    def __init__(self, cedula, nombre, saldo, descripcion):
        self.cedula = cedula
        self.nombre = nombre
        self.saldo = saldo
        self.descripcion = descripcion

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'cedula', 'nombre', 'saldo', 'descripcion')


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/crearCliente', methods=['Post'])
@cross_origin()
def create_task():
  cedula = request.json['cedula']
  nombre = request.json['nombre']
  saldo = request.json['saldo']
  descripcion = request.json['descripcion']

  new_task= Cliente(cedula ,nombre, saldo, descripcion)

  db.session.add(new_task)
  db.session.commit()
  print(request.json)
  print(new_task)
  
  return task_schema.jsonify(new_task)
  

@app.route('/clientes', methods=['GET'])
@cross_origin()
def get_tasks():
  all_tasks = Cliente.query.all()
  result = tasks_schema.dump(all_tasks)
  return jsonify(result)

@app.route('/cliente/<cedulaCLI>', methods=['GET'])
@cross_origin()
def get_task(cedulaCLI):
  task = Cliente.query.filter_by(cedula=cedulaCLI).first()
  return task_schema.jsonify(task)

@app.route('/depositar/<cedulaCLI>/<saldoCLI>', methods=['PUT'])
@cross_origin()
def depositar_task(cedulaCLI, saldoCLI):
  task = Cliente.query.filter_by(cedula = cedulaCLI).first()
  saldoRecuperado = task.saldo
  saldoEnviado = int(saldoCLI)
  #print(type(aux))
  saldoNuevo = saldoRecuperado + saldoEnviado
  task.saldo = saldoNuevo
  print( "verr ", saldoNuevo)
  db.session.commit()
  print("COMMIT")

  return task_schema.jsonify(task)


@app.route('/retirar/<cedulaCLI>/<saldoCLI>', methods=['PUT'])
@cross_origin()
def retirar_task(cedulaCLI, saldoCLI):
  task = Cliente.query.filter_by(cedula = cedulaCLI).first()
  saldoRecuperado = task.saldo
  saldoEnviado = int(saldoCLI)
  #print(type(aux))
  saldoNuevo = saldoRecuperado - saldoEnviado
  task.saldo = saldoNuevo
  db.session.commit()
  print("COMMIT")

  return task_schema.jsonify(task)


@app.route('/cliente/<id>', methods=['DELETE'])
@cross_origin()
def delete_task(id):
  task = Cliente.query.get(id)
  db.session.delete(task)
  db.session.commit()
  return task_schema.jsonify(task)


@app.route('/', methods=['GET'])
@cross_origin()
def index():
    all_tasks = Cliente.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify({'clientes banco del pacifico': result})


if __name__ == "__main__":
    app.run(host='192.168.40.136', port=5001, debug=True)
