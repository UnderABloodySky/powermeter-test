# Especifica la imagen base para el contenedor
FROM python:3.8-slim-buster

# Establece el directorio de trabajo para las instrucciones siguientes
WORKDIR /powermeter

# Instalar dependencias
COPY requirements.txt .
COPY /powermeter .
# Copia los archivos necesarios para la aplicación al contenedor
COPY . /test
RUN chmod +x /test/requirements.txt

# Create and activate the virtual environment
RUN python3 -m venv powermeter-venv

# Establecer el directorio del entorno virtual
ENV VIRTUAL_ENV /powermeter/powermeter-venv
RUN . $VIRTUAL_ENV/bin/activate

# Instala las dependencias de la aplicació
RUN $VIRTUAL_ENV/bin/pip install --upgrade pip
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir -r requirements.txt --use-pep517
RUN $VIRTUAL_ENV/bin/pip install django
RUN $VIRTUAL_ENV/bin/pip install django-rest-framework

# Expone el puerto 8000 para que la aplicación pueda recibir peticiones
EXPOSE 8000

# Especifica el comando para iniciar la aplicación
EXPOSE 8000

# Iniciar el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]
