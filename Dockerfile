# Dockerfile para la aplicación IV-Smile con Streamlit
FROM python:3.9-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

<<<<<<< HEAD
=======
RUN mkdir -p /app/output

>>>>>>> 95a938ce09fc569840d0b2f203f60294e36a4bbf
# Copiar y instalar dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app/ ./app/
<<<<<<< HEAD
COPY output/ ./output/
=======
>>>>>>> 95a938ce09fc569840d0b2f203f60294e36a4bbf

# Exponer el puerto que usará Streamlit
EXPOSE 8501

# Comando de arranque
CMD ["streamlit", "run", "app/iv_smile_app.py", \
<<<<<<< HEAD
     "--server.port", "8501", "--server.address", "0.0.0.0"]
=======
     "--server.port", "8501", "--server.address", "0.0.0.0", "--server.headless", "true", "--server.enableCORS", "false"]
>>>>>>> 95a938ce09fc569840d0b2f203f60294e36a4bbf
