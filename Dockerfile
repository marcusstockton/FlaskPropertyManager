# syntax=docker/dockerfile:1

FROM python:3.13-alpine AS base

ENV FLASK_APP=manage.py
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ADD . /app

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade -r requirements.txt --no-cache-dir
COPY . /app

# EXPOSE 5000
# EXPOSE 5678

######################
## Apply Migrations ##
######################
FROM base as migraions
RUN python manage.py db upgrade

##############
## Debugger ##
##############
FROM base AS debugger
RUN pip install debugpy

ENTRYPOINT [ "python", "-m", "debugpy", "--wait-for-client", "--listen", "0.0.0.0:5678", "-m", "flask", "run", "-h", "0.0.0.0", "-p", "5000" ]

#############
## Primary ##
#############
FROM base AS primary
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "manage:app"]