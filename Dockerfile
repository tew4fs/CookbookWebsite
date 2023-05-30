FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV APP_HOME=/app

COPY . $APP_HOME
WORKDIR $APP_HOME

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev

EXPOSE 8000

RUN python -m pip install pipenv && \
    pipenv install --deploy --ignore-pipfile

#RUN pipenv run python manage.py migrate

RUN chmod -R 755 $APP_HOME

CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]