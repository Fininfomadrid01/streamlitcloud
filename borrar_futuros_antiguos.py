import boto3

# Configura tu región y nombre de la tabla
REGION = 'us-east-1'
TABLE_NAME = 'futuros-table'  # Cambiado al nombre correcto

dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

# Escanea todos los registros de futuros
response = table.scan(
    FilterExpression="contains(#id, :fut)",
    ExpressionAttributeNames={"#id": "id"},
    ExpressionAttributeValues={":fut": "#futures"}
)
items = response['Items']

# Borra los que NO tienen la fecha de scraping al principio (solo 2 partes separadas por #)
borrados = 0
for item in items:
    id_parts = item['id'].split('#')
    if len(id_parts) == 2:  # Formato antiguo: fecha_venc#futures
        print(f"Borrando: {item['id']}")
        table.delete_item(Key={'id': item['id']})
        borrados += 1

print(f"¡Registros antiguos eliminados! Total: {borrados}") 