ARG PYTHON_VERSION=3.12.0
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /hrstop

# Install system dependencies
RUN apt-get update && apt-get install -y \
   build-essential \
   pkg-config \
   default-libmysqlclient-dev && \
   rm -rf /var/lib/apt/lists/* 

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8003

# Run the application.
CMD uvicorn hrstop.asgi:application --reload