from marshmallow import Schema, fields, validates, ValidationError


class OwnerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    sales_opportunity = fields.Bool(dump_only=True)


class CarSchema(Schema):
    id = fields.Int(dump_only=True)
    color = fields.Str(required=True)
    model = fields.Str(required=True)
    owner_id = fields.Int(required=True)

    @validates('color')
    def validate_color(self, value):
        if value not in ['yellow', 'blue', 'gray']:
            raise ValidationError("Color must be 'yellow', 'blue', or 'gray'.")

    @validates('model')
    def validate_model(self, value):
        if value not in ['hatch', 'sedan', 'convertible']:
            raise ValidationError(
                "Model must be 'hatch', 'sedan', or 'convertible'.")
