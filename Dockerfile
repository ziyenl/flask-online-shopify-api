FROM python:3.9
#EXPOSE 5000 #Local Run
WORKDIR /app
COPY requirements.txt .
#RUN pip install -r requirements.txt #Local Run
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
#CMD ["flask", "run", "--host", "0.0.0.0"] #Local Run
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]
