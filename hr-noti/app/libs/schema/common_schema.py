from flask_marshmallow import base_fields
from marshmallow import validate
from flask_restplus_patched import Parameters

SORT_DIRS = ['desc', 'asc']


account_validator = validate.Regexp(r'^[a-zA-Z0-9\_]{6,32}$')
pass_validator = validate.Regexp(r'^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9!@#$%^&*]{8,32}$')
positive_number = validate.Regexp(r'^[1-9][0-9]*$')


class PaginationParameter(Parameters):
    """
    Helper Parameters class to reuse pagination
    """
    limit = base_fields.Integer(
        description="limit a number of items (allowed range is 1-100), default is 20.",
        missing=20,
        validate=validate.Range(min=1, max=100)
    )
    offset = base_fields.Integer(
        description="a number of items to skip, default is 0.",
        missing=0,
        validate=validate.Range(min=0)
    )


class SortParam:
    sort_dir = base_fields.String(validate=validate.OneOf(SORT_DIRS))


# <editor-fold desc="Demo parameters">
class DemoListParams(Parameters):
    field1 = base_fields.String(required=True)


class DemoCreateParams(Parameters):
    field2 = base_fields.String()


class DemoUpdateParams(Parameters):
    id = base_fields.Integer()
    field2 = base_fields.String()


class DemoGetItemParams(Parameters):
    field3 = base_fields.String()
# </editor-fold>


class HealthCheckParams(Parameters):
    pass


class BlankParams(Parameters):
    pass
