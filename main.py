# -----------------------------------------------------------------------
# Importe de librerias
# -----------------------------------------------------------------------
import json
from datetime import datetime
import random

from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS

# -----------------------------------------------------------------------
# Creacion aplicaciones flask
# -----------------------------------------------------------------------
app = Flask(__name__)
CORS(app)

# -----------------------------------------------------------------------
# Make the WSGI interface available at the top level so
# fastcgi can get it.
# -----------------------------------------------------------------------
wsgi_app = app.wsgi_app

# -----------------------------------------------------------------------
# Crear connecion a MongoDB
# -----------------------------------------------------------------------
from pymongo import MongoClient

def contextDB():
    conex = MongoClient(host=['127.0.0.1:27017'])
    conexDB = conex.labApis
    return conexDB

# -----------------------------------------------------------------------
# Crear funciones locales de API para la formacion de tokens.           |
# -----------------------------------------------------------------------
def token():
    ahora = datetime.now()
    antes = datetime.strptime("1970-01-01", "%Y-%m-%d")
    return str(hex(abs((ahora - antes).seconds) * random.randrange(10000000)).split('x')[-1]).upper()

def tokTask():
    ahora = datetime.now()
    antes = datetime.strptime("1970-01-01", "%Y-%m-%d")
    return str(hex(abs((ahora - antes).seconds) * random.randrange(1000000000)).split('x')[-1]).upper()

# -----------------------------------------------------------------------
# Manejo de erroes de para todo tipo de cosas.                          |
# -----------------------------------------------------------------------
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request....!'}), 400)

@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized....!'}), 401)

@app.errorhandler(403)
def forbiden(error):
    return make_response(jsonify({'error': 'Forbidden....!'}), 403)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found....!'}), 404)

@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({'error': 'Internal Server Error....!'}), 500)


# User signup, register new user.
@app.route('/Addestudiante', methods=['POST'])
def AddStutent():
    if not request.json or \
            not 'id' in request.json or \
            not 'name' in request.json or \
            not 'last name' in request.json or \
            not 'telephone number' in request.json or \
            not 'email' in request.json or \
            not 'level' in request.json:
        abort(400)


    user = {
        "_id": request.json['id'],
        'name': request.json['name'],
        'last name': request.json['last name'],
        'telephone number': request.json['telephone number'],
        'email': request.json['email'],
        'level': request.json['level']

    }
    try:
        conex = contextDB()
        conex.user.insert_one(user)
        user2 = {
            "_id": request.json['id'],
            'name': request.json['name'],
            'last name': request.json['last name'],
            'telephone number': request.json['telephone number'],
            'email': request.json['email'],
            'level': request.json['level']
        }
        data = {
            "status_code": 201,
            "status_message": "Data was created",
            "data": {'user': user2}
        }
    except Exception as expc:
        print(expc)
        abort(500)
    return jsonify(data), 201



@app.route('/estudiante', methods=['GET'])
def retrieveStutent():
    try:
        conex = contextDB()
        datos = conex.user.find()

        if datos is None:
            data = {
                "status_code": 200,
                "status_message": "Ok",
                "data": "Empty task list"
            }
        else:
            lista = []
            for collect in datos:
                lista.append({"id": collect['_id'],
                              "name": collect['name'],
                              "last name": collect['last name'],
                              "telephone number": collect['telephone number'],
                              "email": collect['email'],
                              "level": collect['level']})


            data = {
                "status_code": 200,
                "status_message": "Ok",
                "data": lista
            }
    except Exception as expc:
        print(expc)
        abort(500)
    return jsonify(data), 200


@app.route('/datos', methods=['POST'])
def create_datos():
    global datos_globales

    try:
        datos = request.json
        if datos is None:
            data = {
                "status_code": 200,
                "status_message": "Ok",
                "data": "Empty task list"
            }
        else:
            vector = []
            for key, value in datos.items():
                vector.append({key: value})

            cantidad_valores = len(vector)

            # Almacenar los datos en la variable global
            datos_globales = {
                "cantidad_valores": cantidad_valores,
                "vector": vector
            }

            data = {
                "status_code": 200,
                "status_message": "Ok",
                "data": datos_globales
            }
    except Exception as expc:
        print(expc)
        abort(500)
    return jsonify(data), 200

@app.route('/statistics', methods=['GET'])
def get_statistics():
    global datos

    try:
        if datos is None:
            # No hay datos disponibles
            respuesta = {
                "resultado": {
                    "status_code": 404,
                    "status_message": "No data available",
                }
            }
        else:
            valores = []
            for value in datos.values():
                if isinstance(value, int):
                    valores.append(value)

            if not valores:
                # No hay valores enteros en los datos
                respuesta = {
                    "resultado": {
                        "status_code": 404,
                        "status_message": "No integer values available",
                    }
                }
            else:
                mayor = max(valores)
                menor = min(valores)
                n_valores = len(valores)
                promedio = sum(valores) / n_valores
                suma = sum(valores)

                # Construir la respuesta JSON
                respuesta = {
                    "resultado": {
                        "datos": datos,
                        "estadisticas": {
                            "mayor": mayor,
                            "menor": menor,
                            "nValores": n_valores,
                            "promedio": promedio,
                            "suma": suma
                        },
                        "status_code": 200,
                        "status_message": "OK"
                    }
                }

        return jsonify(respuesta), 200
    except Exception as expc:
        print(expc)
        abort(500)
@app.route('/elevar', methods=['GET'])
def elevar_valores():
    global datos_globales

    try:
        datos_originales = {
            "a": 3,
            "b": 2,
            "c": 7,
            "d": 4
        }

        datos_elevados = {key: value ** 2 for key, value in datos_originales.items()}

        data = {
            "resultado": {
                "d_elevados": datos_elevados,
                "d_originales": datos_originales,
                "status_code": 200,
                "status_message": "OK"
            }
        }
    except Exception as expc:
        print(expc)
        abort(500)
    return jsonify(data), 200

@app.route('/elevar/<int:exp>', methods=['GET'])
def elevar_valores(exp):
    global datos_globales

    try:
        datos_originales = {
            "a": 3,
            "b": 2,
            "c": 7,
            "d": 4
        }

        datos_elevados = {key: value ** exp for key, value in datos_originales.items()}

        data = {
            "resultado": {
                "d_elevados": datos_elevados,
                "d_originales": datos_originales,
                "status_code": 200,
                "status_message": "OK"
            }
        }
    except Exception as expc:
        print(expc)
        abort(500)
    return jsonify(data), 200

if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 5000
    app.run(HOST, PORT)
