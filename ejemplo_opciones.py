import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla_opciones = dynamodb.Table('dev-raw-prices')  # Cambia por el nombre real de tu tabla de opciones

response = tabla_opciones.scan(Limit=5)
items = response['Items']

print("Ejemplo de registros de Opciones:")
for item in items:
    print(item) 