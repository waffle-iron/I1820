# In The Name Of God
# ========================================
# [] File Name : route.py
#
# [] Creation Date : 26-08-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
import flask
import json
import datetime

from . import app
from ..things.base import Things
from ..log.log import I1820Logger


@app.route('/test')
def test_handler():
    return "18.20 is leaving us"


@app.route('/log', methods=['POST'])
def log_handler():
    data = flask.request.get_json(force=True)
    log = I1820Logger(
        datetime.datetime.fromtimestamp(data['timestamp']),
        data['data'],
        data['endpoint']
    )
    print(data)
    return ""


@app.route('/service/<string:name>', methods=['POST'])
def service_handler(name):
    pass


@app.route('/thing', methods=['POST', 'PUT'])
def thing_handler():
    data = flask.request.get_json(force=True)
    rpi_id = data['rpi_id']
    device_id = data['device_id']
    result = {}
    try:
        thing = Things.get(data['type'])(rpi_id, device_id)
    except ImportError as e:
        return ('%s is not one of our things: %s' % (data['type'], str(e)),
                400, {})
    if 'settings' in data.keys():
        for key, value in data['settings'].items():
            setattr(thing, key, value)
            result[key] = value
    if 'status' in data.keys():
        for key in data['status']:
            result[key] = getattr(thing, key)

    return json.dumps(result)
