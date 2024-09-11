from mongoengine import (
    Document,
    StringField,
    IntField,
    SequenceField,
    DateTimeField,
)
import shortuuid


SHORT_CODE_LEN = 6  # euqals to 22 million URLs


class UUIDField(StringField):
    def __init__(self, *args, **kwargs):
        kwargs["default"] = self.generate_uuid
        super(UUIDField, self).__init__(*args, **kwargs)

    def generate_uuid(self):
        return shortuuid.ShortUUID().random(length=SHORT_CODE_LEN)

    def to_python(self, value):
        return str(value)

    def to_mongo(self, value):
        return str(value)


def _get_uuid():
    return shortuuid.ShortUUID().random(length=SHORT_CODE_LEN)


class Url(Document):
    id = SequenceField(primary_key=True)
    url = StringField(required=True)
    short_code = UUIDField(
        required=True, max_length=SHORT_CODE_LEN, min_length=SHORT_CODE_LEN, unique=True
    )
    created_at = DateTimeField()  # TODO: required eklemen gerekiyor
    updated_at = DateTimeField()
    access_count = IntField(required=True, default=0)
