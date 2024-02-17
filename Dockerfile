
FROM python:3.10

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8039

WORKDIR /apppython3 -m venv venv


COPY . /app

RUN python -m venv venv && \
    /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8039

CMD ["python", "app.py"]

