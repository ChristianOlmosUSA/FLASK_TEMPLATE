"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
SOME SQL TO REMEMBER: show databases; use example; show tables; describe person; select * from Person; quit; exit;
TO RUN: pipenv run migrate, pipenv run upgrade ==> whenever a new class is added.
pipenv run start
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db
from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

@app.route('/person', methods=['POST', 'GET'])
def handle_person():

    if request.method == 'GET':
       newInput = Person.query.all()
       newInput = list(map(lambda x: x.serialize(), newInput))  # list converts the list, map, lambda is like => function in js
       return jsonify(newInput), 200

    if request.method == 'POST':
        newBody = request.get_json()
        newPerson = Person(username=newBody['username'], email=newBody['email'], password=newBody['password'])
        db.session.add(newPerson)
        db.session.commit()
        return "OK", 200
    return "invalid method", 404
    



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
