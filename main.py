# let's import the flask
import pymongo
from flask import Flask, render_template
import os  # importing operating system module

# mongodb://mongo:mongo@localhost:27017/
MONGODB_URI = 'mongodb://mongo:mongo@localhost:27017/'
client = pymongo.MongoClient(MONGODB_URI)

# Creating database
db = client.my_mongo_db

# Creating students collection and inserting a document
db.students.insert_one({'name': 'Peter', 'country': 'Nepal', 'city': 'Kathmandu', 'age': 200})
print(client.list_database_names())

app = Flask(__name__)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
