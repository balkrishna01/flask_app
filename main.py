from flask import Flask, Response, request, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps
import pymongo
import json
from datetime import datetime

app = Flask(__name__)

# mongodb://mongo:mongo@localhost:27017/
MONGODB_URI = 'mongodb://mongo:mongo@localhost:27017/'
client = pymongo.MongoClient(MONGODB_URI)

# Creating database
db = client.my_mongo_db


@app.route('/api/v1/test', methods=['GET'])
def test_db_connection():
    try:
        # Try to perform a simple query to test the connection
        db.command('ping')
        return jsonify({'message': 'Database connection successful'}), 200
    except Exception as e:
        return jsonify({'message': 'Database connection failed', 'error': str(e)}), 500


@app.route('/api/v1/students', methods=['GET'])
def get_students():
    students = db.students.find()
    return Response(dumps(students), mimetype='application/json')


@app.route('/api/v1/students/<id>', methods=['GET'])
def get_single_student(id):
    student = db.students.find_one({'_id': ObjectId(id)})
    return Response(dumps(student), mimetype='application/json')


@app.route('/api/v1/students', methods=['POST'])
def create_student():
    name = request.form['name']
    country = request.form['country']
    city = request.form['city']
    skills = request.form['skills'].split(', ')
    bio = request.form['bio']
    birth_year = request.form['birth_year']
    created_at = datetime.now()
    student = {
        'name': name,
        'country': country,
        'city': city,
        'birth_year': birth_year,
        'skills': skills,
        'bio': bio,
        'created_at': created_at

    }
    result = db.students.insert_one(student)
    return jsonify({
        'message': 'Student record created successfully',
        'id': str(result.inserted_id)
    }), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
