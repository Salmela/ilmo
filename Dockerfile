FROM python:3.8
ENV PYTHONUNBUFFERED=1
COPY --chmod=777 . /ilmo
WORKDIR /ilmo
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
WORKDIR /ilmo/app
EXPOSE 8000

VOLUME /ilmo/app/static/upload

CMD ["/bin/bash", "-c", "python3 manage.py makemigrations;python3 manage.py migrate;python3 manage.py runserver 0.0.0.0:8000"]
