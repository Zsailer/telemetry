import logging


class SchemaFilter(logging.Filter):
    
    def __init__(self, schemas, include_pii=False, name=''):
        self.schemas = schemas
        self.include_pii = include_pii
        super(EventFilter, self).__init__(name=name)

    def filter(self, record):
        if record.msg['__schema__'] in self.schemas:
            return True
        return False