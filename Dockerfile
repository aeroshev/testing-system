FROM python:3.11.1-alpine3.17

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off

RUN mkdir "/code"
WORKDIR /code

RUN python -m pip install --upgrade pip
RUN python -m pip install --upgrade setuptools
RUN python -m pip install --upgrade wheel
RUN python -m pip install poetry==1.3.1

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --without tests,lint --no-interaction --no-ansi

ADD src .

EXPOSE 8000

WORKDIR /code/testflow
