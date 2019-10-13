FROM ubuntu:latest

RUN apt-get update && apt-get install -y 
RUN apt-get install -y python3-pip
RUN pip3 install --no-cache-dir -r ./requirements.txt

ENTRYPOINT ["python3", "bot.py"]