import boto3
import uuid

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Customers')

# Sample data
sample_customers = [
    {'name': 'John Doe', 'email': 'john.doe@example.com', 'phone': '123-456-7890', 'notes': 'Potential client'},
    {'name': 'Jane Smith', 'email': 'jane.smith@example.com', 'phone': '098-765-4321', 'notes': 'Follow up'},
    {'name': 'Alice Brown', 'email': 'alice.brown@example.com', 'phone': '', 'notes': ''}
]

# Migrate data
def migrate_data():
    try:
        for customer in sample_customers:
            table.put_item(Item={
                'customer_id': str(uuid.uuid4()),
                'name': customer['name'],
                'email': customer['email'],
                'phone': customer['phone'],
                'notes': customer['notes']
            })
        print("Data migration completed!")
    except Exception as e:
        print(f"Error during migration: {str(e)}")

if __name__ == '__main__':
    migrate_data()