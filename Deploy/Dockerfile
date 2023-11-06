FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y libpq-dev
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install
COPY . /app/
EXPOSE 8000
CMD ["poetry", "run", "gunicorn", "-w", "4", "main:app"]