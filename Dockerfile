# Especifica la imagen base para el contenedor
FROM python:3.8-slim-buster

# Establece el directorio de trabajo para las instrucciones siguientes
WORKDIR /powermeter

# Copia los archivos necesarios para la aplicación al contenedor
COPY powermeter/ powermeter/
COPY test/ test/
COPY manage.py .
COPY requirements.txt .

ENV DJANGO_SETTINGS_MODULE=powermeter.settings
# Create and activate the virtual environment
RUN python3 -m venv powermeter-venv

# Establecer el directorio del entorno virtual
ENV VIRTUAL_ENV /powermeter/powermeter-venv
ENV PYTHONPATH "$VIRTUAL_ENV/lib/python3.8/site-packages:$PYTHONPATH"
RUN . $VIRTUAL_ENV/bin/activate

# Instala las dependencias de la aplicació
RUN $VIRTUAL_ENV/bin/pip install --upgrade pip
RUN $VIRTUAL_ENV/bin/pip install wheel
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir Django --use-pep517
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir django-rest-framework --use-pep517
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir -r requirements.txt --use-pep517

# Expone el puerto 8000 para que la aplicación pueda recibir peticiones
# Especifica el comando para iniciar la aplicación
EXPOSE 9000

RUN mkdir static
ENV STATIC_ROOT /powermeter/static

RUN python3 manage.py collectstatic --no-input
RUN python3 manage.py migrate
# Iniciar el servidor de desarrollo de Django
CMD ["python3", "manage.py", "runserver", "0.0.0.0:9000"]
