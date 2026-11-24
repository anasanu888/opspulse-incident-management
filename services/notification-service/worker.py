import json, logging
from common.ops import wait_redis
logging.basicConfig(level=logging.INFO); r=wait_redis()
logging.info("Notification service ready")
while True:
    item=r.blpop("opspulse:notifications",timeout=5)
    if item:
        try:
            n=json.loads(item[1]); logging.info("NOTIFICATION incident=%s service=%s %s",n["incident_id"],n["service"],n["message"])
        except Exception: logging.exception("Bad notification payload")
