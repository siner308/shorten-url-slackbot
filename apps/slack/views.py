from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from slack_sdk.web.client import WebClient
from apps.shortener.models import Shortener
from env import SLACK_BOT_TOKEN, SERVER_URL


class SlackViewSet(ViewSet):
    def __init__(self, *args, **kwargs):
        self.client = WebClient(token=SLACK_BOT_TOKEN)
        super().__init__(*args, **kwargs)

    @action(detail=False, methods=["POST"])
    def event(self, request: Request):
        data = request.data
        if data.get("challenge"):
            return Response(dict(challenge=data["challenge"]))

        event = data["event"]
        event_type = event["type"]
        event_subtype = event.get("subtype")

        def handle(sub_element):
            if sub_element["type"] != "link":
                return
            url = sub_element["url"]
            if len(url) > 20:
                shortener, is_created = Shortener.objects.get_or_create(url=url)
                compressed_origin_url = f"{url[:10:]}...{url[-5::]}"
                text = f"""`{compressed_origin_url}` 을 줄여왔어요!\n{SERVER_URL}/{shortener.id}"""
                self.client.chat_postMessage(
                    text=text,
                    channel=data["event"]["channel"],
                    thread_ts=data["event"]["ts"],
                )
            else:
                self.client.chat_postMessage(
                    text=f"{url} 은 짧아서 줄이지 않았습니다.",
                    channel=data["event"]["channel"],
                    thread_ts=data["event"]["ts"],
                )

        if event_type != "message" or event_subtype is not None or event.get("bot_id"):
            return Response(status=200)

        blocks = event["blocks"]
        for block in blocks:
            for element in block["elements"]:
                for sub_element in element["elements"]:
                    handle(sub_element)
        return Response(status=200)
