# Telemetry

[![CircleCI](https://circleci.com/gh/jupyter/telemetry.svg?style=svg)](https://circleci.com/gh/jupyter/telemetry)
[![codecov](https://codecov.io/gh/jupyter/telemetry/branch/master/graph/badge.svg)](https://codecov.io/gh/jupyter/telemetry)

Telemetry for Jupyter Applications and extensions.

## Basic Usage


### Configuring Eventlog

```python
allowed_schemas = [
    ()
    {}
]
```


```python
allowed_schemas = [
    # Schema ID
    ('my.events/set1/event1', ['start', 'stop'], []),
    ('my.events/set2/event2', [], [])
]
```

Route events to various event logs:
```python
import logging
from jupyter_telemetry import EventLog, EventRouter

router = EventRouter([
    EventLog(
        handlers=[
            logging.FileHandler('events_set1.log')
        ],
        allowed_schemas=[
            'my.events/set1/event1',       # all events are coming from set 1.
            'my.events/set1/event2',
        ]
    ),
    Eventlog(
        handlers=[
            logging.FileHandler('events_set2.log')
        ],
        allowed_schemas=[
            'my.events/set1/event1',       # all events are coming from set 2.
            'my.events/set1/event2',
        ]
    )
])

# Log an event to 'events_set1.log' but not 'events_set2.log'
router.record_event(
    'my.events/set1/event1', 1,
    {...}
)
```





c.Eventlog = []

```

```python

from jupyter_telemetry import instrument, record

class MyClass():

    eventlog = EventLog()
    eventschema = "my.url.to.schema/actions"
    eventkeys = [""]

    def method_to_record():

```






## Defining a schema


Event schemas are written in YAML (or JSON) and require the following keys: 

1. `$id`: the source where this schema lives. Must be a valid URL. 
2. `version`: version of this schema.
3. `title`: a descriptive title of the schema.
4. `description`: a description of what kind of events this schema defines.
5. `type`: should always be set to `object`.
6. `required`: lists the properties that are required+emitted by the 
7. `properties`: the data included in the emitted event capsule.
    - The properties field requires one key, `action`, with the type set to `string`.
    - `action`: the type of event to emit.


Example: 
```yaml
"$id": my.url.to.schema/actions
version: 1
title: Actions emitted by my application
description: |
  Record actions from by application
type: object
required:
- action
properties:
  action:
    type: string
    enum:
    - say-hello
    - say-goodbye
    description: |
      Action performed by JupyterHub.

      This is a required field.

      Possible values:

      1. start
         A user's server was successfully started
      2. stop
         A user's server was successfully stopped
  name:
    type: string
    description: |
      Name of the user who did the action
```

