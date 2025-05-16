import boto3
from datetime import datetime, timedelta

# Configura los nombres de las tablas y la región
TABLE_OPCIONES = 'dev-raw-prices'
TABLE_FUTUROS = 'futuros-table'
REGION = 'us-east-1'

# Calcula la fecha de ayer en formato YYYY-MM-DD
ayer = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')

# Crea el cliente de DynamoDB
client = boto3.client('dynamodb', region_name=REGION)

# Consulta opciones
resp_opciones = client.scan(
    TableName=TABLE_OPCIONES,
    FilterExpression='#d = :fecha and (#t = :call or #t = :put or #t = :calls or #t = :puts)',
    ExpressionAttributeNames={'#d': 'date', '#t': 'type'},
    ExpressionAttributeValues={
        ':fecha': {'S': ayer},
        ':call': {'S': 'call'},
        ':put': {'S': 'put'},
        ':calls': {'S': 'calls'},
        ':puts': {'S': 'puts'}
    }
)

# Consulta futuros
resp_futuros = client.scan(
    TableName=TABLE_FUTUROS,
    FilterExpression='#d = :fecha',
    ExpressionAttributeNames={'#d': 'date'},
    ExpressionAttributeValues={':fecha': {'S': ayer}}
)

print(f"\n=== Comprobación de datos para {ayer} ===")
print(f"Opciones encontradas: {len(resp_opciones['Items'])}")
print(f"Futuros encontrados: {len(resp_futuros['Items'])}")

if resp_opciones['Items']:
    print("- Hay datos de opciones para ayer.")
else:
    print("- NO hay datos de opciones para ayer.")

if resp_futuros['Items']:
    print("- Hay datos de futuros para ayer.")
else:
    print("- NO hay datos de futuros para ayer.") 