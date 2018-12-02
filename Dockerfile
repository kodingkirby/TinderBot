FROM python:3.7

COPY requirements.txt /

RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

CMD ["python3", "main.py"]
#CMD ["python3", "main.py", "s", "15"] #Silent mode, run 15 times