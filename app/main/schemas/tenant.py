from marshmallow import Schema, fields, validate, validates, ValidationError

class TenantSchema(Schema):
    title = fields.Str(
        required=False,
        validate=validate.OneOf([
            "MR", "MRS", "MISS", "MS", "LORD", "SIR", "DR", "LADY", "DAME", "PROFESSOR", "MX"
        ])
    )
    phone_number = fields.Str(required=False, validate=validate.Length(min=7, max=20))
    email_address = fields.Email(required=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    date_of_birth = fields.Date(required=True)
    job_title = fields.Str(required=True)
    tenancy_start_date = fields.Date(required=True)
    tenancy_end_date = fields.Date(required=False, allow_none=True)

    @validates("first_name")
    def validate_first_name(self, value):
        if not value.strip():
            raise ValidationError("First name cannot be empty or whitespace.")

    @validates("last_name")
    def validate_last_name(self, value):
        if not value.strip():
            raise ValidationError("Last name cannot be empty or whitespace.")