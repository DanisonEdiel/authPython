FROM python:3.9-slim

WORKDIR /app

# Copiar solo los archivos necesarios para instalar dependencias primero
# para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Variable de entorno para Heroku
ENV PORT=5000

# Exponer el puerto que la aplicación utilizará (Heroku sobrescribirá esto)
EXPOSE $PORT

# Comando para ejecutar la aplicación con gunicorn
# Usando la variable PORT que proporciona Heroku
CMD gunicorn --bind 0.0.0.0:$PORT app:app
