# syntax=docker/dockerfile:1

FROM python:3.12-alpine as base

ENV FLASK_APP=manage.py
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ADD . /app

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

# EXPOSE 5000
# EXPOSE 5678

##############
## Debugger ##
##############
FROM base as debugger
RUN pip install debugpy

ENTRYPOINT [ "python", "-m", "debugpy", "--wait-for-client", "--listen", "0.0.0.0:5678", "-m", "flask", "run", "-h", "0.0.0.0", "-p", "5000" ]

#############
## Primary ##
#############
FROM base as primary
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "manage:app"]