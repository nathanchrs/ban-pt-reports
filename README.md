# BAN-PT Report Generator

An Odoo 10 add-on module which generates BAN-PT accreditation reports for STEI ITB from existing data on Odoo.

## Catatan untuk Penilaian IF3250 PPL

- Repositori di [Gitlab IF](http://gitlab.informatika.org/IF3250-I-1/banpt_report_generator) merupakan hasil pemindahan repositori secara manual (*add remote*) dari repositori di [Github](https://github.com/nathanchrs/ban-pt-reports).
- *Pull request* di Github tidak dapat di-*import*, karena fitur *import from Github* pada Gitlab IF *error* jika digunakan. Agar mudah dicari, semua *pull request* tetap dilakukan di Github.
- Direktori `src/itb_academic` dan `src/itb_hr` mengandung kode yang diberikan oleh `product owner`, sehingga seharusnya tidak diperhitungkan dalam pengukuran jumlah baris kode. Kedua direktori tersebut di-*commit* sementara untuk mempermudah *automated testing* dan konfigurasi CI.

## Running using Docker in development

Prerequisites: [Docker Engine](https://docs.docker.com/engine/installation/) and [Docker Compose](https://docs.docker.com/compose/install/) must be installed; Internet access for pulling dependencies and Docker images (note: proxy might cause problems).

Note: Docker commands might need root privileges/sudo. If this happens, you probably need to add your user to the `docker` group.

1. Clone this repository.
2. Navigate to the project directory.
3. Run `docker-compose up` to start the application and its supporting services (PostgreSQL). Docker will download images if necessary. Wait until all tests are done.
4. Access Odoo on port 8069. Login with `admin` as the username and password.

- To stop the containers, run `docker-compose stop`.
- To start the application again, simply run `docker-compose up` or `docker-compose up -d` to run in the background (if you don't need to recreate containers, you can also use `docker-compose start`).
- Use `docker ps` to see list of running containers.
- Use `docker exec -it <container_name> /bin/sh` or `docker-compose exec -it <service_name> /bin/sh` to get a shell on a running container.
- To remove the containers (reset all config and data), run `docker-compose down`. To remove the containers and reset all data volumes (persistent data) too, run `docker-compose down -v`.

### Setting up Odoo (for production)

Note: these steps are not needed if using the Docker development container.

1. Log in using an administrator account.
4. Install each app/custom module as needed.
3. Go to `Settings` page by clicking the menu in the top menu bar. Go to `Users` page by clicking the menu in the left sidebar. Add new users as needed. Don't forget to give access rights to the users (for this module, tick `BAN-PT Report Generator / Manager` for full access or `BAN-PT Report Generator / Viewer` for read only access to the reports).

## Directory structure

- `code_generator`: Python script for generating views and other data files from models.
- `config`: Odoo config for development.
- `src`: source for addon modules.
- `src/banpt_report_generator/models`: model files - define data schema and queries.
- `src/banpt_report_generator/security`: security (groups, access rights) configuration.
- `src/banpt_report_generator/views`: define Odoo views - how to display the data.

## Development guide

### How to add a new table

1. Ensure you are on the `master` branch (`git checkout master`). Create a new branch (`git checkout -b <BRANCH_NAME>`). Branch name for a table must be equal to the table code in lower case and with `-` replaced with `_` and `.` removed (e.g. `3a_311`).
2. Create model file in `src/banpt_report_generator/models` directory.
3. Run the code generator: `cd code_generator`, then `python code_generator.py`. Don't forget to return to the main directory using `cd ..`.
4. Check changes by running a Git diff, ensure all of the changes are correct.
5. Restart the Docker containers if they are running (`Ctrl+c` any running Docker Compose processes, then `docker-compose up` again).
6. Lint the code using `pylint src/banpt_report_generator` (requires `pylint` to be installed, see Linting section below). Fix all errors or warnings.
7. Run tests using `docker-compose -f docker-compose.test.yml up --abort-on-container-exit`, ensure there are no `ERROR` lines. Fix all errors.
8. Stage (`git add --all`), commit (`git commit -m <COMMIT_MESSAGE>`, and push changes to Git (`git push -u origin <BRANCH_NAME>`), then make a new pull request to `master` on Github.

### How to refresh changes in Odoo

Restart the Docker containers if they are running (`Ctrl+c` any running Docker Compose processes, then `docker-compose up` again). The `banpt_report_generator` module will be upgraded automatically.

### Linting

Prerequisite: [pylint](https://docs.pylint.org/en/1.8/user_guide/installation.html).
To lint, run `pylint src/banpt_report_generator`.
If there are any errors or warning, fix the source code before committing.

### Tests

Place your tests in the `src/banpt_report_generator/tests` directory, then import it in `src/banpt_report_generator/tests/__init__.py`.

To run tests, run `docker-compose -f docker-compose.test.yml up --abort-on-container-exit`. Check if there are any `ERROR` when the test finishes.

For convenience, to see only relevant test output, use `docker-compose -f docker-compose.test.yml up --abort-on-container-exit | grep banpt_report_generator`.

For automated testing, to return with a non-zero exit code on test failure, use `docker-compose -f docker-compose.test.yml up --abort-on-container-exit | grep FAIL; test $? -eq 1`.

### Code generator

Automatically create views, imports, manifest, and model access files from model files.
To run, `cd code_generator`, then `python code_generator.py`.
Check changes first by running a Git diff before committing.

### pgAdmin

A pgAdmin 4 container is provided on port 5050. Use `odoo` as the username and password.
After login, add new server. Use `postgres` as the hostname, `odoo` as the user and password.
Note: to use the pgAdmin instance for backup or restore, add `/usr/bin` as the PostgreSQL binary path in the `Preferences` menu in pgAdmin. Exported files are in the `/var/lib/pgadmin/storage/odoo` directory in the `pgadmin` container by default. Use `docker cp <PGADMIN_CONTAINER_NAME>:/var/lib/pgadmin/storage/odoo/<FILE_NAME> <DESTINATION_FILE_NAME>` to copy exported files from the container to the host.

### Restore/Import sample DB to the PostgreSQL container

1. Ensure the PostgreSQL container is running (`docker-compose up`).
2. In pgAdmin, expand server -> odoo -> Databases -> banpt -> Schemas -> public -> Tables (If server empty, create new server).
2. Add column in certain table (type: varchar).

| Tables                | Column            |
|-----------------------|:-----------------:|
| hr_employee           | nik               |
| itb_hr_assignment     | standard_id       |
| itb_hr_award          | standard_id       |
| itb_hr_duty_employee  | standard_id       |
| itb_hr_duty_employee  | research_group_id |
| itb_hr_project        | standard_id       |
| itb_hr_publication    | standard_id       |
| itb_hr_training       | standard_id       |

3. Download the file in https://drive.google.com/drive/u/1/folders/1SViDQyP-gfCJYOsdDJ7Pc9jWtREzFCYq (ibos2.sql)
4. Get the name of the PostgreSQL Docker container using `docker ps` (should be like `banptreports_postgres_1`).
5. Create the database if it does not exist yet: `docker exec -i <POSTGRESQL_CONTAINER_NAME> createdb -U odoo <DESTINATION_DB>`.
6. Run `docker exec -i <POSTGRESQL_CONTAINER_NAME> psql -U odoo -v ON_ERROR_STOP=1 <DESTINATION_DB> < <FILE_TO_IMPORT_FROM_HOST>`.
7. If failed, do the step from the beginning (`docker-compose down -v && docker-compose up`).

## Source/sample data notes

### Dosen
- Set correct dosen prodi IDs on `prodi` field of `hr.employee` model
- Add `gelar` field in `itb.hr_education` model

### Identitas
- Add missing fields to `itb_academic_program`
- Add table recording akreditasi BAN-PT results for each prodi

### Record 3a_5122
- Add `sks_mk_dalam_kurikulum_inti` field in `itb.academic_catalog` model
- Add `sks_mk_dalam_kurikulum_institusional` field in `itb.academic_catalog` model
- Add `bobot_tugas` field in `itb.academic_catalog` model
- Add `kelengkapan_sap` field in `itb.academic_catalog` model

### Record 3a_513
- Add `bobot_tugas` field in `itb.academic_catalog` model