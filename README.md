# SQE Robotic Welding Backend
Backend components of the robotic welding project:
| Component                                    | Used Technology                                                                    |
| ------------------------------------- | ---------------------------------------------------------------- |
| Web Framework                             | [FastAPI](https://github.com/tiangolo/fastapi)                      |
| Object Relational Mapping (ORM) | [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) |
| Database                                        | [PostgreSQL](https://www.postgresql.org)                            |
| Database Migrations                      | [Alembic](https://alembic.sqlalchemy.org/en/latest/)           |
| Testing                                            | [pytest](https://docs.pytest.org/en/7.1.x/)                             |

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

## Available variables and functions in templates
The templates are [Jinja2 templates](https://jinja.palletsprojects.com/en/3.1.x/templates/). 

 ### Variables
 The following list is an example input for templates:
```
welding_points": [{
        "id": 1,
        "project_id": 1,
        "robot_id": 1,
        "welding_order": 0,
        "name": "P1",
        "description": "Initial welding point",
        "x_original": 1.57,
        "y_original": 0,
        "z_original": 0.1,
        "x": 1.60,
        "y": 0.01,
        "z": 0.057,
        "x_rel": 1.046,
        "y_rel": -5.54,
        "z_rel": -15.454,
        "roll": 0.2,
        "pitch": 0.1,
        "yaw": 0.05,
        "tolerance": 0.1
    }],
"robot": {
        "id": 1,
        "robot_type_id": 1,
        "project_id": 1,
        "name": "Scratchy",
        "description": "Robot with the scratch on arm",
        "position_x": 0.554,
        "position_y": 5.554,
        "position_z": 15.554,
        "position_norm_vector_x": 0,
        "position_norm_vector_y": 0,
        "position_norm_vector_z": 1,
    }
 ```
Data can be accesed in templates with expressions: the robot name can be used as `{{robot.name}}`, and the first welding point description with `{{welding_points[0].description}}`. As the welding points are given as list, a loop can be used to iterate over it. 
 
 A note about the values `x_rel`, `y_rel`, `z_rel`: These values are the relative x, y and z positions as seen from the robot for this welding point. They are calculated with e.g., `x_rel = welding_point.x - robot.x`.
 
 ### Utility functions
 There is currently only one utility function available: `generate_blockly_block_id()`, which returns a 20 characters long random string. It can be used as ID for blockly blocks.
