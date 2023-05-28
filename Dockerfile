FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV APP_HOME=/app

COPY . $APP_HOME
WORKDIR $APP_HOME

EXPOSE 8000

RUN python -m pip install pipenv && \
    pipenv install --deploy --ignore-pipfile

#RUN pipenv run python manage.py migrate

RUN chmod -R 755 $APP_HOME

CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]