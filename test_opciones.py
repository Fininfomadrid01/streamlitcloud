import requests

url = "https://cyw9gfj3pf.execute-api.us-east-1.amazonaws.com/dev/opciones"
response = requests.get(url)

print("Status code:", response.status_code)
print("Texto bruto de la respuesta:")
print(response.text)

try:
    data = response.json()
    print("\nRespuesta interpretada como JSON:")
    print(data)
except Exception as e:
    print("\nNo se pudo interpretar como JSON:", e) 