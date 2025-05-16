import boto3
from datetime import datetime, timedelta

# Configura los nombres de las tablas y la región
TABLE_OPCIONES = 'dev-raw-prices'
TABLE_FUTUROS = 'futuros-table'
TABLE_IV = 'dev-implied-vols'
REGION = 'us-east-1'

# Calcula la fecha de hoy y ayer en formato YYYY-MM-DD
hoy = datetime.utcnow().strftime('%Y-%m-%d')
ayer = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')

client = boto3.client('dynamodb', region_name=REGION)

def contar_registros(tabla, fecha):
    resp = client.scan(
        TableName=tabla,
        FilterExpression='#s = :fecha',
        ExpressionAttributeNames={'#s': 'scrape_date'},
        ExpressionAttributeValues={':fecha': {'S': fecha}}
    )
    return len(resp['Items'])

print(f"\n=== Comparativa de registros para HOY ({hoy}) y AYER ({ayer}) ===")

opciones_hoy = contar_registros(TABLE_OPCIONES, hoy)
opciones_ayer = contar_registros(TABLE_OPCIONES, ayer)
futuros_hoy = contar_registros(TABLE_FUTUROS, hoy)
futuros_ayer = contar_registros(TABLE_FUTUROS, ayer)
iv_hoy = contar_registros(TABLE_IV, hoy)
iv_ayer = contar_registros(TABLE_IV, ayer)

print(f"Opciones: HOY = {opciones_hoy} | AYER = {opciones_ayer}")
print(f"Futuros:  HOY = {futuros_hoy} | AYER = {futuros_ayer}")
print(f"IV:       HOY = {iv_hoy} | AYER = {iv_ayer}") 