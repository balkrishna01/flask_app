from flask import Flask, Response
import json
from bson.objectid import ObjectId
from bson.json_util import dumps
import pymongo
import os


app = Flask(__name__)

# mongodb://mongo:mongo@localhost:27017/
MONGODB_URI = 'mongodb://mongo:mongo@localhost:27017/'
client = pymongo.MongoClient(MONGODB_URI)

# Creating database
db = client.my_mongo_db


@app.route('/api/v1/students', methods=['GET'])
def get_students():
    students = db.students.find()
    return Response(dumps(students), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
