import os

import pytest
from pytest_httpserver import HTTPServer

from infobip_cpaasx import ApiClient, Configuration, MmsApi, MmsAdvancedRequest, MmsAdvancedMessageSegmentText, \
    MmsAdvancedMessageSegmentLink, MmsSendResult, MmsAdvancedMessage, MmsAdvancedMessageSegment, MmsMessageResult, \
    MmsStatus, MmsDeliveryTimeWindow, MmsDeliveryTime, MmsDeliveryDay, MmsAdvancedMessageSegmentBinary, \
    MmsAdvancedMessageSegmentSmil, MmsAdvancedMessageSegmentUploadReference, MmsReportResponse, MmsReport, MmsPrice, \
    MmsError, MmsInboundReportResponse, MmsInboundReport, \
    MmsWebhookInboundReportResponse, MmsWebhookInboundReport, MmsWebhookInboundMessageSegment, MmsMessageContent, \
    MmsWebhookInboundMessageSegmentLink, MmsWebhookInboundMessageSegmentText, MmsUploadBinaryResult, MmsDestination

mms_advanced_endpoint = "/mms/1/advanced"
mms_reports_endpoint = "/mms/1/reports"
mms_inbound_endpoint = "/mms/1/inbox/reports"
mms_content_endpoint = "/mms/1/content"

api_key = "api_key_value"
user_agent = "infobip-api-client-python/0.0.2-cpaasx"
expected_headers = {
    "Authorization": "App {}".format(api_key),
    "User-Agent": user_agent
}
port = 8088


def test_send_link_mms_with_application_and_entity(httpserver: HTTPServer, mms_api_instance):
    bulk_id = "2034072219640523072"
    to = "41793026727"
    message_id = "2250be2d4219-3af1-78856-aabe-1362af1edfd2"
    given_from = "InfoSMS"
    application_id = "application_id"
    entity_id = "entity_id"

    text_segment_content_id = "text_content_id"
    text_segment_text = "text_segment_text"
    link_segment_content_id = "link_content_id"
    link_segment_content_type = "image/jpeg"
    link_segment_content_url = "https://api.infobip.com/ott/1/media/infobipLogo"

    request = {
        "messages": [
            {
                "destinations": [
                    {
                        "to": to
                    }
                ],
                "from": given_from,
                "messageSegments": [
                    {
                        "contentId": text_segment_content_id,
                        "text": text_segment_text
                    },
                    {
                        "contentId": link_segment_content_id,
                        "contentType": link_segment_content_type,
                        "contentUrl": link_segment_content_url
                    }
                ],
                "applicationId": application_id,
                "entityId": entity_id
            }
        ]
    }

    group_id = 1
    group_name = "PENDING"
    status_id = 26
    status_name = "MESSAGE_ACCEPTED"
    status_description = "Message sent to next instance"

    expected_response = {
        "bulkId": bulk_id,
        "messages": [{
            "to": to,
            "status": {
                "groupId": group_id,
                "groupName": group_name,
                "id": status_id,
                "name": status_name,
                "description": status_description
            },
            "messageId": message_id
        }],
    }

    setup_post_request_ok(
        httpserver=httpserver,
        endpoint=mms_advanced_endpoint,
        expected_request=request,
        expected_response=expected_response
    )

    mms_advanced_request = MmsAdvancedRequest(
        messages=[
            MmsAdvancedMessage(
                destinations=[
                    MmsDestination(
                        to=to,
                    ),
                ],
                var_from=given_from,
                content=MmsMessageContent(
                message_segments=[
                    MmsAdvancedMessageSegment(actual_instance=MmsAdvancedMessageSegmentText(
                        content_id=text_segment_content_id,
                        text=text_segment_text
                    )),
                    MmsAdvancedMessageSegment(actual_instance=MmsAdvancedMessageSegmentLink(
                        content_id=link_segment_content_id,
                        content_type=link_segment_content_type,
                        content_url=link_segment_content_url
                    ))
                ],
                ),
                application_id=application_id,
                entity_id=entity_id
            )
        ])

    actual_response: MmsSendResult = mms_api_instance.send_mms_message(mms_advanced_request=mms_advanced_request)

    expected_mms_send_result = MmsSendResult(
        bulk_id=bulk_id,
        messages=[
            MmsMessageResult(
                message_id=message_id,
                status=MmsStatus(
                    group_id=group_id,
                    group_name=group_name,
                    id=status_id,
                    name=status_name,
                    description=status_description,
                ),
                to=to
            )
        ]
    )

    assert actual_response == expected_mms_send_result


