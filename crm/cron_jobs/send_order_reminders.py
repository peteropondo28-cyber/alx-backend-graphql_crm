from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=False,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql("""
query {
  orders(lastDays: 7, status: "PENDING") {
    id
    customer {
      email
    }
  }
}
""")

result = client.execute(query)

timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

with open("/tmp/order_reminders_log.txt", "a") as f:
    for order in result.get("orders", []):
        f.write(f"{timestamp} Order {order['id']} - {order['customer']['email']}\n")

print("Order reminders processed!")
