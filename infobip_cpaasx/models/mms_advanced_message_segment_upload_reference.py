from __future__ import annotations
import pprint
import json
from typing import Optional
from pydantic import BaseModel, Field, StrictStr


class MmsAdvancedMessageSegmentUploadReference(BaseModel):
    """
    Represents a segment that references previously uploaded content by ID.
    """

    type: StrictStr = Field(
        default="UPLOAD",
        description="The type of the message segment. Must be 'UPLOAD' for references to uploaded content."
    )
    content_id: Optional[StrictStr] = Field(
        None,
        alias="contentId",
        description="Unique identifier within single message. `[a-zA-Z]` up to 20 characters."
    )
    uploaded_content_id: Optional[StrictStr] = Field(
        None,
        alias="uploadedContentId",
        description="ID of previously uploaded binary content."
    )

    __properties = ["type", "contentId", "uploadedContentId"]

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
    def from_json(cls, json_str: str) -> MmsAdvancedMessageSegmentUploadReference:
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def from_dict(cls, obj: dict) -> MmsAdvancedMessageSegmentUploadReference:
        if obj is None:
            return None

        if type(obj) is not dict:
            return cls.parse_obj(obj)

        return cls.parse_obj({
            "type": obj.get("type", "UPLOAD"),
            "content_id": obj.get("contentId"),
            "uploaded_content_id": obj.get("uploadedContentId")
        })
