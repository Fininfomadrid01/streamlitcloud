import boto3

# Configura tu región y nombre de la tabla

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla_futuros = dynamodb.Table('futuros-table')

# Escanea todos los registros
response = tabla_futuros.scan()
items = response['Items']

for item in items:
    # Si no tiene scrape_date, lo añadimos usando la fecha del campo 'date'
    if 'scrape_date' not in item or not item['scrape_date']:
        fecha_scrape = item.get('date', None)
        if fecha_scrape:
            tabla_futuros.update_item(
                Key={'id': item['id']},
                UpdateExpression="SET scrape_date = :s",
                ExpressionAttributeValues={':s': fecha_scrape}
            )
            print(f"Actualizado {item['id']} con scrape_date = {fecha_scrape}")

print("Actualización completada.") 