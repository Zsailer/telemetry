import io
import logging
import json
from traitlets.config import Application, Config
from jupyter_telemetry.eventlog import EventLog


class MyApp(Application):

    classes = [EventLog]

    def initialize(self):
        self.eventlog = EventLog(parent=self)
        self.eventlog.register_schema_file("example-schema.yml")

    def event_to_record(self):
        print("this was triggered")
        # Event logging object.
        event = {
            "name": "cool event"
        }
        self.eventlog.record_event(
            schema_name="example.schema",
            version=1,
            event=event
        )


output = io.StringIO()
handler = logging.StreamHandler(output)

def callback(eventlog, name, version, event):
    print(eventlog, name, version, event)
    breakpoint()


config = {
    "EventLog": {
        "allowed_schemas": ["example.schema"],
        "handlers": [handler],
        "subscriptions": {
            "example.schema": callback
        }
    }
}

app = MyApp(config=Config(config))
app.initialize()
app.event_to_record()

handler.flush()
event_capsule = json.loads(output.getvalue())

print(event_capsule)