FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app
# Install dashboard dependencies
COPY dashboard/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY dashboard ./dashboard
COPY analytics ./analytics
COPY common ./common

# Streamlit port
EXPOSE 8501

CMD ["streamlit", "run", "dashboard/app.py", "--server.address=0.0.0.0", "--server.port=8501"]