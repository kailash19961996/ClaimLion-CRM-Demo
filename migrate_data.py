import boto3
import uuid
from datetime import datetime, timedelta

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Update region if needed
customers_table = dynamodb.Table('Customers')
cases_table = dynamodb.Table('Cases')
deadlines_table = dynamodb.Table('Deadlines')
tasks_table = dynamodb.Table('Tasks')

# Sample data
sample_customers = [
    {'name': 'John Doe', 'email': 'john.doe@example.com', 'phone': '123-456-7890', 'notes': 'Potential client'},
    {'name': 'Jane Smith', 'email': 'jane.smith@example.com', 'phone': '098-765-4321', 'notes': 'Follow up'},
    {'name': 'Alice Brown', 'email': 'alice.brown@example.com', 'phone': '', 'notes': ''}
]

sample_cases = [
    {'case_number': 'CL-2025-001', 'court': 'District Court', 'status': 'Open', 'description': 'Personal injury case', 'client_ids': [], 'start_date': '2025-01-01'},
    {'case_number': 'CL-2025-002', 'court': 'Supreme Court', 'status': 'Pending', 'description': 'Contract dispute', 'client_ids': [], 'start_date': '2025-02-01'}
]

sample_deadlines = [
    {'case_id': '', 'title': 'File Motion', 'description': 'Motion to dismiss', 'due_date': (datetime.utcnow() + timedelta(days=10)).strftime('%Y-%m-%d'), 'status': 'Pending'},
    {'case_id': '', 'title': 'Hearing', 'description': 'Preliminary hearing', 'due_date': (datetime.utcnow() + timedelta(days=20)).strftime('%Y-%m-%d'), 'status': 'Pending'}
]

sample_tasks = [
    {'case_id': '', 'customer_id': '', 'title': 'Prepare Deposition', 'description': 'Prepare questions for witness', 'due_date': (datetime.utcnow() + timedelta(days=5)).strftime('%Y-%m-%d'), 'assigned_to': 'Attorney A', 'status': 'Pending'},
    {'case_id': '', 'customer_id': '', 'title': 'Client Meeting', 'description': 'Discuss case strategy', 'due_date': (datetime.utcnow() + timedelta(days=7)).strftime('%Y-%m-%d'), 'assigned_to': 'Attorney B', 'status': 'Pending'}
]

def migrate_data():
    # Migrate customers
    customer_ids = []
    for customer in sample_customers:
        customer_id = str(uuid.uuid4())
        customer_ids.append(customer_id)
        customers_table.put_item(Item={
            'customer_id': customer_id,
            'name': customer['name'],
            'email': customer['email'],
            'phone': customer['phone'],
            'notes': customer['notes']
        })

    # Migrate cases
    case_ids = []
    for i, case in enumerate(sample_cases):
        case_id = str(uuid.uuid4())
        case_ids.append(case_id)
        case['client_ids'] = [customer_ids[i % len(customer_ids)]]  # Assign a customer to each case
        cases_table.put_item(Item={
            'case_id': case_id,
            'case_number': case['case_number'],
            'court': case['court'],
            'status': case['status'],
            'description': case['description'],
            'client_ids': case['client_ids'],
            'start_date': case['start_date']
        })

    # Migrate deadlines
    for i, deadline in enumerate(sample_deadlines):
        deadline_id = str(uuid.uuid4())
        deadline['case_id'] = case_ids[i % len(case_ids)]
        deadlines_table.put_item(Item={
            'deadline_id': deadline_id,
            'due_date': deadline['due_date'],
            'case_id': deadline['case_id'],
            'title': deadline['title'],
            'description': deadline['description'],
            'status': deadline['status']
        })

    # Migrate tasks
    for i, task in enumerate(sample_tasks):
        task_id = str(uuid.uuid4())
        task['case_id'] = case_ids[i % len(case_ids)]
        task['customer_id'] = customer_ids[i % len(customer_ids)]
        tasks_table.put_item(Item={
            'task_id': task_id,
            'case_id': task['case_id'],
            'customer_id': task['customer_id'],
            'title': task['title'],
            'description': task['description'],
            'due_date': task['due_date'],
            'assigned_to': task['assigned_to'],
            'status': task['status']
        })

    print("Data migration completed!")

if __name__ == '__main__':
    migrate_data()
