FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY pyproject.toml uv.lock ./

# Install project dependencies
RUN pip install uv && uv sync --frozen

COPY producer ./producer
COPY common ./common

CMD ["uv", "run", "python", "producer/main.py"]