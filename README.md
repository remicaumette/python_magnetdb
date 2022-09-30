# MagnetDB

Tools for creating and manipulating a database designed for Magnet simulations.
Data may be partly retreived from **Lncmi control and monitoring website**.
See `python_magnetrun` for more details

## Development setup

0. Pre-requisites

On your host:
```shell
echo "127.0.0.1 handler.sso.grenoble.lncmi.local api.manager.sso.grenoble.lncmi.local manager.sso.grenoble.lncmi.local sso.grenoble.lncmi.local test.sso.grenoble.lncmi" | sudo tee -a /etc/hosts
```

Create a self signed certificate for the magnetdb server:
   
```shell
mkdir -p certs
openssl req -new -x509 -days 365 -nodes -out certs/cert.pem -keyout certs/cert.key
chmod 600 certs/cert.perm certs.cert.key
```

```shell
docker network create nginx-proxy
docker run -d -p 80:80 -p 443:443 -v $PWD/certs:/etc/nginx/certs -v /var/run/docker.sock:/tmp/docker.sock:ro --name my-nginx-proxy --net nginx-proxy jwilder/nginx-proxy
```

1. Start the services

```shell
docker-compose up
```

The first time you run the service, you would need to:

* Fix the premissions for pgadmin-data

```shell
sudo chown -R 5050:5050 pgadmin-data
```

2. Create/Update Database

```shell
docker exec -it remi_magnetdb_web-api_1 /bin/bash
```

In the container, to perform database migration run:

```shell
poetry run orator migrate -c python_magnetdb/database.py
```

Eventually, run seeds to populate the database

```shell
export DATA_DIR=/data
poetry run python3 -m python_magnetdb.seeds
poetry run python3 -m python_magnetdb.seed-again
poetry run python3 -m python_magnetdb.seed-records
```
    
3. Configure LemonLDAP (https://github.com/LemonLDAPNG/lemonldap-ng-docker):
   1. Sign in to http://sso.grenoble.lncmi.local/ with dwho/dwho
   2. Enable OpenID Connect in Administration > WebSSO Manager > General Parameters > Issuer modules > OpenID Connect
   3. Create OpenID relying party in Administration > WebSSO Manager > OpenID Connect Relying Parties > Add OpenID Relying Party
   4. Go in Administration > WebSSO Manager > OpenID Connect Relying Parties > "Name of the relying party" > Options > Basic
   5. Set Client ID to `testid`
   6. Set Client secret to `testsecret`
   7. Set Allowed redirection addresses for login to `http://localhost:8080/sign_in`

4. Setup pgadmin

Load `localhost:5050/` in your web browser
add a server for magnetdb
   
Check magnetdb ip server with: `docker inspect postgres-app  | grep IPAddress`


