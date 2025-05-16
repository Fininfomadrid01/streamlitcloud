import boto3
import json

# Configura el nombre de la tabla y la región
TABLE_NAME = 'dev-raw-prices'
REGION = 'us-east-1'

# Crea el cliente de DynamoDB
client = boto3.client('dynamodb', region_name=REGION)

# Lee los datos ficticios del archivo JSON
with open('item_opciones_plural.json', 'r') as f:
    items = json.load(f)

# Inserta cada ítem en la tabla
for item in items:
    response = client.put_item(
        TableName=TABLE_NAME,
        Item=item
    )
    print(f"Insertado: {item['id']['S']} - Status: {response['ResponseMetadata']['HTTPStatusCode']}")

print("\nTodos los ítems han sido insertados correctamente.") 