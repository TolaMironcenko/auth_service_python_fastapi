# Auth Service

## To start dev

```shell
python -m venv env
source env/bin/activate
pip install -r requirements.txt
fastapi dev main.py
```

## To start prod

```shell
python -m venv env
source env/bin/activate
pip install -r requirements.txt
fastapi run main.py
```

## To start with Docker

```shell
docker-compose up
```

## To only build docker image

```shell
docker build -t <docker images name> .
```

### You don't need to create superuser. Firt registered user will be a superuser
