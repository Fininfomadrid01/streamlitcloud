import boto3

# Configura tu región y nombres de tablas
REGION = 'us-east-1'
RAW_TABLE = 'dev-raw-prices'      # Tabla de futuros y opciones
IV_TABLE = 'dev-implied-vols'    # Tabla de IV

dynamodb = boto3.resource('dynamodb', region_name=REGION)

# Contar futuros
table = dynamodb.Table(RAW_TABLE)
response = table.scan(
    FilterExpression="contains(#id, :fut)",
    ExpressionAttributeNames={"#id": "id"},
    ExpressionAttributeValues={":fut": "#futures"}
)
futuros_count = len(response['Items'])

# Contar CALLs
response = table.scan(
    FilterExpression="contains(#id, :call)",
    ExpressionAttributeNames={"#id": "id"},
    ExpressionAttributeValues={":call": "#call#"}
)
calls_count = len(response['Items'])

# Contar PUTs
response = table.scan(
    FilterExpression="contains(#id, :put)",
    ExpressionAttributeNames={"#id": "id"},
    ExpressionAttributeValues={":put": "#put#"}
)
puts_count = len(response['Items'])

# Contar IVs
iv_table = dynamodb.Table(IV_TABLE)
response = iv_table.scan()
iv_count = len(response['Items'])

print(f"Futuros: {futuros_count}")
print(f"CALLs: {calls_count}")
print(f"PUTs: {puts_count}")
print(f"IVs: {iv_count}") 