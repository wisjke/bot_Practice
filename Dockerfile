FROM python:3.12-alpine3.21

WORKDIR /usr/src/app

COPY . .
RUN pip install  --no-cache-dir -r requirements.txt

CMD ["python", "-u", "./main.py"]