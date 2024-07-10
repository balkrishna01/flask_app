from flask import Blueprint, Response, request, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps
import pymongo
from datetime import datetime
from config import Config

client = pymongo.MongoClient(Config.MONGODB_URI)
db = client.my_mongo_db

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/v1/test', methods=['GET'])
def test_db_connection():
    try:
        # Try to perform a simple query to test the connection
        db.command('ping')
        return jsonify({'message': 'Database connection successful'}), 200
    except Exception as e:
        return jsonify({'message': 'Database connection failed', 'error': str(e)}), 500


@api_bp.route('/api/v1/students', methods=['GET'])
def get_students():
    students = db.students.find()
    return Response(dumps(students), mimetype='application/json')


@api_bp.route('/api/v1/students/<id>', methods=['GET'])
def get_single_student(id):
    try:
        student = db.students.find_one({'_id': ObjectId(id)})
        if student:
            return Response(dumps(student), mimetype='application/json')
        else:
            return jsonify({'message': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)})


@api_bp.route('/api/v1/students', methods=['POST'])
def create_student():
    try:
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
    except Exception as e:
        return jsonify({'error': str(e)})


@api_bp.route('/api/v1/students/<id>', methods=['PUT'])
def update_student(id):
    try:
        data = request.form.to_dict()
        if 'skills' in data:
            data['skills'] = data['skills'].split(', ')

        updated_student = db.students.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': data},
            return_document=pymongo.ReturnDocument.AFTER
        )

        if updated_student:
            return Response(dumps(updated_student), mimetype='application/json')
        else:
            return jsonify({'message': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)})


@api_bp.route('/api/v1/student/<id>', methods=['DELETE'])
def delete_student(id):
    try:
        db.students.delete_one({'_id': ObjectId(id)})
        return jsonify({'message': 'Student deleted successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)})