FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]

# Local use of flask as web server
#EXPOSE 5000 #Local Run
#WORKDIR /app
#COPY requirements.txt .
#RUN pip install -r requirements.txt
#COPY . .
#CMD ["flask", "run", "--host", "0.0.0.0"]

# using bash file as entry point
# CMD["/bin/bash", "docker-entrypoint.sh"]