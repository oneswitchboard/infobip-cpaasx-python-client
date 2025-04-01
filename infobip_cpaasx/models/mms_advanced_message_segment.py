from typing import Union
from pydantic import RootModel
import json
import pprint

from infobip_cpaasx.models.mms_advanced_message_segment_binary import MmsAdvancedMessageSegmentBinary
from infobip_cpaasx.models.mms_advanced_message_segment_link import MmsAdvancedMessageSegmentLink
from infobip_cpaasx.models.mms_advanced_message_segment_smil import MmsAdvancedMessageSegmentSmil
from infobip_cpaasx.models.mms_advanced_message_segment_text import MmsAdvancedMessageSegmentText
from infobip_cpaasx.models.mms_advanced_message_segment_upload_reference import MmsAdvancedMessageSegmentUploadReference


SegmentUnion = Union[
    MmsAdvancedMessageSegmentText,
    MmsAdvancedMessageSegmentLink,
    MmsAdvancedMessageSegmentBinary,
    MmsAdvancedMessageSegmentSmil,
    MmsAdvancedMessageSegmentUploadReference,
]

class MmsAdvancedMessageSegment(RootModel[SegmentUnion]):
    @classmethod
    def from_json(cls, json_str: str) -> "MmsAdvancedMessageSegment":
        try:
            data = json.loads(json_str)
            return cls.model_validate(data)
        except Exception as e:
            raise ValueError(f"Could not parse MmsAdvancedMessageSegment from JSON: {e}")

    @classmethod
    def from_dict(cls, obj: dict) -> "MmsAdvancedMessageSegment":
        try:
            return cls.model_validate(obj)
        except Exception as e:
            raise ValueError(f"Could not parse MmsAdvancedMessageSegment from dict: {e}")

    def to_dict(self) -> dict:
        return self.root.to_dict()

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_str(self) -> str:
        return pprint.pformat(self.to_dict())

    @property
    def actual_instance(self):
        return self.root
