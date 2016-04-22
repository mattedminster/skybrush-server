"""Default configuration for the Flockwave server."""

import os

IN_HEROKU = "DYNO" in os.environ

SECRET_KEY = b'\xa6\xd6\xd3a\xfd\xd9\x08R\xd2U\x05\x10'\
    b'\xbf\x8c2\t\t\x94\xb5R\x06z\xe5\xef'

EXTENSIONS = {
    "api.v1": {},
    "debug": {
        "route": "/debug"
    },
    "_fake_uavs": {
        "count": 3,
        "delay": 0.04 if IN_HEROKU else 2,
        "id_format": "FAKE-{0:02}",
        "center": {
            "lat": 47.473360,
            "lon": 19.062159,
            "alt": 20
        },
        "radius": 50,
        "time_of_single_cycle": 10
    },
    "flockctrl": {
        "id_format": "{0:02}",
        # "connection": "serial+replay:/Users/ntamas/dev/collmot/git/flockwave-server/test3.flight?autoclose=1"
        "connection": "serial:/tmp/xbee"
    }
}

if IN_HEROKU:
    if "_fake_uavs" in EXTENSIONS:
        EXTENSIONS["fake_uavs"] = EXTENSIONS.pop("_fake_uavs")
    del EXTENSIONS["flockctrl"]
