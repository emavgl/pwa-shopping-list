FROM python:3.9

WORKDIR /code/app

COPY ./app /code/app

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Create a volume for the SQLite database
VOLUME /code/app/data

# Update the database path in your app to use the volume location
ENV DATABASE_URL="sqlite:///./data/shopping_list.db"

CMD ["fastapi", "run", "main.py", "--proxy-headers", "--port", "8000"]