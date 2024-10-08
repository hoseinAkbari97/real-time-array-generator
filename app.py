from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import numpy as np
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["array_db"]
collection = db["arrays"]

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('generate_array')
def generate_array(data):
    size = data.get('size', 10000)
    min_val = data.get('min_val', 0)
    max_val = data.get('max_val', 99999)
    array = np.random.randint(min_val, max_val, size).tolist()
    
    # Store array in MongoDB
    collection.insert_one({'array': array})
    
    # Emit the array to all connected clients
    emit('array_generated', {'array': array}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
