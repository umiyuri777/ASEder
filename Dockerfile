FROM python:3.11
WORKDIR /bot

RUN pip install --upgrade pip setuptools

COPY requirements.txt /bot/
RUN pip install -r requirements.txt

COPY . /bot
CMD ["python3", "main.py"]
