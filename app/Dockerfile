FROM python:3.10-alpine AS app

ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir -U pip

WORKDIR /srv/app

COPY ./req/requirements.txt /srv/app/req/

RUN pip install --no-cache-dir -r ./req/requirements.txt

COPY ./ /srv/app

ENTRYPOINT ["./scripts/entrypoint.sh"]
