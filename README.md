# BAN-PT Report Generator

An Odoo 10 add-on module which generates BAN-PT accreditation reports for STEI ITB from existing data on Odoo.

## Running using Docker in development

Prerequisites: [Docker Engine](https://docs.docker.com/engine/installation/) and [Docker Compose](https://docs.docker.com/compose/install/) must be installed; Internet access for pulling dependencies and Docker images (note: proxy might cause problems).

Note: Docker commands might need root privileges/sudo. If this happens, you probably need to add your user to the `docker` group.

1. Clone this repository.
2. Navigate to the project directory.
3. Run `docker-compose up` to start the application and its supporting services (PostgreSQL). Docker will download images if necessary.
4. Access Odoo on port 8069. If this is your first time running Odoo, a setup page will appear. Go to 'Setting up Odoo' section below.

- To stop the containers, run `docker-compose stop`.
- To start the application again, simply run `docker-compose up` or `docker-compose up -d` to run in the background (if you don't need to recreate containers, you can also use `docker-compose start`).
- Use `docker ps` to see list of running containers.
- Use `docker exec -it <container_name> /bin/sh` or `docker-compose exec -it <service_name> /bin/sh` to get a shell on a running container.
- To remove the containers (reset all config and data), run `docker-compose down`. To remove the containers and reset all data volumes (persistent data) too, run `docker-compose down -v`.

### Setting up Odoo

1. Open Odoo on port 8069 in the browser (`localhost:8069` if running Docker directly on the host, replace `localhost` with the host VM's IP address if using VM to run Docker (e.g. with Docker Toolbox)). A setup page will appear.
2. Fill in a database name to be created (any name) and info for creating the administrator user, then submit the form.
3. You will be logged in as the administrator. Click the `Apps` menu in the top menu bar. Find the applications and custom modules you want to install (`BAN-PT Report Generator`, STEI iBOS modules).
4. Install each app/custom module as needed.
5. Go to `Settings` page by clicking the menu in the top menu bar. Go to `Users` page by clicking the menu in the left sidebar. Add new users as needed. Don't forget to give access rights to the users (for this module, tick `BAN-PT Report Generator / Manager` for full access or `BAN-PT Report Generator / Viewer` for read only access to the reports).

## Directory structure

- `code_generator`: Python script for generating views and other data files from models.
- `config`: Odoo config for development.
- `src`: source for addon modules.
- `src/banpt_report_generator/models`: model files - define data schema and queries.
- `src/banpt_report_generator/security`: security (groups, access rights) configuration.
- `src/banpt_report_generator/views`: define Odoo views - how to display the data.

## Development guide

### How to add a new table

1. Ensure you are on the `master` branch (`git checkout master`). Create a new branch (`git checkout -b <BRANCH_NAME>`). Branch name for a table must be equal to `table_` followed by the table code in lower case and with symbols replaced with underscore (e.g. `table_3a_3_1_1`).
2. Create model file in `src/banpt_report_generator/models` directory.
3. Run the code generator: `cd code_generator`, then `python code_generator.py`. Don't forget to return to the main directory using `cd ..`.
4. Check changes by running a Git diff, ensure all of the changes are correct.
5. Restart the Docker containers if they are running (`Ctrl+c` any running Docker Compose processes, then `docker-compose up` again).
6. Open Odoo in the browser, then go to `Apps` menu in the top navigation bar.
7. Search for `BAN-PT Report Generator` module, open it, then click `Upgrade`.
8. Stage (`git add --all`), commit (`git commit -m <COMMIT_MESSAGE>`, and push changes to Git (`git push -u origin <BRANCH_NAME>`), then make a new pull request to `master` on Github.

### How to refresh changes in Odoo

1. Restart the Docker containers if they are running (`Ctrl+c` any running Docker Compose processes, then `docker-compose up` again).
2. Open Odoo in the browser, then go to `Apps` menu in the top navigation bar.
3. Search for `BAN-PT Report Generator` module, open it, then click `Upgrade`.

- Changes to the Python code (e.g. models) requires the Odoo Docker container to be restarted.
- Changes to other types of files requires the module to be upgraded.

### Code generator

Automatically create views, imports, manifest, and model access files from model files.
To run, `cd code_generator`, then `python code_generator.py`.
Check changes first by running a Git diff before committing.

### pgAdmin

A pgAdmin 4 container is provided on port 5050. Use `odoo` as the username and password.
After login, add new server. Use `postgres` as the hostname, `odoo` as the user and password.
Note: the pgAdmin instance can't be used for backup or restore since the PostgreSQL binaries are installed in a separate container.

### Restore/Import sample DB to the PostgreSQL container

1. Ensure the PostgreSQL container is running (`docker-compose up`).
2. Get the name of the PostgreSQL Docker container using `docker ps` (should be like `banptreports_postgres_1`).
3. Create the database if it does not exist yet: `docker exec -i <POSTGRESQL_CONTAINER_NAME> createdb -U odoo <DESTINATION_DB>`.
4. Run `docker exec -i <POSTGRESQL_CONTAINER_NAME> -U odoo <DESTINATION_DB> < <FILE_TO_IMPORT_FROM_HOST>`.
