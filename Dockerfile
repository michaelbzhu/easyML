FROM heroku/heroku:20

RUN curl -fsSL https://pkgs.tangram.dev/stable/ubuntu/focal.gpg | apt-key add -
RUN curl -fsSL https://pkgs.tangram.dev/stable/ubuntu/focal.list | tee /etc/apt/sources.list.d/tangram.list
RUN apt-get update && apt-get install tangram