def test_send_fully_featured_mms(httpserver: HTTPServer, mms_api_instance):
    bulk_id = "2034072219640523072"
    to = "41793026727"
    message_id = "2250be2d4219-3af1-78856-aabe-1362af1edfd2"
    given_from = "InfoSMS"
    application_id = "application_id"
    entity_id = "entity_id"

    text_segment_content_id = "text_content_id"
    text_segment_text = "text_segment_text"
    link_segment_content_id = "link_content_id"
    link_segment_content_type = "image/jpeg"
    link_segment_content_url = "https://api.infobip.com/ott/1/media/infobipLogo"
    binary_segment_content_id = "binary_content_id"
    binary_segment_content_type = "image/jpeg"
    binary_segment_content_base64 = "base64_encoded_image"
    smil_segment_content_id = "smil_content_id"
    smil_segment_content_type = "image/png"
    smil_segment_content = "smil_content"
    uploaded_segment_content_id = "uploaded_content_id"
    uploaded_content_id = "previously_uploaded_content_id"

    callback_data = "my-callback-data"
    first_delivery_day = "MONDAY"
    second_delivery_day = "THURSDAY"
    delivery_from_hours = 11
    delivery_from_minutes = 10
    delivery_to_hours = 12
    delivery_to_minutes = 15
    intermediate_report = True
    notify_url = "https://example.com/mms-webhook"
    validity_period = 10
    title = "MMS Campaign"

    expected_request = {
        "messages": [
            {
                "callbackData": callback_data,
                "deliveryTimeWindow": {
                    "days": [first_delivery_day, second_delivery_day],
                    "from": {
                        "hour": delivery_from_hours,
                        "minute": delivery_from_minutes
                    },
                    "to": {
                        "hour": delivery_to_hours,
                        "minute": delivery_to_minutes
                    }
                },
                "destinations": [
                    {
                        "to": to,
                        "messageId": message_id
                    }
                ],
                "from": given_from,
                "intermediateReport": intermediate_report,
                "notifyUrl": notify_url,
                "messageSegments": [
                    {
                        "contentId": text_segment_content_id,
                        "text": text_segment_text
                    },
                    {
                        "contentId": link_segment_content_id,
                        "contentType": link_segment_content_type,
                        "contentUrl": link_segment_content_url
                    },
                    {
                        "contentId": binary_segment_content_id,
                        "contentType": binary_segment_content_type,
                        "contentBase64": binary_segment_content_base64
                    },
                    {
                        "contentId": smil_segment_content_id,
                        "contentType": smil_segment_content_type,
                        "smil": smil_segment_content
                    },
                    {
                        "contentId": uploaded_segment_content_id,
                        "uploadedContentId": uploaded_content_id
                    }
                ],
                "validityPeriod": validity_period,
                "title": title,
                "applicationId": application_id,
                "entityId": entity_id
            }
        ]
    }

    group_id = 1
    group_name = "PENDING"
    status_id = 26
    status_name = "MESSAGE_ACCEPTED"
    status_description = "Message sent to next instance"

    expected_response = {
        "bulkId": bulk_id,
        "messages": [{
            "to": to,
            "status": {
                "groupId": group_id,
                "groupName": group_name,
                "id": status_id,
                "name": status_name,
                "description": status_description
            },
            "messageId": message_id
        }],
    }

    setup_post_request_ok(
        httpserver=httpserver,
        endpoint=mms_advanced_endpoint,
        expected_request=expected_request,
        expected_response=expected_response
    )

    mms_advanced_request = MmsAdvancedRequest(
        messages=[
            MmsAdvancedMessage(
                callback_data=callback_data,
                delivery_time_window=MmsDeliveryTimeWindow(
                    days=[MmsDeliveryDay.MONDAY, MmsDeliveryDay.THURSDAY],
                    var_from=MmsDeliveryTime(
                        hour=delivery_from_hours,
                        minute=delivery_from_minutes
                    ),
                    to=MmsDeliveryTime(
                        hour=delivery_to_hours,
                        minute=delivery_to_minutes
                    )
                ),
                destinations=[
                    MmsDestination(
                        message_id=message_id,
                        to=to,
                    ),
                ],
                var_from=given_from,
                intermediate_report=intermediate_report,
                notify_url=notify_url,
                message_segments=[
                    MmsAdvancedMessageSegment(actual_instance=MmsAdvancedMessageSegmentText(
                        content_id=text_segment_content_id,
                        text=text_segment_text
                    )),
                    MmsAdvancedMessageSegment(actual_instance=MmsAdvancedMessageSegmentLink(
                        content_id=link_segment_content_id,
                        content_type=link_segment_content_type,
                        content_url=link_segment_content_url
                    )),
                    MmsAdvancedMessageSegment(actual_instance=MmsAdvancedMessageSegmentBinary(
                        content_id=binary_segment_content_id,
                        content_type=binary_segment_content_type,
                        content_base64=binary_segment_content_base64
                    )),
                    MmsAdvancedMessageSegment(actual_instance=MmsAdvancedMessageSegmentSmil(
                        content_id=smil_segment_content_id,
                        content_type=smil_segment_content_type,
                        smil=smil_segment_content
                    )),
                    MmsAdvancedMessageSegment(actual_instance=MmsAdvancedMessageSegmentUploadReference(
                        content_id=uploaded_segment_content_id,
                        uploaded_content_id=uploaded_content_id
                    ))
                ],
                validity_period=validity_period,
                title=title,
                application_id=application_id,
                entity_id=entity_id
            )
        ])

    actual_response: MmsSendResult = mms_api_instance.send_mms_message(mms_advanced_request=mms_advanced_request)

    expected_mms_send_result = MmsSendResult(
        bulk_id=bulk_id,
        messages=[
            MmsMessageResult(
                message_id=message_id,
                status=MmsStatus(
                    group_id=group_id,
                    group_name=group_name,
                    id=status_id,
                    name=status_name,
                    description=status_description,
                ),
                to=to
            )
        ]
    )

    assert actual_response == expected_mms_send_result


