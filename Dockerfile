FROM python:3

RUN mkdir -p /usr/src/jaram-gaming-welcomebot
WORKDIR /usr/src/jaram-gaming-welcomebot


COPY . .
RUN pip3 install --no-cache-dir -r ./requirements.txt --default-timeout=100

ENTRYPOINT ["python3", "bot.py"]