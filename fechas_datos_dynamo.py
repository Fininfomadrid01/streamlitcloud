import boto3
from collections import Counter

TABLE_OPCIONES = 'dev-raw-prices'
TABLE_FUTUROS = 'futuros-table'
REGION = 'us-east-1'

client = boto3.client('dynamodb', region_name=REGION)

# Opciones
resp_opciones = client.scan(
    TableName=TABLE_OPCIONES,
    ProjectionExpression='#d, #t',
    ExpressionAttributeNames={'#d': 'date', '#t': 'type'}
)
fechas_opciones = [
    item['date']['S']
    for item in resp_opciones['Items']
    if 'type' in item and item['type']['S'] in ['call', 'put', 'calls', 'puts']
]
cont_opciones = Counter(fechas_opciones)

# Futuros
resp_futuros = client.scan(
    TableName=TABLE_FUTUROS,
    ProjectionExpression='#d',
    ExpressionAttributeNames={'#d': 'date'}
)
fechas_futuros = [item['date']['S'] for item in resp_futuros['Items']]
cont_futuros = Counter(fechas_futuros)

print("\n=== Fechas con datos de OPCIONES ===")
for fecha, count in sorted(cont_opciones.items()):
    print(f"{fecha}: {count} opciones")

print("\n=== Fechas con datos de FUTUROS ===")
for fecha, count in sorted(cont_futuros.items()):
    print(f"{fecha}: {count} futuros") 