def test_get_outbound_mms_message_reports(httpserver: HTTPServer, mms_api_instance):
    bulk_id = "2034072219640523072"
    to = "41793026727"
    message_id = "2250be2d4219-3af1-78856-aabe-1362af1edfd2"
    given_from = "InfoSMS"
    application_id = "application_id"
    entity_id = "entity_id"
    sent_at = "2019-11-09T16:00:00.000+0000"
    done_at = "2019-11-09T16:01:00.000+0000"
    mms_count = 1
    mcc_mnc = "code"
    callback_data = "my-callback-data"
    price_per_message = 0.01
    currency = "EUR"

    group_id = 3
    group_name = "DELIVERED"
    status_id = 5
    status_name = "DELIVERED_TO_HANDSET"
    status_description = "Message delivered to handset"

    error_group_id = 0
    error_group_name = "Ok"
    error_id = 0
    error_name = "NO_ERROR"
    error_description = "No Error"

    delivery_report = {
        "results": [
            {
                "bulkId": bulk_id,
                "messageId": message_id,
                "to": to,
                "from": given_from,
                "sentAt": sent_at,
                "doneAt": done_at,
                "mmsCount": mms_count,
                "mccMnc": mcc_mnc,
                "callbackData": callback_data,
                "price": {
                    "pricePerMessage": price_per_message,
                    "currency": currency
                },
                "status": {
                    "groupId": group_id,
                    "groupName": group_name,
                    "id": status_id,
                    "name": status_name,
                    "description": status_description
                },
                "error": {
                    "groupId": error_group_id,
                    "groupName": error_group_name,
                    "id": error_id,
                    "name": error_name,
                    "description": error_description
                },
                "entityId": entity_id,
                "applicationId": application_id
            }
        ]
    }

    query_string = to_query_string_without_escaping({
        "bulkId": bulk_id,
        "messageId": message_id,
        "limit": 1
    })

    setup_get_request(
        httpserver=httpserver,
        endpoint=mms_reports_endpoint,
        expected_response=delivery_report,
        query_string=query_string
    )

    expected_delivery_report = MmsReportResponse(
        results=[
            MmsReport(
                bulk_id=bulk_id,
                message_id=message_id,
                to=to,
                var_from=given_from,
                sent_at=sent_at,
                done_at=done_at,
                mms_count=mms_count,
                mcc_mnc=mcc_mnc,
                callback_data=callback_data,
                price=MmsPrice(
                    price_per_message=price_per_message,
                    currency=currency
                ),
                status=MmsStatus(
                    group_id=group_id,
                    group_name=group_name,
                    id=status_id,
                    name=status_name,
                    description=status_description
                ),
                error=MmsError(
                    group_id=error_group_id,
                    group_name=error_group_name,
                    id=error_id,
                    name=error_name,
                    description=error_description
                ),
                entity_id=entity_id,
                application_id=application_id
            )
        ]
    )

    actual_response = mms_api_instance.get_outbound_mms_message_delivery_reports(
        bulk_id=bulk_id,
        message_id=message_id,
        limit=1
    )

    assert actual_response == expected_delivery_report


