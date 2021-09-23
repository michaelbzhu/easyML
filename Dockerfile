FROM heroku/heroku:20

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential

RUN curl -fsSL https://pkgs.tangram.dev/stable/ubuntu/focal.gpg | apt-key add -
RUN curl -fsSL https://pkgs.tangram.dev/stable/ubuntu/focal.list | tee /etc/apt/sources.list.d/tangram.list
RUN apt-get update && apt-get install tangram

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN tangram --help

CMD ["gunicorn", "app:app"]