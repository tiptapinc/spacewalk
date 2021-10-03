FROM python:3.7-buster

RUN apt-get update && apt-get install -y telnet

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY example.sh example.sh
RUN chmod +x example.sh

COPY spacewalk spacewalk
COPY tests tests
COPY example.py example.py

ENTRYPOINT ["./example.sh"]
