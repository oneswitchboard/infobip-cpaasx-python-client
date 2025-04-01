from __future__ import annotations
import pprint
import json
from typing import Optional
from pydantic import BaseModel, Field, StrictStr


class MmsAdvancedMessageSegmentBinary(BaseModel):
    """
    Represents a binary media segment (base64) in an MMS message.
    """

    type: StrictStr = Field(
        default="BINARY",
        description="The type of the message segment. Must be 'BINARY' for base64-encoded content."
    )
    content_id: Optional[StrictStr] = Field(
        None,
        alias="contentId",
        description="Unique identifier within single message. `[a-zA-Z]` up to 20 characters."
    )
    content_type: Optional[StrictStr] = Field(
        None,
        alias="contentType",
        description="Content type for media, for example `image/png`."
    )
    content_base64: Optional[StrictStr] = Field(
        None,
        alias="contentBase64",
        description="Content in Base64 format."
    )

    __properties = ["type", "contentId", "contentType", "contentBase64"]

    class Config:
        populate_by_name = True
        validate_assignment = True

    def to_str(self) -> str:
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_dict(self):
        return self.dict(by_alias=True, exclude_none=True)

    @classmethod
    def from_json(cls, json_str: str) -> MmsAdvancedMessageSegmentBinary:
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def from_dict(cls, obj: dict) -> MmsAdvancedMessageSegmentBinary:
        if obj is None:
            return None

        if type(obj) is not dict:
            return cls.parse_obj(obj)

        return cls.parse_obj({
            "type": obj.get("type", "BINARY"),
            "content_id": obj.get("contentId"),
            "content_type": obj.get("contentType"),
            "content_base64": obj.get("contentBase64")
        })
