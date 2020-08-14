# TradingView Alerts

This aims to forward tradingview alerts into messages to other apps, queues or bots. Exposes an HTTP(S) endpoint and configured out of the box to support Telegram and RabbitMQ forwarders.

## Required Env Vars

| Name | Description |
| :--- | :--- |
| `FORWARDER` | Required string, valid options are `telegram` and `rabbitmq` |

## Forwarders

Here are the available forwarders.

### Telegram

Alerts are forwarded to a Telegram chat. You can get your own Telegram bot to receive the alert by following the steps [here](https://core.telegram.org/bots). Start a chat to your bot after creating one.

#### Env Vars

| Name | Description |
| :--- | :--- |
| `TELEGRAM_TOKEN` | Required string |
| `TELEGRAM_CHAT_ID` | Required string |

### RabbitMQ

Alerts are forwarded to the default exchange. Once published to RabbitMQ, this is where the fun begins.

#### Env Vars

| Name | Description |
| :--- | :--- |
| `AMQP_CONN_STRING` | Required string |
| `AMQP_QUEUE` | Required string, also known as routing key |

## Endpoint

The exposed endpoint is `[POST] /webhook` with these key/value pair expected to exist in a JSON body:

| Name | Description |
| :--- | :--- |
| `close` | Last close when alert is triggered, use `{{close}}` in TradingView |
| `indicator` | Indicator used for the alert, any string is accepted |
| `exchange` | Exchange used for the alert, use `{{exchange}}` in TradingView |
| `pair` | Pair used for the alert, use `{{ticker}}` in TradingView |
| `action` | Can either be `long` or `short` |

## Running

A compact bash script containing env vars is available called `run-local.sh`. Edit the contents and run this to develop locally. But first, do this.

```shell
$ python3 -m virtualenv
$ virtualenv env
$ . env/bin/activate
$ pip install -r requirements.txt
$ ./run-local.sh # Will silently fail when env vars are invalid
```

### Docker

Any commits pushed to the `master` branch will automatically push docker images to `tistaharahap/tv-alerts:latest`.

#### Telegram Forwarder

```shell
$ docker run -d --name tv-alerts -e FORWARDER=telegram -e TELEGRAM_TOKEN=your_token -e TELEGRAM_CHAT_ID=your_user_id tistaharahap/tv-alerts:latest 
```

#### RabbitMQ Forwarder

```shell
$ docker run -d --name tv-alerts -e FORWARDER=rabbitmq -e AMQP_CONN_STRING=your_conn_string -e AMQP_QUEUE=the_queue_or_routing_key tistaharahap/tv-alerts:latest 
```
