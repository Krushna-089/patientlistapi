from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os

app = Flask(__name__)

# Path to the JSON data file
DATA_FILE = 'data.json'

# Initialize JSON file if it doesn't exist
def init_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

# Read data from JSON file
def read_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Write data to JSON file
def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Generate new ID
def generate_id(data):
    if not data:
        return 1
    return max(item['id'] for item in data) + 1

# Route 1: Home page with form for inserting data
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        room_number = request.form.get('room_number')
        name = request.form.get('name')
        phone = request.form.get('phone')
        id_number = request.form.get('id')
        doctor_name = request.form.get('doctorname')
        diet = request.form.get('diet')
        diet_skill = request.form.get('dietskill')
        
        # Read existing data
        data = read_data()
        
        # Create new entry
        new_entry = {
            'id': generate_id(data),
            'room_number': room_number,
            'name': name,
            'phone': phone,
            'id_number': id_number,
            'doctor_name': doctor_name,
            'diet': diet,
            'diet_skill': diet_skill
        }
        
        # Add to data and save
        data.append(new_entry)
        write_data(data)
        
        return redirect(url_for('view_data'))
    
    return render_template('index.html')

# Route 2: View all data in table format with add and edit
@app.route('/view')
def view_data():
    data = read_data()
    return render_template('view_data.html', data=data)

# Route 3: Edit data
@app.route('/edit/<int:record_id>', methods=['GET', 'POST'])
def edit_data(record_id):
    data = read_data()
    
    if request.method == 'POST':
        # Update the record
        for item in data:
            if item['id'] == record_id:
                item['room_number'] = request.form.get('room_number')
                item['name'] = request.form.get('name')
                item['phone'] = request.form.get('phone')
                item['id_number'] = request.form.get('id')
                item['doctor_name'] = request.form.get('doctorname')
                item['diet'] = request.form.get('diet')
                item['diet_skill'] = request.form.get('dietskill')
                break
        
        write_data(data)
        return redirect(url_for('view_data'))
    
    # Find the record to edit
    record = None
    for item in data:
        if item['id'] == record_id:
            record = item
            break
    
    return render_template('edit.html', record=record)

# Route 4: Delete data
@app.route('/delete/<int:record_id>')
def delete_data(record_id):
    data = read_data()
    data = [item for item in data if item['id'] != record_id]
    write_data(data)
    return redirect(url_for('view_data'))

# Route 5: API route - returns data in JSON format
@app.route('/api/data')
def api_data():
    data = read_data()
    return jsonify(data)

if __name__ == '__main__':
    init_data_file()
    app.run(debug=True, host='0.0.0.0', port=5000)
