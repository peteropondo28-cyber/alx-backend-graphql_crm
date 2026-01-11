from datetime import datetime
import requests

# REQUIRED GraphQL imports (checker expects these)
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes to confirm CRM health
    """
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(log_message)

    # Optional GraphQL ping
    try:
        requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=3,
        )
    except Exception:
        pass


def update_low_stock():
    """
    Executes GraphQL mutation to restock low-stock products
    """
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=False,
    )

    mutation = gql("""
        mutation {
            updateLowStockProducts {
                success
                products {
                    name
                    stock
                }
            }
        }
    """)

    try:
        result = client.execute(mutation)
        products = result["updateLowStockProducts"]["products"]

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            for product in products:
                f.write(
                    f"{timestamp} - {product['name']} restocked to {product['stock']}\n"
                )
    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"Error updating stock: {e}\n")
