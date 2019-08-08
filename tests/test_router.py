import io
import pytest
import logging
from jupyter_telemetry.eventlog import EventLog
from jupyter_telemetry.router import EventRouter


TEST_SCHEMA_1 = {
    '$id': 'test/test1',
    'version': 1,
    'properties': {
        'something': {
            'type': 'string'
        },
    },
}

TEST_SCHEMA_2 = {
    '$id': 'test/test2',
    'version': 1,
    'properties': {
        'something_else': {
            'type': 'string'
        },
    },
}


def test_event_router_init():
    # Test that router initialization works.
    router = EventRouter(
        eventlogs=[
            EventLog(),
            EventLog()
    ])
    assert hasattr(router, 'eventlogs')
    assert isinstance(router.eventlogs[0], EventLog)    


def test_register_schema():
    router = EventRouter(
        eventlogs=[
            EventLog(),
            EventLog()
    ])
    router.register_schema(TEST_SCHEMA_1)
    key = (TEST_SCHEMA_1['$id'], TEST_SCHEMA_1['version'])
    assert key in router.eventlogs[0].schemas
    assert key in router.eventlogs[1].schemas


def test_routing():
    log_capture_1 = io.StringIO()
    log_capture_2 = io.StringIO()

    router = EventRouter(
        eventlogs=[
            EventLog(
                handlers=[logging.StreamHandler(log_capture_1)],
                allowed_schemas=['test/test1']
            ),
            EventLog(
                handlers=[logging.StreamHandler(log_capture_2)],
                allowed_schemas=['test/test2']
            )
    ])
    event = {
        'something': 'blah'
    }
    router.register_schema(TEST_SCHEMA_1)
    router.register_schema(TEST_SCHEMA_2)
    router.record_event(TEST_SCHEMA_1['$id'], 1, event)

    breakpoint()


    # key = (TEST_SCHEMA_1['$id'], TEST_SCHEMA_1['version'])
    # assert key in router.eventlogs[0].schemas
    # assert key in router.eventlogs[1].schemas