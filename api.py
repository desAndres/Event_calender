from flask import Flask
from flask import request

app = Flask(__name__)

import model
import logic

_event_logic = logic.EventLogic()
class ApiException(Exception):
     pass


def _from_raw(raw_event: str) -> model.Event:
    parts = raw_event.split('|')
    if len(parts) == 3:
        event = model.Event()
        event.id = None
        event.date = str(parts[0])
        event.title = str(parts[1])
        event.text = str(parts[2])
        return event
    elif len(parts) == 4:
        event = model.Event()
        event.id = str(parts[0])
        event.date = str(parts[1])
        event.title = str(parts[2])
        event.text = str(parts[3])
        return event
    else:
        raise ApiException(f"invalid RAW note data {raw_event}")

def _to_raw(event: model.Event) -> str:
    if event.id is None:
        return f"{event.date}|{event.title}|{event.text}"
    else:
        return f"{event.id}|{event.date}|{event.title}|{event.text}"



API_ROOT = "/api/v1"
EVENT_API_ROOT = API_ROOT + "/event"

@app.route(EVENT_API_ROOT + "/", methods=["POST"])
def create():
    # return "create",201
    try:
        data = str(request.get_data())
        event = _from_raw(data)
        _id = _event_logic.create(event)
        return f"new id: {event.id}", 201
    except Exception as ex:
        return f"failed to CREATE with: {ex}", 404


@app.route(EVENT_API_ROOT + "/", methods=["GET"])
def list():
    try:
        events = _event_logic.list()
        raw_events = ""
        for event in events:
            raw_events += _to_raw(event) + '\n'
        return raw_events, 200
    except Exception as ex:
        return f"failed to LIST with: {ex}", 404


@app.route(EVENT_API_ROOT + "/<_id>", methods=["GET"])
def read(_id:str):
    try:
       event = _event_logic.read(_id)
       _raw_event = _to_raw(event)
       return _raw_event,200
    except Exception as ex:
        return f"failed to READ with: {ex}", 404


@app.route(EVENT_API_ROOT + "/<_id>", methods=["PUT"])
def update(_id:str):
    try:
        data = str(request.get_data())
        event = _from_raw(data)
        _event_logic.update(_id,event)
        return "updated", 200
    except Exception as ex:
        return f"failed to READ with: {ex}", 404


@app.route(EVENT_API_ROOT + "/<_id>", methods=["DELETE"])
def delete(_id:str):
    try:
        _event_logic.delete(_id)
        return "deleted", 200
    except Exception as ex:
        return f"failed to DELETE with: {ex}", 404

