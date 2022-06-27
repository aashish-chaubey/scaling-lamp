# Scaling Lamp

A Flask application for doing the basic operations on PostGres DB (or any database) using SQLAlchemy (as ORM library), Swagger (document and automating REST APIs), and Sphinx (For code level documentations).

### Steps to run this file

---

1. Create a virutal environment and switch into the virtual environment  
    + `python -m pip install virutalenv`  
    + `python -m venv .venv`
    + `source activate .venv/bin/activate`

2. Install the required packages
    + `pip install -r requirements.txt`

3. Grant the *run.sh* execute privilidges
    + `chmod u+x run.sh`

4. Do the required configuration changes in *database.conf* file matching the values passed in the *docker-compose.yml file*

5. Build the database images using the *Dockerfile*
    + `docker build -f Dockerfile -t postgres_customimage .`

6. Pull up the database containers using **docker-compose**
    + `docker-compose up --detach`


