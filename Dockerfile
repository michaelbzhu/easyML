FROM heroku/heroku:20

RUN curl -fsSL https://pkgs.tangram.dev/stable/ubuntu/focal.gpg | sudo apt-key add -
RUN curl -fsSL https://pkgs.tangram.dev/stable/ubuntu/focal.list | sudo tee /etc/apt/sources.list.d/tangram.list
RUN sudo apt-get update && sudo apt-get install tangram

