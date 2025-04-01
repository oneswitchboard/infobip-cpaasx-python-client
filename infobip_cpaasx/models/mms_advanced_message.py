from __future__ import annotations
import pprint
import json
from typing import List, Optional
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr, constr

from infobip_cpaasx.models.mms_message_content import MmsMessageContent
from infobip_cpaasx.models.mms_delivery_time_window import MmsDeliveryTimeWindow
from infobip_cpaasx.models.mms_destination import MmsDestination


class MmsAdvancedMessage(BaseModel):
    callback_data: Optional[constr(strict=True, max_length=4000, min_length=0)] = Field(
        None, alias="callbackData"
    )
    delivery_time_window: Optional[MmsDeliveryTimeWindow] = Field(
        None, alias="deliveryTimeWindow"
    )
    destinations: List[MmsDestination] = Field(
        ..., description="An array of destination objects for where messages are being sent."
    )
    sender: Optional[StrictStr] = Field(
        None,
        alias="sender",
        description="The sender ID (alphanumeric or numeric, e.g., 'CompanyName' or short code)."
    )
    intermediate_report: Optional[StrictBool] = Field(
        None, alias="intermediateReport"
    )
    notify_url: Optional[StrictStr] = Field(
        None, alias="notifyUrl"
    )
    content: MmsMessageContent = Field(
        None, description="The content of the MMS message. Max size: 600 KB."
    )
    validity_period: Optional[StrictInt] = Field(
        None, alias="validityPeriod"
    )
    entity_id: Optional[constr(strict=True, max_length=50, min_length=0)] = Field(
        None, alias="entityId"
    )
    application_id: Optional[constr(strict=True, max_length=50, min_length=0)] = Field(
        None, alias="applicationId"
    )

    class Config:
        populate_by_name = True
        validate_assignment = True

    def to_str(self) -> str:
        return pprint.pformat(self.to_dict())

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_dict(self):
        _dict = self.dict(by_alias=True, exclude_none=True)

        if self.delivery_time_window:
            _dict["deliveryTimeWindow"] = self.delivery_time_window.to_dict()

        if self.destinations:
            _dict["destinations"] = [d.to_dict() for d in self.destinations]

        if self.content:
            _dict["content"] = self.content.to_dict()

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> MmsAdvancedMessage:
        if obj is None:
            return None

        return cls(
            callback_data=obj.get("callbackData"),
            delivery_time_window=MmsDeliveryTimeWindow.from_dict(obj.get("deliveryTimeWindow"))
                if obj.get("deliveryTimeWindow") is not None else None,
            destinations=[
                MmsDestination.from_dict(d) for d in obj.get("destinations", [])
            ],
            sender=obj.get("sender"),
            intermediate_report=obj.get("intermediateReport"),
            notify_url=obj.get("notifyUrl"),
            content=MmsMessageContent.from_dict(obj.get("content"))
                if obj.get("content") is not None else None,
            validity_period=obj.get("validityPeriod"),
            entity_id=obj.get("entityId"),
            application_id=obj.get("applicationId"),
        )
