from marshmallow import Schema, fields
from app.main.model.portfolio import Portfolio

class PortfolioSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    # If you want to include owner details, you can nest another schema here
    # owner = fields.Nested('UserSchema', only=['id', 'username'], dump_only=True)
    # If you want to include properties, you can nest another schema here
    # properties = fields.List(fields.Nested('PropertySchema', dump_only=True))

    class Meta:
        model = Portfolio
        fields = ("id", "name", "owner_id")