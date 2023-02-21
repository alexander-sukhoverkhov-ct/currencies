FROM python:3.11-alpine
RUN python -m venv /opt/venv && \
    pip install --upgrade pip setuptools wheel
ENV PATH="/opt/venv/bin:$PATH"
COPY src/ /app
WORKDIR /app/

# Зависимости времени выполнения
COPY requirements.txt .
RUN pip install -r requirements.txt
