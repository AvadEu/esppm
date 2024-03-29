FROM python:3.11-slim

WORKDIR /core

ENV PYTHONBUFFERED 1

RUN python -m venv .venv
RUN /bin/bash -c "source ./.venv/bin/activate"

COPY requirements.txt ./

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.api.application:app", "--host", "0.0.0.0", "--port", "4200"]