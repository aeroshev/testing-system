FROM python:3.11.1-alpine3.17

# Set python environment
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off

# Create folder for sources
RUN mkdir "/code"
WORKDIR /code

# Update instruments
RUN python -m pip install --upgrade pip
RUN python -m pip install --upgrade setuptools
RUN python -m pip install --upgrade wheel
RUN python -m pip install poetry==1.3.1

# Copy dependncies
COPY poetry.lock pyproject.toml ./

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --without tests,lint --no-interaction --no-ansi

# Add sources
ADD src .

# Expose app port
EXPOSE 8000
