import logging
import os
from datetime import datetime, timezone
from enum import Enum
from kubernetes import client, config, watch
import slack

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(level=logging.getLevelName(LOG_LEVEL),
                    format='%(asctime)s.%(msecs)03d %(levelname)s:\t%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging

start_time = datetime.now(timezone.utc)

TOKEN = os.getenv('SLACK_TOKEN')
CHANNEL = os.getenv('SLACK_CHANNEL')
NAMESPACE = os.getenv('NAMESPACE', 'default')

if TOKEN is None or CHANNEL is None:
    log.critical("Please provide SLACK_TOKEN and SLACK_CHANNEL env vars")
    quit()

if os.getenv("TEST") is not None:
    config.load_kube_config()
else:
    config.load_incluster_config()

v1 = client.CoreV1Api()
client = slack.WebClient(token=TOKEN)


def is_current_event(e): return e.last_timestamp >= start_time


class Level(Enum):
    NONE = '#808080',
    INFO = '#339900',
    WARN = '#ffcc00',
    ERROR = '#cc3300'

    def __init__(self, color):
        self.color = color


def send(title, text='', level=Level.NONE):
    res = client.chat_postMessage(
        channel=CHANNEL,
        username='k8s',
        attachments=[{'title': title, 'text': text, 'color': level.color}],
        as_user=True)
    if res['ok']:
        log.info(f"Sent to Slack: [{level.name}] {title}")
    else:
        log.error(f"Error sending message to Slack: {res}")


stream = watch.Watch().stream(v1.list_namespaced_event, NAMESPACE)

for event in stream:
    e = event['object']
    obj = e.involved_object

    log.info(f"EVENT [{e.last_timestamp}] {obj.kind}/{obj.name} '{e.reason}': {e.message}")

    if is_current_event(e):
        if obj.kind == 'Pod':
            if e.reason == 'Started':
                send(f"{obj.name} started", level=Level.INFO)
            if e.reason == 'Unhealthy':
                send(f"{obj.name} - {e.reason}", text=e.message, level=Level.WARN)
