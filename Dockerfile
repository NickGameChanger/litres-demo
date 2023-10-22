FROM python:3.9

WORKDIR /app

COPY requirements.txt .

ENV PYTHONPATH ./app

RUN pip3 install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"


COPY . .

CMD [ "python", "/api/core.py" ]

EXPOSE 8079