def test_mms_reports_webhook_model(httpserver: HTTPServer, mms_api_instance):
    delivery_report = """
    {
        "results": [
            {
                "bulkId": "2034072219640523072",
                "messageId": "2250be2d4219-3af1-78856-aabe-1362af1edfd2",
                "to": "41793026727",
                "from": "InfoSMS",
                "sentAt": "2019-11-09T16:00:00.000+0000",
                "doneAt": "2019-11-09T16:01:00.000+0000",
                "mmsCount": 1,
                "mccMnc": "code",
                "callbackData": "my-callback-data",
                "price": {
                    "pricePerMessage": 0.01,
                    "currency": "EUR"
                },
                "status": {
                    "groupId": 3,
                    "groupName": "DELIVERED",
                    "id": 5,
                    "name": "DELIVERED_TO_HANDSET",
                    "description": "Message delivered to handset"
                },
                "error": {
                    "groupId": 0,
                    "groupName": "Ok",
                    "id": 0,
                    "name": "NO_ERROR",
                    "description": "No Error"
                },
                "entityId": "entity_id",
                "applicationId": "application_id"
            }
        ]
    }
    """

    expected_deserialized_report = MmsReportResponse(
        results=[
            MmsReport(
                bulk_id="2034072219640523072",
                message_id="2250be2d4219-3af1-78856-aabe-1362af1edfd2",
                to="41793026727",
                var_from="InfoSMS",
                sent_at="2019-11-09T16:00:00.000+0000",
                done_at="2019-11-09T16:01:00.000+0000",
                mms_count=1,
                mcc_mnc="code",
                callback_data="my-callback-data",
                price=MmsPrice(
                    price_per_message=0.01,
                    currency="EUR"
                ),
                status=MmsStatus(
                    group_id=3,
                    group_name="DELIVERED",
                    id=5,
                    name="DELIVERED_TO_HANDSET",
                    description="Message delivered to handset"
                ),
                error=MmsError(
                    group_id=0,
                    group_name="Ok",
                    id=0,
                    name="NO_ERROR",
                    description="No Error"
                ),
                entity_id="entity_id",
                application_id="application_id"
            )
        ]
    )

    actual_deserialized_report = MmsReportResponse.from_json(delivery_report)

    assert actual_deserialized_report == expected_deserialized_report


def test_get_inbound_mms_messages(httpserver: HTTPServer, mms_api_instance):
    to = "41793026727"
    message_id = "2250be2d4219-3af1-78856-aabe-1362af1edfd2"
    given_from = "InfoSMS"
    message = "Hello World!"
    received_at = "2019-11-09T16:00:00.000+0000"
    mms_count = 1
    mcc_mnc = "code"
    callback_data = "my-callback-data"
    price_per_message = 0.01
    currency = "EUR"

    inbound_report = {
        "results": [
            {
                "messageId": message_id,
                "to": to,
                "from": given_from,
                "message": message,
                "receivedAt": received_at,
                "mmsCount": mms_count,
                "callbackData": callback_data,
                "price": {
                    "pricePerMessage": price_per_message,
                    "currency": currency
                }
            }
        ]
    }

    query_string = to_query_string_without_escaping({
        "limit": 1
    })

    setup_get_request(
        httpserver=httpserver,
        endpoint=mms_inbound_endpoint,
        expected_response=inbound_report,
        query_string=query_string
    )

    expected_inbound_report = MmsInboundReportResponse(
        results=[
            MmsInboundReport(
                message_id=message_id,
                to=to,
                var_from=given_from,
                message=message,
                received_at=received_at,
                mms_count=mms_count,
                mcc_mnc=mcc_mnc,
                callback_data=callback_data,
                price=MmsPrice(
                    price_per_message=price_per_message,
                    currency=currency
                )
            )
        ]
    )

    actual_response = mms_api_instance.get_inbound_mms_messages(limit=1)

    assert actual_response == expected_inbound_report


