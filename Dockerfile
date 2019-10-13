FROM ubuntu:latest

RUN mkdir -p /usr/src/jaram-gaming-welcomebot
WORKDIR /usr/src/jaram-gaming-welcomebot
RUN apt-get update && apt-get install -y 
RUN apt-get install -y python3-pip

COPY . .
RUN pip3 install --no-cache-dir -r ./requirements.txt

ENTRYPOINT ["python3", "bot.py"]