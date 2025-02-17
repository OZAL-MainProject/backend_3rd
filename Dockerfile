FROM python:3.13

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
build-essential \
libpq-dev \
&& rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY . /app
COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock


RUN poetry install --no-root

ENTRYPOINT ["bash", "/app/scripts/run.sh"]