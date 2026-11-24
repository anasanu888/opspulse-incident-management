
import json, logging
from common.ops import wait_redis, wait_db, db

logging.basicConfig(level=logging.INFO)
r = wait_redis()
wait_db()

logging.info("Rule engine ready")

while True:
    item = r.blpop("opspulse:rules", timeout=5)

    if not item:
        continue

    try:
        e = json.loads(item[1])
        sev = e["severity"].lower()
        metric = e["metric"].lower()
        val = float(e["value"])

        trigger = sev in ("critical", "high") or (
            metric in ("cpu", "memory") and val >= 85
        )

        status = "REMEDIATION_QUEUED" if trigger else "MONITORED"

        if trigger:
            r.rpush(
                "opspulse:remediations",
                json.dumps({
                    "incident_id": e["id"],
                    "service": e["service"],
                    "action": "SIMULATED_RESTART",
                    "reason": f"{sev} {metric} alert"
                })
            )

        with db() as conn:
            with conn.cursor() as c:
                c.execute(
                    "UPDATE incidents SET status=%s WHERE id=%s",
                    (status, e["id"])
                )

        logging.info("Incident %s -> %s", e["id"], status)

    except Exception:
        logging.exception("Rule evaluation failed")
