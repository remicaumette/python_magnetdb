# MagnetDB

Tools for creating and manipulating a database designed for Magnet simulations.
Data may be partly retreived from **Lncmi control and monitoring website**.
See `python_magnetrun` for more details

## Development setup

0. Pre-requisites

On your host:
```shell
echo "127.0.0.1 handler.sso.lncmig.local api.manager.sso.lncmig.local manager.sso.lncmig.local sso.lncmig.local test.sso.lncmig.local" | sudo tee -a /etc/hosts
```

Create a self signed certificate for the magnetdb server:
   
```shell
mkdir -p certs
cd certs
mkcerts -CAROOT
mkcerts ...
mkcerts -install
chmod 600 certs/*.key
```


1. Install python dependencies:

```shell
poetry install
```

2. Start dependencies with docker:

```shell
docker-compose -f docker-compose-dev-traefik-ssl.yml up
```

Note: if you see error messages about pgadmin, try to fix permissions on pgadmin-data directory by running `sudo chown -R 5050:5050 pgadmin-data`

5. Configure LemonLDAP (https://github.com/LemonLDAPNG/lemonldap-ng-docker):
   1. Sign in to https://auth.lemon.magnetdb-dev.local/ with dwho/dwho
   2. Enable OpenID Connect in Administration > WebSSO Manager > General Parameters > Issuer modules > OpenID Connect
   3. Create OpenID relying party in Administration > WebSSO Manager > OpenID Connect Relying Parties > Add OpenID Relying Party
   4. Go in Administration > WebSSO Manager > OpenID Connect Relying Parties > "Name of the relying party" > Options > Basic
   5. Set Client ID to `testid`
   6. Set Client secret to `testsecret`
   7. Set Allowed redirection addresses for login to `https://magnetdb-dev.local/sign_in`


3. Setup Minio bucket:
   1. Sign in to https://minio.magnetdb-dev.local/ with minio/minio123
   2. Create bucket on https://minio.magnetdb-dev.local/add-bucket

4. Run migrations:

 Connect to magnetdb-api container

```shell
poetry run orator migrate -c python_magnetdb/database.py
```


<!--
6. Setup front-end:
   
```shell
cd web
npx browserslist@latest --update-db
sudo npm install --location=global npm@8.13.2
yarn install
cd ..
```


7. Start front-end:

```shell
cd web
export API_ENDPOINT=http://localhost:8000
yarn serve
```

8. Start back-end:

```shell
export API_ENDPOINT=http://localhost:8000
export S3_ENDPOINT=localhost:9000 S3_ACCESS_KEY=minio S3_SECRET_KEY=minio123 S3_BUCKET=magnetdb
poetry run uvicorn python_magnetdb.web:app --reload --log-level=debug
```

9. Start worker:

```shell
export API_ENDPOINT=http://localhost:8000
export S3_ENDPOINT=localhost:9000 S3_ACCESS_KEY=minio S3_SECRET_KEY=minio123 S3_BUCKET=magnetdb
export IMAGES_DIR=/images
poetry run watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- poetry run celery -A python_magnetdb.worker worker --loglevel=INFO
```
-->

7. Run seeds:

   To run this step you must have a '/data' directory. Connect to magnetdb-api container, check the directory is mounted, then
   
```shell
export DATA_DIR=/data
poetry run python3 -m python_magnetdb.seeds
poetry run python3 -m python_magnetdb.seed-again
poetry run python3 -m python_magnetdb.seed-records
```

8. PgAdmin setup

Load `https://pgadmin.magnetdb-dev.local/` in your web browser
add a server for magnetdb
   
magnetdb ip DB server shall be: `magnetdb-postgres`


