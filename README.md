# Pyhacid

Python NCID client with Home Assistant support. Use HA REST API to announce CallerID

## Getting Started

You will need an NCID server (AKA ncidd) setup and connected to your modem.

### Prerequisites

You just need docker installed, then you need to configure the following variables

```
NCID_HOST=127.0.0.1
NCID_PORT=3333

HA_URL=https://ha.example.com/api/
HA_TOKEN=your_token_here

ALEXA_ANNOUNCE=True
ALEXA_PUSH=True
ALEXA_TARGETS=media_player.kitchen,media_player.lounge

NOTIFY_SERVICES=lounge_tv

MESSAGE_TEMPLATE="{cid} is calling."
ALEXA_TITLE="Call on Home Phone"
```

You can get a token from the Home Assistant User Profile page under the section marked "Long lived tokens".

### Installing

You have two options, run locally or run under Docker. Either way make sure you have setup the environment variables listed above, all are required bu ncid_host and ncid_port have reasonable defaults that should work in many situations.

To install locally run:

```
pipenv install -r requirements.txt
pipenv run python app.py
```

Or using docker (remember to set env variables!)

```
docker run chrisfranklin/pyhacid
```

## Built With

* [Python](http://python.org) - Programming language
* [Requests](python-requests.org) - HTTP for humans
* [NCID](http://ncid.sourceforge.net) - Network Caller ID

## Contributing

Yes please, all contributions welcome from anyone kind enough to help.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/chrisfranklin/pyhacid/tags). 

## Authors

See the list of [contributors](https://github.com/hairychris/pyhacid/contributors) who participated in this project.
