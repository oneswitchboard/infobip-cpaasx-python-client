from __future__ import annotations
import pprint
import json
from typing import Optional
from pydantic import BaseModel, Field, StrictStr


class MmsAdvancedMessageSegmentLink(BaseModel):
    """
    Represents a media segment in an MMS message.
    """

    type: StrictStr = Field(
        default="LINK",
        description="The type of the message segment. Must be 'LINK' for media segments."
    )
    content_id: Optional[StrictStr] = Field(
        None,
        alias="contentId",
        description="Unique identifier within single message. `[a-zA-Z]` up to 20 characters."
    )
    content_type: Optional[StrictStr] = Field(
        None,
        alias="contentType",
        description="Content type for media, e.g., `image/jpeg`."
    )
    content_url: StrictStr = Field(
        ..., alias="contentUrl", description="URL of externally hosted content."
    )

    __properties = ["type", "contentId", "contentType", "contentUrl"]

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
    def from_json(cls, json_str: str) -> MmsAdvancedMessageSegmentLink:
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def from_dict(cls, obj: dict) -> MmsAdvancedMessageSegmentLink:
        if obj is None:
            return None

        if type(obj) is not dict:
            return cls.parse_obj(obj)

        return cls.parse_obj({
            "type": obj.get("type", "LINK"),
            "content_id": obj.get("contentId"),
            "content_type": obj.get("contentType"),
            "content_url": obj.get("contentUrl"),
        })
