import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla_futuros = dynamodb.Table('futuros-table')  # Cambia por el nombre real de tu tabla de futuros

response = tabla_futuros.scan(Limit=5)
items = response['Items']

print("Ejemplo de registros de Futuros:")
for item in items:
    print(item) 