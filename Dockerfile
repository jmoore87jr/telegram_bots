# Install the base requirements for the app.
# This stage is to support development.
FROM python:3.9.4-slim-buster AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "app/labsTelegramBot.py" ]