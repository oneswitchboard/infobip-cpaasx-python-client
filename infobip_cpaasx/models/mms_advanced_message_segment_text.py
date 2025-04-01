from __future__ import annotations
import pprint
import json
from typing import Optional
from pydantic import BaseModel, Field, StrictStr


class MmsAdvancedMessageSegmentText(BaseModel):
    """
    Represents a text segment in an MMS message.
    """

    type: StrictStr = Field(
        default="TEXT",
        description="The type of the message segment. Must be 'TEXT' for plain text segments."
    )
    content_id: Optional[StrictStr] = Field(
        None,
        alias="contentId",
        description="Unique identifier within a single message. `[a-zA-Z]` up to 20 characters."
    )
    text: Optional[StrictStr] = Field(
        None,
        description="Message text."
    )

    __properties = ["type", "contentId", "text"]

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
    def from_json(cls, json_str: str) -> MmsAdvancedMessageSegmentText:
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def from_dict(cls, obj: dict) -> MmsAdvancedMessageSegmentText:
        if obj is None:
            return None

        if type(obj) is not dict:
            return cls.parse_obj(obj)

        return cls.parse_obj({
            "type": obj.get("type", "TEXT"),
            "content_id": obj.get("contentId"),
            "text": obj.get("text")
        })
