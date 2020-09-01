from flask_restx import fields


class ObjectCount(fields.Raw):
    def format(self, value):
        return len(value)
