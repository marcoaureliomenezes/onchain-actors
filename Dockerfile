FROM python:3.8-slim

WORKDIR /app

COPY ./requirements.txt .

RUN apt-get update && apt-get install nodejs -y
RUN apt-get install npm -y

RUN pip install --upgrade "pip==22.0.4" && \
    pip install -r requirements.txt

RUN pip install eth-brownie
RUN npm install -g ganache-cli

RUN brownie pm install uniswap/v2-periphery@1.0.0-beta.0
RUN brownie pm install uniswap/v2-core@1.0.1

COPY ./src .

RUN brownie compile

ENTRYPOINT [ "sleep", "infinity" ]