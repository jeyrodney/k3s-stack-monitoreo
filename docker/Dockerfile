FROM python:3.11.11-slim

WORKDIR /code

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

#Esta liena no se requiere cuando se trabaja con docker-compose.yml, ya que desde allí se tira el comando con command
CMD ["waitress-serve", "--host", "0.0.0.0", "--port", "5000", "src.alert_listener:app"]