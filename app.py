from flask import Flask, request, jsonify, render_template
import boto3
import uuid
from datetime import datetime

app = Flask(__name__)

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Update region if needed
customers_table = dynamodb.Table('Customers')
cases_table = dynamodb.Table('Cases')
deadlines_table = dynamodb.Table('Deadlines')
tasks_table = dynamodb.Table('Tasks')

# Serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

# --- Customer Routes ---
@app.route('/api/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    customer_id = str(uuid.uuid4())
    customers_table.put_item(Item={
        'customer_id': customer_id,
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone'],
        'notes': data['notes']
    })
    return jsonify({'message': 'Customer created', 'customer_id': customer_id}), 201

@app.route('/api/customers', methods=['GET'])
def get_customers():
    response = customers_table.scan()
    return jsonify(response['Items']), 200

@app.route('/api/customers/<customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    customers_table.update_item(
        Key={'customer_id': customer_id},
        UpdateExpression='SET #n = :name, email = :email, phone = :phone, notes = :notes',
        ExpressionAttributeNames={'#n': 'name'},
        ExpressionAttributeValues={
            ':name': data['name'],
            ':email': data['email'],
            ':phone': data['phone'],
            ':notes': data['notes']
        }
    )
    return jsonify({'message': 'Customer updated'}), 200

@app.route('/api/customers/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customers_table.delete_item(Key={'customer_id': customer_id})
    return jsonify({'message': 'Customer deleted'}), 200

# --- Case Routes ---
@app.route('/api/cases', methods=['POST'])
def create_case():
    data = request.get_json()
    case_id = str(uuid.uuid4())
    cases_table.put_item(Item={
        'case_id': case_id,
        'case_number': data['case_number'],
        'court': data['court'],
        'status': data['status'],
        'description': data['description'],
        'client_ids': data['client_ids'],  # List of customer IDs
        'start_date': data['start_date']
    })
    return jsonify({'message': 'Case created', 'case_id': case_id}), 201

@app.route('/api/cases', methods=['GET'])
def get_cases():
    response = cases_table.scan()
    return jsonify(response['Items']), 200

# --- Deadline Routes ---
@app.route('/api/deadlines', methods=['POST'])
def create_deadline():
    data = request.get_json()
    deadline_id = str(uuid.uuid4())
    deadlines_table.put_item(Item={
        'deadline_id': deadline_id,
        'due_date': data['due_date'],
        'case_id': data['case_id'],
        'title': data['title'],
        'description': data['description'],
        'status': data['status']
    })
    return jsonify({'message': 'Deadline created', 'deadline_id': deadline_id}), 201

@app.route('/api/deadlines', methods=['GET'])
def get_deadlines():
    response = deadlines_table.scan()
    # Filter for upcoming deadlines (simplified for demo)
    today = datetime.utcnow().isoformat().split('T')[0]
    upcoming = [item for item in response['Items'] if item['due_date'] >= today]
    return jsonify(upcoming), 200

# --- Task Routes ---
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task_id = str(uuid.uuid4())
    tasks_table.put_item(Item={
        'task_id': task_id,
        'case_id': data['case_id'],
        'customer_id': data.get('customer_id', ''),
        'title': data['title'],
        'description': data['description'],
        'due_date': data['due_date'],
        'assigned_to': data['assigned_to'],
        'status': data['status']
    })
    return jsonify({'message': 'Task created', 'task_id': task_id}), 201

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    response = tasks_table.scan()
    return jsonify(response['Items']), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)