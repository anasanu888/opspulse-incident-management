from flask import Flask, request, jsonify
from common.ops import wait_redis
import json
app=Flask(__name__); q=wait_redis()
@app.get("/health")
def health(): return {"status":"ok","service":"api-service"}
@app.post("/incidents")
def create():
    d=request.get_json(silent=True) or {}
    required=["service","environment","severity","metric","value","message"]
    missing=[x for x in required if x not in d]
    if missing: return jsonify(error="Missing fields",fields=missing),400
    if str(d["severity"]).lower() not in ["low","medium","high","critical"]:
        return jsonify(error="Invalid severity"),400
    try: d["value"]=float(d["value"])
    except (ValueError,TypeError): return jsonify(error="value must be numeric"),400
    q.rpush("opspulse:events",json.dumps(d))
    return jsonify(message="Incident queued",queued=True),202
@app.get("/stats")
def stats():
    return {"events":q.llen("opspulse:events"),"rules":q.llen("opspulse:rules"),"actions":q.llen("opspulse:remediations")}
if __name__=="__main__": app.run(host="0.0.0.0",port=5000)
