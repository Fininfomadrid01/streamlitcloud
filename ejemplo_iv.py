import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla_iv = dynamodb.Table('dev-iv-table')  # Cambia por el nombre real de tu tabla de IV

response = tabla_iv.scan(Limit=5)
items = response['Items']

print("Ejemplo de registros de IV:")
for item in items:
    print(item) 