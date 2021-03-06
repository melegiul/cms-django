"""
Retrieve push notifications that have been sent, optionally filtering by channel.
"""
from django.http import JsonResponse

from cms.models import PushNotificationTranslation


def sent_push_notifications(request, region_slug, language_code):
    """
    Function to iterate through all sent push notifications related to a region and adds them to a JSON.

    :param request: Django request
    :type request: ~django.http.HttpRequest
    :param region_slug: slug of a region
    :type region_slug: str
    :param language_code: language code
    :type language_code: str

    :return: JSON object according to APIv3 push notifications definition
    :rtype: ~django.http.JsonResponse
    """

    channel = request.GET.get("channel", "all")
    query_result = (
        PushNotificationTranslation.objects.filter(
            push_notification__region__slug=region_slug
        )
        .filter(push_notification__sent_date__isnull=False)
        .filter(language__code=language_code)
    )
    if channel != "all":
        query_result = query_result.filter(push_notification__channel=channel)
    result = list(map(transform_notification, query_result))
    return JsonResponse(result, safe=False)


def transform_notification(pn):
    """
    Function to create a JSON from a single push_notification Object.

    :param offer: one offer (formerly extra)
    :type offer: ~cms.models.push_notifications.push_notification.PushNotification

    :return: return data necessary for API
    :rtype: dict
    """
    return {
        "title": pn.title,
        "text": pn.text,
        "channel": pn.push_notification.channel,
        "sent_date": pn.push_notification.sent_date,
    }
