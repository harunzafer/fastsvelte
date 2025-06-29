## Prerequisites

- Install sqitch: https://sqitch.org/download/
- Install PostgreSQL: https://www.postgresql.org/download/
- Install pgAdmin or any other PostgreSQL client to manage the database.

## Create a new database on a Docker container

Run the following command in the root of your project to create a new database using Docker:

```bash
 docker-compose up -d
```

## Create a new change with Sqitch
To create a new change with Sqitch, run the following command:

```bash
sqitch add <change_name> -n "<description>"
```

## Deploy the changes to the database
To deploy the changes to the database, run the following command:
```bash
./sqitch.sh dev deploy
```

This will apply all the changes in the `deploy` directory to the `DATABASE_URL_DEV` database specified in the `.env` file.

## Revert the changes from the database
To revert the changes from the database, run the following command:
```bash
./sqitch.sh dev revert --to <change_name>
```

## Why do we have `sqitch.sh` script?
The `sqitch.sh` script is a convenience script to run Sqitch commands with the correct environment variables set. It allows you to run Sqitch commands without having to specify the database URL every time. The script sets the `DATABASE_URL` environment variable based on the argument passed to it (`dev`, `beta`, `gamma`, or `prod`). 

By default `sqitch revert` will revert all changes. This is very dangerous even in development if you have data in the database. `sqitch.sh` script will not allow you to revert all changes. You must specify a change name to revert to. This is to prevent accidental data loss.

Finally, the script will force to have `BEGIN;` and `COMMIT;` statements in the SQL files. This is to ensure that the changes are applied in a transaction, which is a good practice to avoid partial changes in case of errors. sqitch generates the `BEGIN;` and `COMMIT;` statements automatically, but I've expeerienced deleting them accidentally while editing the SQL files. That's why the script will force to have them in the SQL files.


## Create a New Database from an Existing Database with Schema Only

Download the public schema with the following command:

Connect to the DB with pgadmin or similar and run the following command to create the user:

```sql
CREATE USER neondb_owner WITH SUPERUSER PASSWORD '<some_password>';
```

```bash
pg_dump -h hostname -U neondb_owner -d fastsvelte --schema-only --schema=public --schema=sqitch > public_schema.sql
```

Copy file to the docker container:

```bash
docker cp final_dump.sql local-postgres:/tmp/public_schema.sql
```


Once the database is created, you can restore the schema using:

```bash
docker exec -i local-postgres psql -U admin -d fastsvelte -f /tmp/public_schema.sql
```


