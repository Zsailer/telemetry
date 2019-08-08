from traitlets import List
from .eventlog import EventLog
from .traits import Configurable, InstanceContainer


class EventLogs(InstanceContainer):
    """A trait that takes a list of logging handlers and converts
    it to a callable that returns that list (thus, making this
    trait pickleable).
    """
    info_text = "a list of eventloggers handlers"
    _class = EventLog


class EventRouter(Configurable):

    eventlogs = EventLogs(
        [],
        config=True,
        allow_none=True,
        help="""A list of EventLogs instances to send events to.

        When set to None (the default), events are discarded.
        """
    )

    def register_schema_file(self, filename):
        """Register schema with each eventlog."""
        for eventlog in self.eventlogs:
            eventlog.register_schema_file(filename)

    def register_schema(self, schema):
        """Register schema with each eventlog."""
        for eventlog in self.eventlogs:
            eventlog.register_schema(schema)

    def record_event(self, schema_name, version, event):
        """Route events to each eventlog and only emit event if 
        the schema is registered with the given eventlog.
        """
        for eventlog in self.eventlogs:
            eventlog.record_event(schema_name, version, event)