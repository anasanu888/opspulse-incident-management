
import json, logging, time
from common.ops import wait_redis, wait_db, db

logging.basicConfig(level=logging.INFO)
r = wait_redis()
wait_db()

logging.info("Remediation worker ready (simulation mode)")

while True:
    item = r.blpop("opspulse:remediations", timeout=5)

    if not item:
        continue

    try:
        a = json.loads(item[1])
        time.sleep(2)

        detail = f"Simulated restart workflow completed for {a['service']}; no infrastructure changed."

        with db() as conn:
            with conn.cursor() as c:
                c.execute(
                    """INSERT INTO remediation_actions
                    (incident_id,action_name,status,details)
                    VALUES (%s,%s,%s,%s)""",
                    (
                        a["incident_id"],
                        a["action"],
                        "SIMULATED_SUCCESS",
                        detail
                    )
                )

                c.execute(
                    "UPDATE incidents SET status='REMEDIATED_SIMULATED' WHERE id=%s",
                    (a["incident_id"],)
                )

        r.rpush(
            "opspulse:notifications",
            json.dumps({
                "incident_id": a["incident_id"],
                "service": a["service"],
                "message": detail
            })
        )

        logging.info(
            "Simulated action completed for incident %s",
            a["incident_id"]
        )

    except Exception:
        logging.exception("Remediation simulation failed")
