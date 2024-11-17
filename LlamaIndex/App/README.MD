# To spin this app up:

## Backend
Start by installing requirements
```
cd ./backend/_app
poetry shell init
poetry install
cd ../
```

Spin up the backend using docker
```
docker compose -f ./kafka/docker/docker-compose.yml --project-directory ./ up --build -d
```

To spin down the backend
```
docker compose -f ./kafka/docker/docker-compose.yml --project-directory ./ down
```

## Frontend
Start by installing requirements
```
pip install -r requirements.txt
```

Execute frontend
```
chainlit run app.py --port 8080
```