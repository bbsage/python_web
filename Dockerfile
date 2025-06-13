FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt
COPY ./app ./app
COPY main.py main.py


FROM python:3.12-slim
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
RUN mkdir -p /root/.kube

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
