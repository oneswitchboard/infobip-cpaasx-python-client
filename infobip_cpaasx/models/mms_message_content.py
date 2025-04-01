from typing import List, Optional
from pydantic import BaseModel, Field
from infobip_cpaasx.models.mms_advanced_message_segment import MmsAdvancedMessageSegment

class MmsMessageContent(BaseModel):
    title: Optional[str] = Field(None, description="Optional title of the MMS message")
    message_segments: List[MmsAdvancedMessageSegment] = Field(
        ..., alias="messageSegments", description="List of content segments in the MMS message"
    )

    class Config:
        populate_by_name = True
        validate_assignment = True

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)

    def to_json(self) -> str:
        return self.model_dump_json(by_alias=True, exclude_none=True)

    @classmethod
    def from_dict(cls, obj: dict) -> "MmsMessageContent":
        return cls.model_validate(obj)

    @classmethod
    def from_json(cls, json_str: str) -> "MmsMessageContent":
        import json
        return cls.from_dict(json.loads(json_str))

    def to_str(self) -> str:
        import pprint
        return pprint.pformat(self.to_dict())
