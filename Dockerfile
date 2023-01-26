# Especifica la imagen base para el contenedor
FROM python:3.8-slim-buster

# Establece el directorio de trabajo para las instrucciones siguientes
WORKDIR /powermeter

# Instalar dependencias

COPY /powermeter .
COPY requirements.txt .
# Copia los archivos necesarios para la aplicación al contenedor
RUN chmod +x requirements.txt

# Create and activate the virtual environment
RUN python3 -m venv powermeter-venv

# Establecer el directorio del entorno virtual
ENV VIRTUAL_ENV /powermeter/powermeter-venv
RUN . $VIRTUAL_ENV/bin/activate

# Instala las dependencias de la aplicació
RUN $VIRTUAL_ENV/bin/pip install --upgrade pip
RUN $VIRTUAL_ENV/bin/pip install wheel
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir django-rest-framework --use-pep517
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir -r requirements.txt --use-pep517

# Expone el puerto 8000 para que la aplicación pueda recibir peticiones
EXPOSE 9000

# Especifica el comando para iniciar la aplicación
EXPOSE 9000

# Iniciar el servidor de desarrollo de Django
CMD ["python3", "/powermeter/manage.py", "runserver", "0.0.0.0:9000"]
