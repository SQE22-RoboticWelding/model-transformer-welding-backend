# SQE Robotic Welding Backend
Backend component of the robotic welding project. The backend is built with the 
web framework [FastAPI](https://github.com/tiangolo/fastapi), [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
is used for Object Relational Mapping (ORM) and [PostgreSQL](https://www.postgresql.org) as database. For database 
migrations we used [Alembic](https://alembic.sqlalchemy.org/en/latest/), which is associated with SQLAlchemy.
For tests, [pytest](https://docs.pytest.org/en/7.1.x/) is used.

## Project Structure
* **scripts:** Utility scripts for developing
* **src:** Source code of the backend
  * **alembic:** Database migrations and configuration of alembic
  * **app:** Backend application
    * **api:** Endpoints
    * **codegen:** Code generation implementation and utility based on Jinja2 templates
    * **core:** Core functionality, currently only application configuration
    * **crud:** CRUD base class and CRUD implementation for each entity
    * **db:** Everything related to the database connection. E.g. session objects or initialization of the databse itself
    * **models:** Code-First ORM entity classes
    * **parser:** Custom file parser for reading project files
    * **schemas:** DTO schemas
    * **templates:** Pre-defined templates for the codegen
    * **tests:** Tests for the application
    
## Prerequisites
- [Python 3.10+](https://www.python.org/downloads/release/python-3100/) (only when running locally)
- [Docker 20.10+](https://docs.docker.com/get-docker/)

## Building and running
For running as docker, execute from the repository root:
```shell
docker compose up -d --build
```
Or, for running locally, execute from the repository root:  
* Install dependencies first: `pip3 install -r src/requirements.txt`
* Start the database `docker compose up -d --no-deps sqe_database`
* Run the backend application with uvicorn: `cd src && uvicorn app.main:app`
* If you want to start the backend in development mode (hot reloading etc.) use `uvicorn app.main:app --reload` instead
