from flask_restx import fields


class ObjectCount(fields.Raw):
    def format(self, value):
        return len(value)


class SumOfProperties(fields.Raw):
    def format(self, value):
        return sum([x.monthly_rental_price for x in value])