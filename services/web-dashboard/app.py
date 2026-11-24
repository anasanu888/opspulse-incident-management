from flask import Flask, request, redirect, render_template_string
from common.ops import wait_db, db
import requests
app=Flask(__name__); wait_db()
PAGE='''<!doctype html><html><head><title>OpsPulse</title><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{font-family:Arial;background:#101827;color:#e5e7eb;margin:0;padding:28px}.wrap{max-width:1100px;margin:auto}.card{background:#1d293b;padding:18px;border-radius:12px;margin:14px 0}.muted{color:#9ca3af}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px}input,select,button{padding:10px;border-radius:7px;border:1px solid #475569;margin:4px;background:#0f172a;color:#e5e7eb}button{background:#2563eb;cursor:pointer}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:9px;border-bottom:1px solid #374151;font-size:13px}.pill{background:#334155;padding:4px 8px;border-radius:20px}</style></head><body><div class="wrap">
<h1>OpsPulse <span class="pill">INCIDENT COMMAND</span></h1><p class="muted">Incident detection • rule evaluation • simulated remediation</p>
<div class="card"><h3>Inject a test incident</h3><form method="post" action="/submit"><div class="grid">
<input name="service" value="payments-api" required><input name="environment" value="lab" required>
<select name="severity"><option>critical</option><option>high</option><option>medium</option><option>low</option></select>
<select name="metric"><option>cpu</option><option>memory</option><option>http_5xx</option><option>latency</option></select>
<input name="value" type="number" step="any" value="96" required><input name="message" value="Threshold exceeded in lab" required></div><button>Submit incident</button></form></div>
<div class="card"><h3>Recent incidents</h3><table><tr><th>ID</th><th>Service</th><th>Severity</th><th>Metric</th><th>Value</th><th>Status</th><th>Created</th></tr>
{% for x in incidents %}<tr><td>{{x.id}}</td><td>{{x.service_name}}</td><td>{{x.severity}}</td><td>{{x.metric}}</td><td>{{x.metric_value}}</td><td><span class="pill">{{x.status}}</span></td><td>{{x.created_at}}</td></tr>{% endfor %}</table></div>
<div class="card"><h3>Remediation activity</h3><table><tr><th>Incident</th><th>Action</th><th>Status</th><th>Details</th></tr>
{% for a in actions %}<tr><td>{{a.incident_id}}</td><td>{{a.action_name}}</td><td>{{a.status}}</td><td>{{a.details}}</td></tr>{% endfor %}</table></div>
<p class="muted">Lab only: remediation is simulated; no infrastructure is changed.</p></div></body></html>'''
@app.get("/")
def index():
    with db() as c:
        c.execute("SELECT * FROM incidents ORDER BY id DESC LIMIT 30"); incidents=c.fetchall()
        c.execute("SELECT * FROM remediation_actions ORDER BY id DESC LIMIT 30"); actions=c.fetchall()
    return render_template_string(PAGE,incidents=incidents,actions=actions)
@app.post("/submit")
def submit():
    p={k:request.form[k] for k in ["service","environment","severity","metric","message"]}; p["value"]=float(request.form["value"])
    requests.post("http://api-service:5000/incidents",json=p,timeout=5)
    return redirect("/")
@app.get("/health")
def health(): return {"status":"ok","service":"web-dashboard"}
if __name__=="__main__": app.run(host="0.0.0.0",port=5000)
