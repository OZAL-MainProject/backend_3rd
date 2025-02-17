FROM python:3.13-alpine3.21

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN apk update && apk add --no-cache postgresql-client bash

RUN apk add --no-cache curl

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"
ENV PATH="/usr/local/bin/:$PATH"

RUN chmod +x scripts/run.sh && \
    chmod -R 777 /app

RUN poetry install --no-root

CMD ["bash", "./scripts/run.sh"]

EXPOSE 8000