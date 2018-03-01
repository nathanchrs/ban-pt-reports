# BAN-PT Report Generator

An Odoo 10 add-on module which generates BAN-PT accreditation reports for STEI ITB from existing data on Odoo.

## Running using Docker in development

Prerequisites: [Docker Engine](https://docs.docker.com/engine/installation/) and [Docker Compose](https://docs.docker.com/compose/install/) must be installed; Internet access for pulling dependencies and Docker images.

Note: Docker commands might need root privileges/sudo.

1. Navigate to the project directory.
2. Run `docker-compose up` to start the application and its supporting services (PostgreSQL). Docker will download images if necessary.
3. Access Odoo on port 8069.
4. If this your first time running Odoo, a setup form will appear. Set up your account.

- To stop the containers, run `docker-compose stop`.
- To start the application again, simply run `docker-compose up` or `docker-compose up -d` to run in the background (if you don't need to recreate containers, you can also use `docker-compose start`).
- Use `docker ps` to see list of running containers.
- Use `docker exec -it <container_name> /bin/sh` or `docker-compose exec -it <service_name> /bin/sh` to get a shell on a running container.
- To remove the containers, run `docker-compose down`. To remove the containers and reset all data volumes (persistent data) too, run `docker-compose down -v`.

## Directory structure

- `src`: source for addon modules.
- `config`: Odoo config for development.
