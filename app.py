from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# In-memory storage (replace with database in production)
emergencies = []
volunteers = []
users = []

class Emergency:
    def __init__(self, id, type, location, description, people_affected, needs, status="active"):
        self.id = id
        self.type = type
        self.location = location
        self.description = description
        self.people_affected = people_affected
        self.needs = needs
        self.status = status
        self.created_at = datetime.now().isoformat()
        self.lat = 0.0
        self.lng = 0.0

class Volunteer:
    def __init__(self, id, name, location, skills, contact):
        self.id = id
        self.name = name
        self.location = location
        self.skills = skills
        self.contact = contact
        self.lat = 0.0
        self.lng = 0.0
        self.status = "available"

class User:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

# Sample data
emergencies.append(Emergency(
    id=1,
    type="Flood",
    location="Downtown Area",
    description="Severe flooding in residential areas",
    people_affected=500,
    needs=["Food", "Shelter", "Medical Aid"]
))

volunteers.append(Volunteer(
    id=1,
    name="John Doe",
    location="City Center",
    skills=["First Aid", "Rescue"],
    contact="john@email.com"
))

users.append(User(1, "admin", "admin123", "admin"))
users.append(User(2, "volunteer", "vol123", "volunteer"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = next((u for u in users if u.username == username and u.password == password), None)
    
    if user:
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/emergencies', methods=['GET'])
def get_emergencies():
    emergencies_list = [{
        'id': e.id,
        'type': e.type,
        'location': e.location,
        'description': e.description,
        'people_affected': e.people_affected,
        'needs': e.needs,
        'status': e.status,
        'created_at': e.created_at,
        'lat': e.lat,
        'lng': e.lng
    } for e in emergencies]
    return jsonify(emergencies_list)

@app.route('/emergencies', methods=['POST'])
def create_emergency():
    data = request.json
    new_id = max([e.id for e in emergencies], default=0) + 1
    
    emergency = Emergency(
        id=new_id,
        type=data.get('type'),
        location=data.get('location'),
        description=data.get('description'),
        people_affected=data.get('people_affected', 0),
        needs=data.get('needs', [])
    )
    
    emergencies.append(emergency)
    return jsonify({'success': True, 'id': new_id})

@app.route('/volunteers', methods=['GET'])
def get_volunteers():
    volunteers_list = [{
        'id': v.id,
        'name': v.name,
        'location': v.location,
        'skills': v.skills,
        'contact': v.contact,
        'status': v.status,
        'lat': v.lat,
        'lng': v.lng
    } for v in volunteers]
    return jsonify(volunteers_list)

@app.route('/volunteers', methods=['POST'])
def register_volunteer():
    data = request.json
    new_id = max([v.id for v in volunteers], default=0) + 1
    
    volunteer = Volunteer(
        id=new_id,
        name=data.get('name'),
        location=data.get('location'),
        skills=data.get('skills', []),
        contact=data.get('contact')
    )
    
    volunteers.append(volunteer)
    return jsonify({'success': True, 'id': new_id})

@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.json
    user_type = data.get('type')  # 'emergency' or 'volunteer'
    user_id = data.get('id')
    lat = data.get('lat')
    lng = data.get('lng')
    
    if user_type == 'emergency':
        target = next((e for e in emergencies if e.id == user_id), None)
    else:
        target = next((v for v in volunteers if v.id == user_id), None)
    
    if target:
        target.lat = lat
        target.lng = lng
        return jsonify({'success': True})
    
    return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)