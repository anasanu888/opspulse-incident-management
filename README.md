# OpsPulse – Incident Detection & Auto-Remediation Lab

Nine-container Docker Compose project for DevOps practice.

**Containers:** Nginx, MySQL, Redis, API Service, Event Ingestor, Rule Engine, Remediation Worker, Notification Service, Web Dashboard.

Flow: Browser -> Nginx -> Dashboard/API -> Redis event queue -> Event Ingestor -> MySQL + rules queue -> Rule Engine -> remediation queue -> Remediation Worker -> MySQL + notification queue -> Notification Service logs.

Remediation is simulated only. No real servers, containers, or cloud resources are modified.

## Setup
1. Copy `.env.example` to `.env`.
2. Change the sample passwords.
3. Run `docker compose up -d --build`.
4. Browse to http://localhost:8080.
5. Submit an incident from the dashboard.

API test:
```bash
curl -X POST http://localhost:8080/api/incidents -H "Content-Type: application/json" -d '{"service":"payments-api","environment":"lab","severity":"critical","metric":"cpu","value":96,"message":"CPU threshold exceeded"}'
```

Useful commands: `docker compose ps`, `docker compose logs -f`, `docker compose down`, `docker compose down -v` (deletes persistent volumes).

Learning: Dockerfiles, Compose, reverse proxy, service discovery, health checks, networks, volumes, environment variables, Redis queues, logs and troubleshooting.

This is a learning demo, not a production-ready incident management platform. Authentication, TLS, durable queue guarantees, retries/dead-letter handling and production secrets management are out of scope.
