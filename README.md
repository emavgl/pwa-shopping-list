# Shopping list Web App (PWA)

## Description:

Shopping list with basic functionalities, add item, delete item.  
Why? It is simple to use, no login required. You click a button and you create a new Shopping List identified by a UUID.  
You can bookmark and share the link with the person you like.

Do you want an app? Save it as Progressive Web App.

## How to run

To debug

```
cd src/fastapi/app
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

To deploy

```
docker compose up --build
```

### More technical details

- On the docker-compose you will find also `caddy` to implement reverse proxy.
You need to set `DOMAIN` as environment variable.
- Uses `SQLite` as storage.
- Framework FastAPI
- Almost everything AI generated.
