## Prerequisites

- Install sqitch: https://sqitch.org/download/
- Install PostgreSQL: https://www.postgresql.org/download/
- Install pgAdmin or any other PostgreSQL client to manage the database.

## Create a new database on a Docker container

Run the following command to create a new database:

```bash
 docker pull postgres:latest
```

- Run the postgres container. Make sure `~/workspace/fastsvelte/postgres` exists for the volume.

```bash
 docker run --name local-postgres \
  -e POSTGRES_USER=fastsvelte \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=fastsvelte \
  -v $HOME/workspace/fastsvelte-data/postgres:/var/lib/postgresql/data \
  -p 5432:5432 \
  -d postgres:latest
```


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


