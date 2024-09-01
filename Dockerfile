FROM python:3.9

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && pip install --no-cache-dir -r requirements.txt \
    && chmod +x /usr/src/app/wait-for-db.sh

EXPOSE 5000

ENTRYPOINT ["/usr/src/app/wait-for-db.sh"]
CMD ["flask", "run", "--host=0.0.0.0"]