import json, logging
from common.ops import wait_redis, wait_db, db
logging.basicConfig(level=logging.INFO); r=wait_redis(); wait_db()
logging.info("Event ingestor ready")
while True:
    item=r.blpop("opspulse:events",timeout=5)
    if not item: continue
    try:
        e=json.loads(item[1])
        with db() as c:
            c.execute("INSERT INTO incidents (service_name,environment_name,severity,metric,metric_value,message,status) VALUES (%s,%s,%s,%s,%s,%s,'INGESTED')",
              (e["service"],e["environment"],e["severity"].lower(),e["metric"],e["value"],e["message"]))
            e["id"]=c.lastrowid
        r.rpush("opspulse:rules",json.dumps(e))
        logging.info("Stored incident %s",e["id"])
    except Exception:
        logging.exception("Ingestion failed; moving payload to failed queue"); r.rpush("opspulse:failed-events",item[1])
