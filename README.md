# MagnetDB

Tools for creating and manipulating a database designed for Magnet simulations.
Data may be partly retreived from **Lncmi control and monitoring website**.
See `python_magnetrun` for more details

## Development setup

5. Configure LemonLDAP (https://github.com/LemonLDAPNG/lemonldap-ng-docker):
   1. Sign in to http://auth.example.com/ with dwho/dwho
   2. Enable OpenID Connect in Administration > WebSSO Manager > General Parameters > Issuer modules > OpenID Connect
   3. Create OpenID relying party in Administration > WebSSO Manager > OpenID Connect Relying Parties > Add OpenID Relying Party
   4. Go in Administration > WebSSO Manager > OpenID Connect Relying Parties > "Name of the relying party" > Options > Basic
   5. Set Client ID to `testid`
   6. Set Client secret to `testsecret`
   7. Set Allowed redirection addresses for login to `http://localhost:8080/sign_in`

On your host:
```shell
echo "127.0.0.1 auth.example.com manager.example.com test1.example.com test2.example.com" | sudo tee -a /etc/hosts
```

This step has to be done prior with lemonldap base image
Then copy the conf files in the lemonldap-etc and lemonldap-var/conf directories 

1. Install python dependencies:
    ```shell
    poetry install
    cd python_magnetsetup
    poetry install
    cd ..
    ```

2. Start dependencies with docker:
    ```shell
    docker-compose up
    ```

3. Setup Minio bucket:
   1. Sign in to http://localhost:9080/ with minio/minio123
   2. Create bucket on http://localhost:9080/add-bucket

4. Run migrations:
    ```shell
    poetry run orator migrate -c python_magnetdb/database.py
    ```


6. Setup front-end:
   ```shell
    cd web
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
   export S3_ENDPOINT=localhost:9000 S3_ACCESS_KEY=minio S3_SECRET_KEY=minio123 S3_BUCKET=magnetdb
   poetry run uvicorn python_magnetdb.web:app --reload --log-level=debug
   ```

9. Start worker:
   ```shell
   export S3_ENDPOINT=localhost:9000 S3_ACCESS_KEY=minio S3_SECRET_KEY=minio123 S3_BUCKET=magnetdb
   poetry run celery -A python_magnetdb.worker worker --loglevel=info
   ```

10. Run seeds:

    Need to define `DATA_DIR`
    ```shell
    poetry run python3 -m python_magnetdb.seeds
    ```
