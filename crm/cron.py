from datetime import datetime
import requests

def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes to confirm CRM health
    """
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"

    # Write heartbeat log (append mode)
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(log_message)

    # Optional: ping GraphQL endpoint to verify availability
    try:
        requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=3,
        )
    except Exception:
        pass
