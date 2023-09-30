FROM python:3.8
ENV PYTHONUNBUFFERED=1
ENV DOCKER=True
COPY . /ilmo
WORKDIR /ilmo
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
WORKDIR /ilmo/app