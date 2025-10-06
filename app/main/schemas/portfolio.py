from marshmallow import Schema, fields
from app.main.model.portfolio import Portfolio


class PortfolioSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    created_date = fields.DateTime(allow_none=True)
    updated_date = fields.DateTime(allow_none=True)
    property_count = fields.Int(allow_none=True)
    total_income = fields.Float(allow_none=True)
    # If you want to include owner details, you can nest another schema here
    # owner = fields.Nested('UserSchema', only=['id', 'username'], dump_only=True)
    # If you want to include properties, you can nest another schema here
    # properties = fields.List(fields.Nested('PropertySchema', dump_only=True))

    class Meta:
        model = Portfolio
        fields = ("id", "name", "owner_id", "created_date",
                  "updated_date", "property_count", "total_income")
