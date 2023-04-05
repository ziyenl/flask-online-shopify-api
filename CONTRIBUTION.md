# Running the flask app
1.  After git clone, run the following commands:
- `flask run`: runs the flask app
- `flask db init`: interacts with alembic to create the migrations folder)
- `flask  db migrate`: compare existing database model and create the script to go from one revision to the other
- `flask db upgrade`: applies the changes to the database

2. To use docker, you can build the docker image
- `docker build -t <IMAGE_NAME> .`: builds the docker image
- `docker run -dp 5007:5000 -w /app -v "$(pwd):/app" <IMAGE_NAME> sh -c "flask run"`: creates the docker container and run it using flask

3. If you need to use a different db, set the setting through .env