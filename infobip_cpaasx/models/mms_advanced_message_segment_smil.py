from __future__ import annotations
import pprint
import json
from typing import Optional
from pydantic import BaseModel, Field, StrictStr


class MmsAdvancedMessageSegmentSmil(BaseModel):
    """
    Represents a SMIL segment in an MMS message.
    """

    type: StrictStr = Field(
        default="SMIL",
        description="The type of the message segment. Must be 'SMIL' for SMIL segments."
    )
    content_id: Optional[StrictStr] = Field(
        None,
        alias="contentId",
        description="Unique identifier within single message. `[a-zA-Z]` up to 20 characters."
    )
    content_type: Optional[StrictStr] = Field(
        None,
        alias="contentType",
        description="Content type for SMIL, typically `application/smil`."
    )
    smil: Optional[StrictStr] = Field(
        None,
        description="Message segment as SMIL format."
    )

    __properties = ["type", "contentId", "contentType", "smil"]

    class Config:
        populate_by_name = True
        validate_assignment = True

    def to_str(self) -> str:
        return pprint.pformat(self.to_dict())

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_dict(self):
        return self.dict(by_alias=True, exclude_none=True)

    @classmethod
    def from_json(cls, json_str: str) -> MmsAdvancedMessageSegmentSmil:
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def from_dict(cls, obj: dict) -> MmsAdvancedMessageSegmentSmil:
        if obj is None:
            return None

        if type(obj) is not dict:
            return cls.parse_obj(obj)

        return cls.parse_obj({
            "type": obj.get("type", "SMIL"),
            "content_id": obj.get("contentId"),
            "content_type": obj.get("contentType"),
            "smil": obj.get("smil")
        })