def test_mms_inbound_reports_webhook_model(httpserver: HTTPServer, mms_api_instance):
    inbound_report = """
    {
      "results": [
        {
          "from": "385916242493",
          "to": "385921004026",
          "receivedAt": "2020-10-06T09:28:39.220+0000",
          "messageId": "817790313235066447-3af1-78856-aabe-1362af1edfd2",
          "pairedMessageId": "100200",
          "callbackData": "my-callback-data",
          "userAgent": "custom-user-agent",
          "message": [
            {
              "contentType": "image/jpeg",
              "url": "https://example.com/123456"
            },
            {
              "contentType": "text/plain",
              "value": "This is message text"
            }
          ],
          "price": {
            "pricePerMessage": 0.01,
            "currency": "EUR"
          },
          "applicationId": "given-application-id",
          "entityId": "given-entity-id"
        }
      ],
      "messageCount": 1,
      "pendingMessageCount": 0
    }
    """

    expected_deserialized_report = MmsWebhookInboundReportResponse(
        results=[
            MmsWebhookInboundReport(
                message_id="817790313235066447-3af1-78856-aabe-1362af1edfd2",
                to="385921004026",
                var_from="385916242493",
                received_at="2020-10-06T09:28:39.220+0000",
                paired_message_id="100200",
                callback_data="my-callback-data",
                user_agent="custom-user-agent",
                message=[
                    MmsWebhookInboundMessageSegment(actual_instance=MmsWebhookInboundMessageSegmentLink(
                        content_type="image/jpeg",
                        url="https://example.com/123456"
                    )),
                    MmsWebhookInboundMessageSegment(actual_instance=MmsWebhookInboundMessageSegmentText(
                        content_type="text/plain",
                        value="This is message text"
                    ))
                ],
                price=MmsPrice(
                    price_per_message=0.01,
                    currency="EUR"
                ),
                application_id="given-application-id",
                entity_id="given-entity-id"
            )
        ],
        message_count=1,
        pending_message_count=0
    )

    actual_deserialized_report = MmsWebhookInboundReportResponse.from_json(inbound_report)

    assert actual_deserialized_report == expected_deserialized_report


def test_upload_binary(httpserver: HTTPServer, mms_api_instance):
    uploaded_content_id = "ABC100"
    media_type = "image/png"
    content_id = "test-icon-id"
    validity_period = 10

    all_expected_headers = {
        "Content-Type": "application/octet-stream",
        "Accept": "application/json",
        "X-Media-Type": media_type,
        "X-Content-Id": content_id,
        "X-Validity-Period-Minutes": validity_period
    }.update(expected_headers)

    with open(locate_resource("icon.png"), mode='rb') as file:
        icon_file_content = file.read()

    httpserver.expect_request(
        uri=mms_content_endpoint,
        method="POST",
        headers=all_expected_headers,
        data=icon_file_content
    ).respond_with_json(
        status=200,
        response_json={"uploadedContentId": uploaded_content_id}
    )

    expected_upload_response = MmsUploadBinaryResult(uploaded_content_id=uploaded_content_id)

    actual_response = mms_api_instance.upload_binary(
        x_content_id=content_id,
        x_media_type=media_type,
        x_validity_period_minutes=validity_period,
        body=icon_file_content
    )

    assert actual_response == expected_upload_response


def setup_post_request_ok(
        httpserver: HTTPServer,
        endpoint: str,
        expected_request: dict,
        expected_response: dict
):
    httpserver.expect_request(
        uri=endpoint,
        method="POST",
        headers=expected_headers,
        json=expected_request
    ).respond_with_json(status=200, response_json=expected_response)


def to_query_string_without_escaping(query_params: dict):
    if not query_params:
        return ""
    return "&".join(["{}={}".format(paramName, paramValue) for (paramName, paramValue) in query_params.items()])


def setup_get_request(httpserver: HTTPServer, endpoint: str, expected_response: dict, query_string: str):
    httpserver.expect_request(
        uri=endpoint,
        method="GET",
        headers=expected_headers,
        query_string=query_string
    ).respond_with_json(status=200, response_json=expected_response)


def locate_resource(resource_name: str) -> str:
    return os.path.join(os.path.dirname(__file__), 'resources', resource_name)


@pytest.fixture
def mms_api_instance():
    return MmsApi(ApiClient(Configuration(
        host="http://localhost:{}".format(port),
        api_key=api_key,
        api_key_prefix="App"
    )))


@pytest.fixture(scope="session")
def httpserver_listen_address():
    return "localhost", port
